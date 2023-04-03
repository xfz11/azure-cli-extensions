# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#
# Code generated by aaz-dev-tools
# --------------------------------------------------------------------------------------------

# pylint: skip-file
# flake8: noqa

from azure.cli.core.aaz import *


@register_command(
    "databricks workspace update",
)
class Update(AAZCommand):
    """Update the workspace.

    :example: Update the workspace's tags.
        az databricks workspace update --resource-group MyResourceGroup --name MyWorkspace --tags key1=value1 key2=value2

    :example: Clean the workspace's tags.
        az databricks workspace update --resource-group MyResourceGroup --name MyWorkspace --tags ""

    :example: Prepare for CMK encryption by assigning identity for storage account.
        az databricks workspace update --resource-group MyResourceGroup --name MyWorkspace --prepare-encryption

    :example: Configure CMK encryption
        az databricks workspace update --resource-group MyResourceGroup --name MyWorkspace --key-source Microsoft.KeyVault --key-name MyKey --key-vault https://myKeyVault.vault.azure.net/ --key-version 00000000000000000000000000000000

    :example: Revert encryption to Microsoft Managed Keys
        az databricks workspace update --resource-group MyResourceGroup --name MyWorkspace --key-source Default
    """

    _aaz_info = {
        "version": "2023-02-01",
        "resources": [
            ["mgmt-plane", "/subscriptions/{}/resourcegroups/{}/providers/microsoft.databricks/workspaces/{}", "2023-02-01"],
        ]
    }

    AZ_SUPPORT_NO_WAIT = True

    AZ_SUPPORT_GENERIC_UPDATE = True

    def _handler(self, command_args):
        super()._handler(command_args)
        return self.build_lro_poller(self._execute_operations, self._output)

    _args_schema = None

    @classmethod
    def _build_arguments_schema(cls, *args, **kwargs):
        if cls._args_schema is not None:
            return cls._args_schema
        cls._args_schema = super()._build_arguments_schema(*args, **kwargs)

        # define Arg Group ""

        _args_schema = cls._args_schema
        _args_schema.resource_group = AAZResourceGroupNameArg(
            required=True,
        )
        _args_schema.name = AAZStrArg(
            options=["-n", "--name"],
            help="The name of the workspace.",
            required=True,
            id_part="name",
            fmt=AAZStrArgFormat(
                max_length=64,
                min_length=3,
            ),
        )
        _args_schema.prepare_encryption = AAZBoolArg(
            options=["--prepare-encryption"],
            help="Flag to enable the Managed Identity for managed storage account to prepare for CMK encryption.",
        )
        _args_schema.sku = AAZStrArg(
            options=["--sku"],
            help="The SKU tier name.  Allowed values: premium, standard, trial.",
        )
        _args_schema.tags = AAZDictArg(
            options=["--tags"],
            help="Space-separated tags: key[=value] [key[=value] ...]. Use \"\" to clear existing tags.",
            nullable=True,
        )

        tags = cls._args_schema.tags
        tags.Element = AAZStrArg(
            nullable=True,
        )

        # define Arg Group "Encryption"

        _args_schema = cls._args_schema
        _args_schema.key_name = AAZStrArg(
            options=["--key-name"],
            arg_group="Encryption",
            help="The name of KeyVault key.",
            nullable=True,
        )
        _args_schema.key_source = AAZStrArg(
            options=["--key-source"],
            arg_group="Encryption",
            help="The encryption key source (provider).  Allowed values: Default, Microsoft.Keyvault.",
            nullable=True,
            enum={"Default": "Default", "Microsoft.Keyvault": "Microsoft.Keyvault"},
        )
        _args_schema.key_vault = AAZStrArg(
            options=["--key-vault"],
            arg_group="Encryption",
            help="The Uri of KeyVault.",
            nullable=True,
        )
        _args_schema.key_version = AAZStrArg(
            options=["--key-version"],
            arg_group="Encryption",
            help="The version of KeyVault key. It is optional when updating CMK.",
            nullable=True,
        )

        # define Arg Group "Parameters"

        # define Arg Group "Properties"

        # define Arg Group "Sku"
        return cls._args_schema

    _args_workspace_custom_boolean_parameter_update = None

    @classmethod
    def _build_args_workspace_custom_boolean_parameter_update(cls, _schema):
        if cls._args_workspace_custom_boolean_parameter_update is not None:
            _schema.prepare_encryption_value = cls._args_workspace_custom_boolean_parameter_update.prepare_encryption_value
            return

        cls._args_workspace_custom_boolean_parameter_update = AAZObjectArg(
            nullable=True,
        )

        workspace_custom_boolean_parameter_update = cls._args_workspace_custom_boolean_parameter_update
        workspace_custom_boolean_parameter_update.prepare_encryption_value = AAZBoolArg(
            options=["prepare-encryption-value"],
            help="The value which should be used for this field.",
        )

        _schema.prepare_encryption_value = cls._args_workspace_custom_boolean_parameter_update.prepare_encryption_value

    _args_workspace_custom_string_parameter_update = None

    @classmethod
    def _build_args_workspace_custom_string_parameter_update(cls, _schema):
        if cls._args_workspace_custom_string_parameter_update is not None:
            _schema.value = cls._args_workspace_custom_string_parameter_update.value
            return

        cls._args_workspace_custom_string_parameter_update = AAZObjectArg(
            nullable=True,
        )

        workspace_custom_string_parameter_update = cls._args_workspace_custom_string_parameter_update
        workspace_custom_string_parameter_update.value = AAZStrArg(
            options=["value"],
            help="The value which should be used for this field.",
        )

        _schema.value = cls._args_workspace_custom_string_parameter_update.value

    def _execute_operations(self):
        self.pre_operations()
        self.WorkspacesGet(ctx=self.ctx)()
        self.pre_instance_update(self.ctx.vars.instance)
        self.InstanceUpdateByJson(ctx=self.ctx)()
        self.InstanceUpdateByGeneric(ctx=self.ctx)()
        self.post_instance_update(self.ctx.vars.instance)
        yield self.WorkspacesCreateOrUpdate(ctx=self.ctx)()
        self.post_operations()

    @register_callback
    def pre_operations(self):
        pass

    @register_callback
    def post_operations(self):
        pass

    @register_callback
    def pre_instance_update(self, instance):
        pass

    @register_callback
    def post_instance_update(self, instance):
        pass

    def _output(self, *args, **kwargs):
        result = self.deserialize_output(self.ctx.vars.instance, client_flatten=True)
        return result

    class WorkspacesGet(AAZHttpOperation):
        CLIENT_TYPE = "MgmtClient"

        def __call__(self, *args, **kwargs):
            request = self.make_request()
            session = self.client.send_request(request=request, stream=False, **kwargs)
            if session.http_response.status_code in [200]:
                return self.on_200(session)

            return self.on_error(session.http_response)

        @property
        def url(self):
            return self.client.format_url(
                "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Databricks/workspaces/{workspaceName}",
                **self.url_parameters
            )

        @property
        def method(self):
            return "GET"

        @property
        def error_format(self):
            return "ODataV4Format"

        @property
        def url_parameters(self):
            parameters = {
                **self.serialize_url_param(
                    "resourceGroupName", self.ctx.args.resource_group,
                    required=True,
                ),
                **self.serialize_url_param(
                    "subscriptionId", self.ctx.subscription_id,
                    required=True,
                ),
                **self.serialize_url_param(
                    "workspaceName", self.ctx.args.name,
                    required=True,
                ),
            }
            return parameters

        @property
        def query_parameters(self):
            parameters = {
                **self.serialize_query_param(
                    "api-version", "2023-02-01",
                    required=True,
                ),
            }
            return parameters

        @property
        def header_parameters(self):
            parameters = {
                **self.serialize_header_param(
                    "Accept", "application/json",
                ),
            }
            return parameters

        def on_200(self, session):
            data = self.deserialize_http_content(session)
            self.ctx.set_var(
                "instance",
                data,
                schema_builder=self._build_schema_on_200
            )

        _schema_on_200 = None

        @classmethod
        def _build_schema_on_200(cls):
            if cls._schema_on_200 is not None:
                return cls._schema_on_200

            cls._schema_on_200 = AAZObjectType()
            _UpdateHelper._build_schema_workspace_read(cls._schema_on_200)

            return cls._schema_on_200

    class WorkspacesCreateOrUpdate(AAZHttpOperation):
        CLIENT_TYPE = "MgmtClient"

        def __call__(self, *args, **kwargs):
            request = self.make_request()
            session = self.client.send_request(request=request, stream=False, **kwargs)
            if session.http_response.status_code in [202]:
                return self.client.build_lro_polling(
                    self.ctx.args.no_wait,
                    session,
                    self.on_200_201,
                    self.on_error,
                    lro_options={"final-state-via": "azure-async-operation"},
                    path_format_arguments=self.url_parameters,
                )
            if session.http_response.status_code in [200, 201]:
                return self.client.build_lro_polling(
                    self.ctx.args.no_wait,
                    session,
                    self.on_200_201,
                    self.on_error,
                    lro_options={"final-state-via": "azure-async-operation"},
                    path_format_arguments=self.url_parameters,
                )

            return self.on_error(session.http_response)

        @property
        def url(self):
            return self.client.format_url(
                "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Databricks/workspaces/{workspaceName}",
                **self.url_parameters
            )

        @property
        def method(self):
            return "PUT"

        @property
        def error_format(self):
            return "ODataV4Format"

        @property
        def url_parameters(self):
            parameters = {
                **self.serialize_url_param(
                    "resourceGroupName", self.ctx.args.resource_group,
                    required=True,
                ),
                **self.serialize_url_param(
                    "subscriptionId", self.ctx.subscription_id,
                    required=True,
                ),
                **self.serialize_url_param(
                    "workspaceName", self.ctx.args.name,
                    required=True,
                ),
            }
            return parameters

        @property
        def query_parameters(self):
            parameters = {
                **self.serialize_query_param(
                    "api-version", "2023-02-01",
                    required=True,
                ),
            }
            return parameters

        @property
        def header_parameters(self):
            parameters = {
                **self.serialize_header_param(
                    "Content-Type", "application/json",
                ),
                **self.serialize_header_param(
                    "Accept", "application/json",
                ),
            }
            return parameters

        @property
        def content(self):
            _content_value, _builder = self.new_content_builder(
                self.ctx.args,
                value=self.ctx.vars.instance,
            )

            return self.serialize_content(_content_value)

        def on_200_201(self, session):
            data = self.deserialize_http_content(session)
            self.ctx.set_var(
                "instance",
                data,
                schema_builder=self._build_schema_on_200_201
            )

        _schema_on_200_201 = None

        @classmethod
        def _build_schema_on_200_201(cls):
            if cls._schema_on_200_201 is not None:
                return cls._schema_on_200_201

            cls._schema_on_200_201 = AAZObjectType()
            _UpdateHelper._build_schema_workspace_read(cls._schema_on_200_201)

            return cls._schema_on_200_201

    class InstanceUpdateByJson(AAZJsonInstanceUpdateOperation):

        def __call__(self, *args, **kwargs):
            self._update_instance(self.ctx.vars.instance)

        def _update_instance(self, instance):
            _instance_value, _builder = self.new_content_builder(
                self.ctx.args,
                value=instance,
                typ=AAZObjectType
            )
            _builder.set_prop("properties", AAZObjectType, ".", typ_kwargs={"flags": {"required": True, "client_flatten": True}})
            _builder.set_prop("sku", AAZObjectType)
            _builder.set_prop("tags", AAZDictType, ".tags")

            properties = _builder.get(".properties")
            if properties is not None:
                properties.set_prop("parameters", AAZObjectType)

            parameters = _builder.get(".properties.parameters")
            if parameters is not None:
                parameters.set_prop("encryption", AAZObjectType)
                parameters.set_prop("prepareEncryption", AAZObjectType)

            encryption = _builder.get(".properties.parameters.encryption")
            if encryption is not None:
                encryption.set_prop("value", AAZObjectType)

            value = _builder.get(".properties.parameters.encryption.value")
            if value is not None:
                value.set_prop("KeyName", AAZStrType, ".key_name")
                value.set_prop("keySource", AAZStrType, ".key_source")
                value.set_prop("keyvaulturi", AAZStrType, ".key_vault")
                value.set_prop("keyversion", AAZStrType, ".key_version")

            prepare_encryption = _builder.get(".properties.parameters.prepareEncryption")
            if prepare_encryption is not None:
                prepare_encryption.set_prop("value", AAZBoolType, ".prepare_encryption", typ_kwargs={"flags": {"required": True}})

            sku = _builder.get(".sku")
            if sku is not None:
                sku.set_prop("name", AAZStrType, ".sku", typ_kwargs={"flags": {"required": True}})

            tags = _builder.get(".tags")
            if tags is not None:
                tags.set_elements(AAZStrType, ".")

            return _instance_value

    class InstanceUpdateByGeneric(AAZGenericInstanceUpdateOperation):

        def __call__(self, *args, **kwargs):
            self._update_instance_by_generic(
                self.ctx.vars.instance,
                self.ctx.generic_update_args
            )


