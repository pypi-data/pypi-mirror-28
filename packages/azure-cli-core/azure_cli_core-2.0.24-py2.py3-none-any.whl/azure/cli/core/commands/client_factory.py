# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import os

from knack.log import get_logger
from knack.util import CLIError

from azure.cli.core import __version__ as core_version
import azure.cli.core._debug as _debug
from azure.cli.core.profiles._shared import get_client_class, SDKProfile
from azure.cli.core.profiles import ResourceType, get_api_version, get_sdk

logger = get_logger(__name__)
UA_AGENT = "AZURECLI/{}".format(core_version)
ENV_ADDITIONAL_USER_AGENT = 'AZURE_HTTP_USER_AGENT'


def get_mgmt_service_client(cli_ctx, client_or_resource_type, subscription_id=None, api_version=None,
                            **kwargs):
    sdk_profile = None
    if isinstance(client_or_resource_type, ResourceType):
        # Get the versioned client
        client_type = get_client_class(client_or_resource_type)
        api_version = api_version or get_api_version(cli_ctx, client_or_resource_type, as_sdk_profile=True)
        if isinstance(api_version, SDKProfile):
            sdk_profile = api_version.profile
            api_version = api_version.default_api_version
    else:
        # Get the non-versioned client
        client_type = client_or_resource_type
    client, _ = _get_mgmt_service_client(cli_ctx, client_type, subscription_id=subscription_id,
                                         api_version=api_version, sdk_profile=sdk_profile, **kwargs)
    return client


def get_subscription_service_client(cli_ctx):
    return _get_mgmt_service_client(cli_ctx, get_client_class(ResourceType.MGMT_RESOURCE_SUBSCRIPTIONS),
                                    subscription_bound=False,
                                    api_version=get_api_version(cli_ctx, ResourceType.MGMT_RESOURCE_SUBSCRIPTIONS))


def configure_common_settings(cli_ctx, client):
    client = _debug.change_ssl_cert_verification(client)

    client.config.add_user_agent(UA_AGENT)
    try:
        client.config.add_user_agent(os.environ[ENV_ADDITIONAL_USER_AGENT])
    except KeyError:
        pass

    try:
        command_ext_name = cli_ctx.data['command_extension_name']
        if command_ext_name:
            client.config.add_user_agent("CliExtension/{}".format(command_ext_name))
    except KeyError:
        pass

    for header, value in cli_ctx.data['headers'].items():
        # We are working with the autorest team to expose the add_header functionality of the generated client to avoid
        # having to access private members
        client._client.add_header(header, value)  # pylint: disable=protected-access

    command_name_suffix = ';completer-request' if cli_ctx.data['completer_active'] else ''
    client._client.add_header('CommandName',  # pylint: disable=protected-access
                              "{}{}".format(cli_ctx.data['command'], command_name_suffix))
    client.config.generate_client_request_id = 'x-ms-client-request-id' not in cli_ctx.data['headers']


def _get_mgmt_service_client(cli_ctx,
                             client_type,
                             subscription_bound=True,
                             subscription_id=None,
                             api_version=None,
                             base_url_bound=True,
                             resource=None,
                             sdk_profile=None,
                             **kwargs):
    from azure.cli.core._profile import Profile
    logger.debug('Getting management service client client_type=%s', client_type.__name__)
    resource = resource or cli_ctx.cloud.endpoints.active_directory_resource_id
    profile = Profile(cli_ctx=cli_ctx)
    cred, subscription_id, _ = profile.get_login_credentials(subscription_id=subscription_id, resource=resource)

    client_kwargs = {}
    if base_url_bound:
        client_kwargs = {'base_url': cli_ctx.cloud.endpoints.resource_manager}
    if api_version:
        client_kwargs['api_version'] = api_version
    if sdk_profile:
        client_kwargs['profile'] = sdk_profile
    if kwargs:
        client_kwargs.update(kwargs)

    if subscription_bound:
        client = client_type(cred, subscription_id, **client_kwargs)
    else:
        client = client_type(cred, **client_kwargs)

    configure_common_settings(cli_ctx, client)

    return client, subscription_id


def get_data_service_client(cli_ctx, service_type, account_name, account_key, connection_string=None,
                            sas_token=None, endpoint_suffix=None):
    logger.debug('Getting data service client service_type=%s', service_type.__name__)
    try:
        client_kwargs = {'account_name': account_name,
                         'account_key': account_key,
                         'connection_string': connection_string,
                         'sas_token': sas_token}
        if endpoint_suffix:
            client_kwargs['endpoint_suffix'] = endpoint_suffix
        client = service_type(**client_kwargs)
    except ValueError as exc:
        _ERROR_STORAGE_MISSING_INFO = get_sdk(cli_ctx, ResourceType.DATA_STORAGE,
                                              'common._error#_ERROR_STORAGE_MISSING_INFO')
        if _ERROR_STORAGE_MISSING_INFO in str(exc):
            raise ValueError(exc)
        else:
            raise CLIError('Unable to obtain data client. Check your connection parameters.')
    # TODO: enable Fiddler
    client.request_callback = _get_add_headers_callback(cli_ctx)
    return client


def get_subscription_id(cli_ctx):
    from azure.cli.core._profile import Profile
    _, subscription_id, _ = Profile(cli_ctx=cli_ctx).get_login_credentials()
    return subscription_id


def _get_add_headers_callback(cli_ctx):

    def _add_headers(request):
        agents = [request.headers['User-Agent'], UA_AGENT]
        try:
            agents.append(os.environ[ENV_ADDITIONAL_USER_AGENT])
        except KeyError:
            pass

        request.headers['User-Agent'] = ' '.join(agents)

        try:
            request.headers.update(cli_ctx.data['headers'])
        except KeyError:
            pass

    return _add_headers
