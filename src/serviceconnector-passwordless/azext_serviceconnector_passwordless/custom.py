# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------


# pylint: disable=too-many-locals,too-many-statements,unused-argument,too-many-positional-arguments
from knack.log import get_logger
from knack.util import todict
from azure.cli.command_modules.serviceconnector._resource_config import (
    CLIENT_TYPE,
    RESOURCE,
    OPT_OUT_OPTION
)
from azure.cli.command_modules.serviceconnector._validators import (
    get_target_resource_name,
)
from azure.cli.core.azclierror import (
    ValidationError,
)
logger = get_logger(__name__)

def connection_create_ext(cmd, client,
                          connection_name=None, client_type=None,
                          source_resource_group=None, source_id=None,
                          target_resource_group=None, target_id=None,
                          secret_auth_info=None, secret_auth_info_auto=None,
                          user_identity_auth_info=None, system_identity_auth_info=None,
                          workload_identity_auth_info=None,                     # only used as arg
                          service_principal_auth_info_secret=None,
                          key_vault_id=None,
                          app_config_id=None,
                          service_endpoint=None,
                          private_endpoint=None,
                          store_in_connection_string=False,
                          new_addon=False, no_wait=False,
                          yes=False, new=False,
                          # Resource.KubernetesCluster
                          cluster=None, scope=None, enable_csi=False,
                          customized_keys=None,
                          opt_out_list=None,
                          site=None, slot=None,                                  # Resource.WebApp
                          spring=None, app=None, deployment='default',           # Resource.SpringCloud
                          # Resource.*Postgres, Resource.*Sql*
                          server=None, database=None,
                          # Resource.FabricSQL
                          connstr_props=None,
                          fabric_workspace_uuid=None,
                          fabric_sql_db_uuid=None,
                          **kwargs,
                          ):

    from azure.cli.command_modules.serviceconnector.custom import connection_create_func
    from ._credential_free import get_enable_mi_for_db_linker_func

    linker = todict(client.get(resource_uri=source_id, linker_name=connection_name))
    logger.warning(f"Existing properties for comparison: {linker}")

    if (linker.get('id') is not None):
        all_auth_info = []
        if secret_auth_info is not None:
            all_auth_info.append(secret_auth_info)
        if secret_auth_info_auto is not None:
            all_auth_info.append(secret_auth_info_auto)
        if user_identity_auth_info is not None:
            all_auth_info.append(user_identity_auth_info)
        if system_identity_auth_info is not None:
            all_auth_info.append(system_identity_auth_info)
        if service_principal_auth_info_secret is not None:
            all_auth_info.append(service_principal_auth_info_secret)

        # validate auth info
        if len(all_auth_info) > 1:
            raise ValidationError('Only one auth info is needed')
        # when user provides auth info
        if len(all_auth_info) == 1:
            auth_info = all_auth_info[0]
        # when user doesn't provide auth info and linker is not secret-with-username type
        elif not all_auth_info and (linker.get('authInfo') is None or
                                    linker.get('authInfo').get('authType') != 'secret' or
                                    not linker.get('authInfo').get('name')):
            auth_info = linker.get('authInfo')
        else:
            raise ValidationError('Auth info argument should be provided when '
                                  'updating the connection: {}'.format(linker.get('name')))
        # validate the properties to be updated
        if client_type is None and not all_auth_info:
            raise ValidationError(
                'Either client type or auth info should be specified to update')
        auth_action = 'optOutAllAuth' if (opt_out_list is not None and
                                          OPT_OUT_OPTION.AUTHENTICATION.value in opt_out_list) else None
        if auth_info is not None:
            auth_info["auth_mode"] = auth_action

        if linker.get('secretStore') and linker.get('secretStore').get('keyVaultId'):
            key_vault_id = key_vault_id or linker.get('secretStore').get('keyVaultId')

        client_type = client_type or linker.get('clientType')
        if store_in_connection_string:
            if client_type == CLIENT_TYPE.Dotnet.value:
                client_type = CLIENT_TYPE.DotnetConnectionString.value
            else:
                logger.warning('client_type is not dotnet, ignore "--config-connstr"')

        if linker.get('configurationInfo') and linker.get('configurationInfo').get('customizedKeys'):
            customized_keys = customized_keys or linker.get('configurationInfo').get('customizedKeys')

        if linker.get('configurationInfo') and linker.get('configurationInfo').get('additionalConnectionStringProperties'):
            connstr_props = connstr_props or linker.get(
                'configurationInfo').get('additionalConnectionStringProperties')

        config_action = 'optOut' if (opt_out_list is not None and
                                     OPT_OUT_OPTION.CONFIGURATION_INFO.value in opt_out_list) else None
        public_network_action = 'optOut' if (opt_out_list is not None and
                                             OPT_OUT_OPTION.PUBLIC_NETWORK.value in opt_out_list) else None

        target_type = get_target_resource_name(cmd)
        if target_type == RESOURCE.FabricSql:
            targetService = {
                "type": "FabricPlatform",
                "endpoint": target_id
            }
        else:
            targetService = {
                "type": "AzureResource",
                "id": target_id
            }
        newProperties = {
            'targetService': targetService,
            'authInfo': auth_info,
            'secretStore': {
                'keyVaultId': key_vault_id,
            },
            'clientType': client_type,
            # scope can be updated in container app while cannot be updated in aks due to some limitations
            'scope': scope or linker.get('scope'),
            'configurationInfo': {
                'customizedKeys': customized_keys,
                'configurationStore': {
                    'appConfigurationId': app_config_id
                },
                'additionalConnectionStringProperties': connstr_props,
                'action': config_action
            },
            'publicNetworkSolution': {
                'action': public_network_action
            }
        }
        if service_endpoint:
            newProperties['vNetSolution'] = {
                'type': 'serviceEndpoint'
            }
        if private_endpoint:
            newProperties['vNetSolution'] = {
                'type': 'privateLink'
            }

        if enable_csi:
            newProperties['targetService']['resourceProperties'] = {
                'type': 'KeyVault',
                'connectAsKubernetesCsiDriver': enable_csi,
            }

        def deep_compare_properties(new_props, existing_props):
            """
            Deep comparison function that checks if there are meaningful differences
            between new properties and existing properties, ignoring None values.
            Returns True if there are differences that require an update.
            """
            def has_meaningful_changes(new_value, existing_value):
                if new_value is None:
                    # If new value is None, no change needed
                    return False

                if isinstance(new_value, dict) and isinstance(existing_value, dict):
                    # For nested dictionaries, check each key recursively
                    for key, value in new_value.items():
                        existing_nested = existing_value.get(key) if existing_value else None
                        if has_meaningful_changes(value, existing_nested):
                            return True
                    return False
                elif isinstance(new_value, dict) and existing_value is None:
                    # If existing is None but new is a dict, check if any values in new dict are meaningful
                    for value in new_value.values():
                        if value is not None:
                            return True
                    return False
                else:
                    # For primitive values, compare directly
                    return new_value != existing_value

            # Check if any property has meaningful changes
            for key, new_value in new_props.items():
                existing_value = existing_props.get(key) if existing_props else None
                logger.warning("compare " + key + " new_value: " + str(new_value) +
                               " existing_value: " + str(existing_value) + "\n ")
                if has_meaningful_changes(new_value, existing_value):
                    return True
            return False

        # Check if there are any meaningful changes
        logger.warning(f"New properties for comparison: {newProperties}")
        if not deep_compare_properties(newProperties, linker):
            logger.warning('Connection exists and no property to be updated, skip the update operation.')
            return linker
    # return

    return connection_create_func(cmd, client, connection_name, client_type,
                                  source_resource_group, source_id,
                                  target_resource_group, target_id,
                                  secret_auth_info, secret_auth_info_auto,
                                  user_identity_auth_info, system_identity_auth_info,
                                  service_principal_auth_info_secret,
                                  key_vault_id,
                                  service_endpoint,
                                  private_endpoint,
                                  store_in_connection_string,
                                  new_addon, no_wait,
                                  # Resource.KubernetesCluster
                                  cluster, scope, enable_csi,
                                  site, slot,
                                  spring, app, deployment,
                                  server, database,
                                  enable_mi_for_db_linker=get_enable_mi_for_db_linker_func(yes, new),
                                  customized_keys=customized_keys,
                                  opt_out_list=opt_out_list,
                                  app_config_id=app_config_id,
                                  connstr_props=connstr_props,
                                  fabric_workspace_uuid=fabric_workspace_uuid,
                                  fabric_sql_db_uuid=fabric_sql_db_uuid,
                                  **kwargs)