class _UpdateHelper:
    """Helper class for Update"""

    @classmethod
    def _build_schema_workspace_custom_boolean_parameter_update(cls, _builder):
        if _builder is None:
            return
        _builder.set_prop("value", AAZBoolType, ".prepare_encryption_value", typ_kwargs={"flags": {"required": True}})

    @classmethod
    def _build_schema_workspace_custom_string_parameter_update(cls, _builder):
        if _builder is None:
            return
        _builder.set_prop("value", AAZStrType, ".value", typ_kwargs={"flags": {"required": True}})

    _schema_created_by_read = None

    @classmethod
    def _build_schema_created_by_read(cls, _schema):
        if cls._schema_created_by_read is not None:
            _schema.application_id = cls._schema_created_by_read.application_id
            _schema.oid = cls._schema_created_by_read.oid
            _schema.puid = cls._schema_created_by_read.puid
            return

        cls._schema_created_by_read = _schema_created_by_read = AAZObjectType()

        created_by_read = _schema_created_by_read
        created_by_read.application_id = AAZStrType(
            serialized_name="applicationId",
            flags={"read_only": True},
        )
        created_by_read.oid = AAZStrType(
            flags={"read_only": True},
        )
        created_by_read.puid = AAZStrType(
            flags={"read_only": True},
        )

        _schema.application_id = cls._schema_created_by_read.application_id
        _schema.oid = cls._schema_created_by_read.oid
        _schema.puid = cls._schema_created_by_read.puid

    _schema_managed_identity_configuration_read = None

    @classmethod
    def _build_schema_managed_identity_configuration_read(cls, _schema):
        if cls._schema_managed_identity_configuration_read is not None:
            _schema.principal_id = cls._schema_managed_identity_configuration_read.principal_id
            _schema.tenant_id = cls._schema_managed_identity_configuration_read.tenant_id
            _schema.type = cls._schema_managed_identity_configuration_read.type
            return

        cls._schema_managed_identity_configuration_read = _schema_managed_identity_configuration_read = AAZObjectType()

        managed_identity_configuration_read = _schema_managed_identity_configuration_read
        managed_identity_configuration_read.principal_id = AAZStrType(
            serialized_name="principalId",
            flags={"read_only": True},
        )
        managed_identity_configuration_read.tenant_id = AAZStrType(
            serialized_name="tenantId",
            flags={"read_only": True},
        )
        managed_identity_configuration_read.type = AAZStrType(
            flags={"read_only": True},
        )

        _schema.principal_id = cls._schema_managed_identity_configuration_read.principal_id
        _schema.tenant_id = cls._schema_managed_identity_configuration_read.tenant_id
        _schema.type = cls._schema_managed_identity_configuration_read.type

    _schema_workspace_custom_boolean_parameter_read = None

    @classmethod
    def _build_schema_workspace_custom_boolean_parameter_read(cls, _schema):
        if cls._schema_workspace_custom_boolean_parameter_read is not None:
            _schema.type = cls._schema_workspace_custom_boolean_parameter_read.type
            _schema.value = cls._schema_workspace_custom_boolean_parameter_read.value
            return

        cls._schema_workspace_custom_boolean_parameter_read = _schema_workspace_custom_boolean_parameter_read = AAZObjectType()

        workspace_custom_boolean_parameter_read = _schema_workspace_custom_boolean_parameter_read
        workspace_custom_boolean_parameter_read.type = AAZStrType(
            flags={"read_only": True},
        )
        workspace_custom_boolean_parameter_read.value = AAZBoolType(
            flags={"required": True},
        )

        _schema.type = cls._schema_workspace_custom_boolean_parameter_read.type
        _schema.value = cls._schema_workspace_custom_boolean_parameter_read.value

    _schema_workspace_custom_string_parameter_read = None

    @classmethod
    def _build_schema_workspace_custom_string_parameter_read(cls, _schema):
        if cls._schema_workspace_custom_string_parameter_read is not None:
            _schema.type = cls._schema_workspace_custom_string_parameter_read.type
            _schema.value = cls._schema_workspace_custom_string_parameter_read.value
            return

        cls._schema_workspace_custom_string_parameter_read = _schema_workspace_custom_string_parameter_read = AAZObjectType()

        workspace_custom_string_parameter_read = _schema_workspace_custom_string_parameter_read
        workspace_custom_string_parameter_read.type = AAZStrType(
            flags={"read_only": True},
        )
        workspace_custom_string_parameter_read.value = AAZStrType(
            flags={"required": True},
        )

        _schema.type = cls._schema_workspace_custom_string_parameter_read.type
        _schema.value = cls._schema_workspace_custom_string_parameter_read.value

    _schema_workspace_read = None

    @classmethod
    def _build_schema_workspace_read(cls, _schema):
        if cls._schema_workspace_read is not None:
            _schema.id = cls._schema_workspace_read.id
            _schema.location = cls._schema_workspace_read.location
            _schema.name = cls._schema_workspace_read.name
            _schema.properties = cls._schema_workspace_read.properties
            _schema.sku = cls._schema_workspace_read.sku
            _schema.system_data = cls._schema_workspace_read.system_data
            _schema.tags = cls._schema_workspace_read.tags
            _schema.type = cls._schema_workspace_read.type
            return

        cls._schema_workspace_read = _schema_workspace_read = AAZObjectType()

        workspace_read = _schema_workspace_read
        workspace_read.id = AAZStrType(
            flags={"read_only": True},
        )
        workspace_read.location = AAZStrType(
            flags={"required": True},
        )
        workspace_read.name = AAZStrType(
            flags={"read_only": True},
        )
        workspace_read.properties = AAZObjectType(
            flags={"required": True, "client_flatten": True},
        )
        workspace_read.sku = AAZObjectType()
        workspace_read.system_data = AAZObjectType(
            serialized_name="systemData",
            flags={"read_only": True},
        )
        workspace_read.tags = AAZDictType()
        workspace_read.type = AAZStrType(
            flags={"read_only": True},
        )

        properties = _schema_workspace_read.properties
        properties.authorizations = AAZListType()
        properties.created_by = AAZObjectType(
            serialized_name="createdBy",
        )
        cls._build_schema_created_by_read(properties.created_by)
        properties.created_date_time = AAZStrType(
            serialized_name="createdDateTime",
            flags={"read_only": True},
        )
        properties.disk_encryption_set_id = AAZStrType(
            serialized_name="diskEncryptionSetId",
            flags={"read_only": True},
        )
        properties.encryption = AAZObjectType()
        properties.managed_disk_identity = AAZObjectType(
            serialized_name="managedDiskIdentity",
        )
        cls._build_schema_managed_identity_configuration_read(properties.managed_disk_identity)
        properties.managed_resource_group_id = AAZStrType(
            serialized_name="managedResourceGroupId",
            flags={"required": True},
        )
        properties.parameters = AAZObjectType()
        properties.private_endpoint_connections = AAZListType(
            serialized_name="privateEndpointConnections",
            flags={"read_only": True},
        )
        properties.provisioning_state = AAZStrType(
            serialized_name="provisioningState",
            flags={"read_only": True},
        )
        properties.public_network_access = AAZStrType(
            serialized_name="publicNetworkAccess",
        )
        properties.required_nsg_rules = AAZStrType(
            serialized_name="requiredNsgRules",
        )
        properties.storage_account_identity = AAZObjectType(
            serialized_name="storageAccountIdentity",
        )
        cls._build_schema_managed_identity_configuration_read(properties.storage_account_identity)
        properties.ui_definition_uri = AAZStrType(
            serialized_name="uiDefinitionUri",
        )
        properties.updated_by = AAZObjectType(
            serialized_name="updatedBy",
        )
        cls._build_schema_created_by_read(properties.updated_by)
        properties.workspace_id = AAZStrType(
            serialized_name="workspaceId",
            flags={"read_only": True},
        )
        properties.workspace_url = AAZStrType(
            serialized_name="workspaceUrl",
            flags={"read_only": True},
        )

        authorizations = _schema_workspace_read.properties.authorizations
        authorizations.Element = AAZObjectType()

        _element = _schema_workspace_read.properties.authorizations.Element
        _element.principal_id = AAZStrType(
            serialized_name="principalId",
            flags={"required": True},
        )
        _element.role_definition_id = AAZStrType(
            serialized_name="roleDefinitionId",
            flags={"required": True},
        )

        encryption = _schema_workspace_read.properties.encryption
        encryption.entities = AAZObjectType(
            flags={"required": True},
        )

        entities = _schema_workspace_read.properties.encryption.entities
        entities.managed_disk = AAZObjectType(
            serialized_name="managedDisk",
        )
        entities.managed_services = AAZObjectType(
            serialized_name="managedServices",
        )

        managed_disk = _schema_workspace_read.properties.encryption.entities.managed_disk
        managed_disk.key_source = AAZStrType(
            serialized_name="keySource",
            flags={"required": True},
        )
        managed_disk.key_vault_properties = AAZObjectType(
            serialized_name="keyVaultProperties",
            flags={"required": True},
        )
        managed_disk.rotation_to_latest_key_version_enabled = AAZBoolType(
            serialized_name="rotationToLatestKeyVersionEnabled",
        )

        key_vault_properties = _schema_workspace_read.properties.encryption.entities.managed_disk.key_vault_properties
        key_vault_properties.key_name = AAZStrType(
            serialized_name="keyName",
            flags={"required": True},
        )
        key_vault_properties.key_vault_uri = AAZStrType(
            serialized_name="keyVaultUri",
            flags={"required": True},
        )
        key_vault_properties.key_version = AAZStrType(
            serialized_name="keyVersion",
            flags={"required": True},
        )

        managed_services = _schema_workspace_read.properties.encryption.entities.managed_services
        managed_services.key_source = AAZStrType(
            serialized_name="keySource",
            flags={"required": True},
        )
        managed_services.key_vault_properties = AAZObjectType(
            serialized_name="keyVaultProperties",
        )

        key_vault_properties = _schema_workspace_read.properties.encryption.entities.managed_services.key_vault_properties
        key_vault_properties.key_name = AAZStrType(
            serialized_name="keyName",
            flags={"required": True},
        )
        key_vault_properties.key_vault_uri = AAZStrType(
            serialized_name="keyVaultUri",
            flags={"required": True},
        )
        key_vault_properties.key_version = AAZStrType(
            serialized_name="keyVersion",
            flags={"required": True},
        )

        parameters = _schema_workspace_read.properties.parameters
        parameters.aml_workspace_id = AAZObjectType(
            serialized_name="amlWorkspaceId",
        )
        cls._build_schema_workspace_custom_string_parameter_read(parameters.aml_workspace_id)
        parameters.custom_private_subnet_name = AAZObjectType(
            serialized_name="customPrivateSubnetName",
        )
        cls._build_schema_workspace_custom_string_parameter_read(parameters.custom_private_subnet_name)
        parameters.custom_public_subnet_name = AAZObjectType(
            serialized_name="customPublicSubnetName",
        )
        cls._build_schema_workspace_custom_string_parameter_read(parameters.custom_public_subnet_name)
        parameters.custom_virtual_network_id = AAZObjectType(
            serialized_name="customVirtualNetworkId",
        )
        cls._build_schema_workspace_custom_string_parameter_read(parameters.custom_virtual_network_id)
        parameters.enable_no_public_ip = AAZObjectType(
            serialized_name="enableNoPublicIp",
        )
        cls._build_schema_workspace_custom_boolean_parameter_read(parameters.enable_no_public_ip)
        parameters.encryption = AAZObjectType()
        parameters.load_balancer_backend_pool_name = AAZObjectType(
            serialized_name="loadBalancerBackendPoolName",
        )
        cls._build_schema_workspace_custom_string_parameter_read(parameters.load_balancer_backend_pool_name)
        parameters.load_balancer_id = AAZObjectType(
            serialized_name="loadBalancerId",
        )
        cls._build_schema_workspace_custom_string_parameter_read(parameters.load_balancer_id)
        parameters.nat_gateway_name = AAZObjectType(
            serialized_name="natGatewayName",
        )
        cls._build_schema_workspace_custom_string_parameter_read(parameters.nat_gateway_name)
        parameters.prepare_encryption = AAZObjectType(
            serialized_name="prepareEncryption",
        )
        cls._build_schema_workspace_custom_boolean_parameter_read(parameters.prepare_encryption)
        parameters.public_ip_name = AAZObjectType(
            serialized_name="publicIpName",
        )
        cls._build_schema_workspace_custom_string_parameter_read(parameters.public_ip_name)
        parameters.require_infrastructure_encryption = AAZObjectType(
            serialized_name="requireInfrastructureEncryption",
        )
        cls._build_schema_workspace_custom_boolean_parameter_read(parameters.require_infrastructure_encryption)
        parameters.resource_tags = AAZObjectType(
            serialized_name="resourceTags",
        )
        parameters.storage_account_name = AAZObjectType(
            serialized_name="storageAccountName",
        )
        cls._build_schema_workspace_custom_string_parameter_read(parameters.storage_account_name)
        parameters.storage_account_sku_name = AAZObjectType(
            serialized_name="storageAccountSkuName",
        )
        cls._build_schema_workspace_custom_string_parameter_read(parameters.storage_account_sku_name)
        parameters.vnet_address_prefix = AAZObjectType(
            serialized_name="vnetAddressPrefix",
        )
        cls._build_schema_workspace_custom_string_parameter_read(parameters.vnet_address_prefix)

        encryption = _schema_workspace_read.properties.parameters.encryption
        encryption.type = AAZStrType(
            flags={"read_only": True},
        )
        encryption.value = AAZObjectType()

        value = _schema_workspace_read.properties.parameters.encryption.value
        value.key_name = AAZStrType(
            serialized_name="KeyName",
        )
        value.key_source = AAZStrType(
            serialized_name="keySource",
        )
        value.keyvaulturi = AAZStrType()
        value.keyversion = AAZStrType()

        resource_tags = _schema_workspace_read.properties.parameters.resource_tags
        resource_tags.type = AAZStrType(
            flags={"read_only": True},
        )

        private_endpoint_connections = _schema_workspace_read.properties.private_endpoint_connections
        private_endpoint_connections.Element = AAZObjectType()

        _element = _schema_workspace_read.properties.private_endpoint_connections.Element
        _element.id = AAZStrType(
            flags={"read_only": True},
        )
        _element.name = AAZStrType(
            flags={"read_only": True},
        )
        _element.properties = AAZObjectType(
            flags={"required": True},
        )
        _element.type = AAZStrType(
            flags={"read_only": True},
        )

        properties = _schema_workspace_read.properties.private_endpoint_connections.Element.properties
        properties.group_ids = AAZListType(
            serialized_name="groupIds",
        )
        properties.private_endpoint = AAZObjectType(
            serialized_name="privateEndpoint",
        )
        properties.private_link_service_connection_state = AAZObjectType(
            serialized_name="privateLinkServiceConnectionState",
            flags={"required": True},
        )
        properties.provisioning_state = AAZStrType(
            serialized_name="provisioningState",
            flags={"read_only": True},
        )

        group_ids = _schema_workspace_read.properties.private_endpoint_connections.Element.properties.group_ids
        group_ids.Element = AAZStrType()

        private_endpoint = _schema_workspace_read.properties.private_endpoint_connections.Element.properties.private_endpoint
        private_endpoint.id = AAZStrType(
            flags={"read_only": True},
        )

        private_link_service_connection_state = _schema_workspace_read.properties.private_endpoint_connections.Element.properties.private_link_service_connection_state
        private_link_service_connection_state.actions_required = AAZStrType(
            serialized_name="actionsRequired",
        )
        private_link_service_connection_state.description = AAZStrType()
        private_link_service_connection_state.status = AAZStrType(
            flags={"required": True},
        )

        sku = _schema_workspace_read.sku
        sku.name = AAZStrType(
            flags={"required": True},
        )
        sku.tier = AAZStrType()

        system_data = _schema_workspace_read.system_data
        system_data.created_at = AAZStrType(
            serialized_name="createdAt",
        )
        system_data.created_by = AAZStrType(
            serialized_name="createdBy",
        )
        system_data.created_by_type = AAZStrType(
            serialized_name="createdByType",
        )
        system_data.last_modified_at = AAZStrType(
            serialized_name="lastModifiedAt",
        )
        system_data.last_modified_by = AAZStrType(
            serialized_name="lastModifiedBy",
        )
        system_data.last_modified_by_type = AAZStrType(
            serialized_name="lastModifiedByType",
        )

        tags = _schema_workspace_read.tags
        tags.Element = AAZStrType()

        _schema.id = cls._schema_workspace_read.id
        _schema.location = cls._schema_workspace_read.location
        _schema.name = cls._schema_workspace_read.name
        _schema.properties = cls._schema_workspace_read.properties
        _schema.sku = cls._schema_workspace_read.sku
        _schema.system_data = cls._schema_workspace_read.system_data
        _schema.tags = cls._schema_workspace_read.tags
        _schema.type = cls._schema_workspace_read.type


__all__ = ["Update"]