def local_connection_create_ext(cmd, client,  # pylint: disable=too-many-locals,too-many-statements,too-many-positional-arguments
                                resource_group_name,
                                connection_name=None,
                                location=None,
                                client_type=None,
                                target_resource_group=None, target_id=None,
                                secret_auth_info=None, secret_auth_info_auto=None,
                                user_account_auth_info=None,                      # new auth info
                                service_principal_auth_info_secret=None,
                                no_wait=False,
                                customized_keys=None,
                                yes=False, new=False,
                                # Resource.*Postgres, Resource.*Sql*
                                server=None, database=None,
                                **kwargs
                                ):
    from azure.cli.command_modules.serviceconnector.custom import local_connection_create_func
    from ._credential_free import get_enable_mi_for_db_linker_func
    return local_connection_create_func(cmd, client,
                                        resource_group_name,
                                        connection_name,
                                        location,
                                        client_type,
                                        target_resource_group, target_id,
                                        secret_auth_info, secret_auth_info_auto,
                                        user_account_auth_info,                      # new auth info
                                        service_principal_auth_info_secret,
                                        no_wait,
                                        # Resource.*Postgres, Resource.*Sql*
                                        server, database,
                                        enable_mi_for_db_linker=get_enable_mi_for_db_linker_func(yes, new),
                                        customized_keys=customized_keys,
                                        **kwargs)
