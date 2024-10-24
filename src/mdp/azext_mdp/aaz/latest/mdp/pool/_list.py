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
    "mdp pool list",
)
class List(AAZCommand):
    """List all pools

    :example: List by resource group
        az mdp pool list --resource-group "rg1"

    :example: List by subscription
        az mdp pool list
    """

    _aaz_info = {
        "version": "2024-10-19",
        "resources": [
            ["mgmt-plane", "/subscriptions/{}/providers/microsoft.devopsinfrastructure/pools", "2024-10-19"],
            ["mgmt-plane", "/subscriptions/{}/resourcegroups/{}/providers/microsoft.devopsinfrastructure/pools", "2024-10-19"],
        ]
    }

    AZ_SUPPORT_PAGINATION = True

    def _handler(self, command_args):
        super()._handler(command_args)
        return self.build_paging(self._execute_operations, self._output)

    _args_schema = None

    @classmethod
    def _build_arguments_schema(cls, *args, **kwargs):
        if cls._args_schema is not None:
            return cls._args_schema
        cls._args_schema = super()._build_arguments_schema(*args, **kwargs)

        # define Arg Group ""

        _args_schema = cls._args_schema
        _args_schema.resource_group = AAZResourceGroupNameArg()
        return cls._args_schema

    def _execute_operations(self):
        self.pre_operations()
        condition_0 = has_value(self.ctx.args.resource_group) and has_value(self.ctx.subscription_id)
        condition_1 = has_value(self.ctx.subscription_id) and has_value(self.ctx.args.resource_group) is not True
        if condition_0:
            self.PoolsListByResourceGroup(ctx=self.ctx)()
        if condition_1:
            self.PoolsListBySubscription(ctx=self.ctx)()
        self.post_operations()

    @register_callback
    def pre_operations(self):
        pass

    @register_callback
    def post_operations(self):
        pass

    def _output(self, *args, **kwargs):
        result = self.deserialize_output(self.ctx.vars.instance.value, client_flatten=True)
        next_link = self.deserialize_output(self.ctx.vars.instance.next_link)
        return result, next_link

    class PoolsListByResourceGroup(AAZHttpOperation):
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
                "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DevOpsInfrastructure/pools",
                **self.url_parameters
            )

        @property
        def method(self):
            return "GET"

        @property
        def error_format(self):
            return "MgmtErrorFormat"

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
            }
            return parameters

        @property
        def query_parameters(self):
            parameters = {
                **self.serialize_query_param(
                    "api-version", "2024-10-19",
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

            _schema_on_200 = cls._schema_on_200
            _schema_on_200.next_link = AAZStrType(
                serialized_name="nextLink",
            )
            _schema_on_200.value = AAZListType(
                flags={"required": True},
            )

            value = cls._schema_on_200.value
            value.Element = AAZObjectType()

            _element = cls._schema_on_200.value.Element
            _element.id = AAZStrType(
                flags={"read_only": True},
            )
            _element.identity = AAZObjectType()
            _element.location = AAZStrType(
                flags={"required": True},
            )
            _element.name = AAZStrType(
                flags={"read_only": True},
            )
            _element.properties = AAZObjectType(
                flags={"client_flatten": True},
            )
            _element.system_data = AAZObjectType(
                serialized_name="systemData",
                flags={"read_only": True},
            )
            _element.tags = AAZDictType()
            _element.type = AAZStrType(
                flags={"read_only": True},
            )

            identity = cls._schema_on_200.value.Element.identity
            identity.principal_id = AAZStrType(
                serialized_name="principalId",
                flags={"read_only": True},
            )
            identity.tenant_id = AAZStrType(
                serialized_name="tenantId",
                flags={"read_only": True},
            )
            identity.type = AAZStrType(
                flags={"required": True},
            )
            identity.user_assigned_identities = AAZDictType(
                serialized_name="userAssignedIdentities",
            )

            user_assigned_identities = cls._schema_on_200.value.Element.identity.user_assigned_identities
            user_assigned_identities.Element = AAZObjectType(
                nullable=True,
            )

            _element = cls._schema_on_200.value.Element.identity.user_assigned_identities.Element
            _element.client_id = AAZStrType(
                serialized_name="clientId",
                flags={"read_only": True},
            )
            _element.principal_id = AAZStrType(
                serialized_name="principalId",
                flags={"read_only": True},
            )

            properties = cls._schema_on_200.value.Element.properties
            properties.agent_profile = AAZObjectType(
                serialized_name="agentProfile",
                flags={"required": True},
            )
            properties.dev_center_project_resource_id = AAZStrType(
                serialized_name="devCenterProjectResourceId",
                flags={"required": True},
            )
            properties.fabric_profile = AAZObjectType(
                serialized_name="fabricProfile",
                flags={"required": True},
            )
            properties.maximum_concurrency = AAZIntType(
                serialized_name="maximumConcurrency",
                flags={"required": True},
            )
            properties.organization_profile = AAZObjectType(
                serialized_name="organizationProfile",
                flags={"required": True},
            )
            properties.provisioning_state = AAZStrType(
                serialized_name="provisioningState",
            )

            agent_profile = cls._schema_on_200.value.Element.properties.agent_profile
            agent_profile.kind = AAZStrType(
                flags={"required": True},
            )
            agent_profile.resource_predictions = AAZObjectType(
                serialized_name="resourcePredictions",
            )
            agent_profile.resource_predictions_profile = AAZObjectType(
                serialized_name="resourcePredictionsProfile",
            )

            resource_predictions_profile = cls._schema_on_200.value.Element.properties.agent_profile.resource_predictions_profile
            resource_predictions_profile.kind = AAZStrType(
                flags={"required": True},
            )

            disc_automatic = cls._schema_on_200.value.Element.properties.agent_profile.resource_predictions_profile.discriminate_by("kind", "Automatic")
            disc_automatic.prediction_preference = AAZStrType(
                serialized_name="predictionPreference",
            )

            disc_stateful = cls._schema_on_200.value.Element.properties.agent_profile.discriminate_by("kind", "Stateful")
            disc_stateful.grace_period_time_span = AAZStrType(
                serialized_name="gracePeriodTimeSpan",
            )
            disc_stateful.max_agent_lifetime = AAZStrType(
                serialized_name="maxAgentLifetime",
            )

            fabric_profile = cls._schema_on_200.value.Element.properties.fabric_profile
            fabric_profile.kind = AAZStrType(
                flags={"required": True},
            )

            disc_vmss = cls._schema_on_200.value.Element.properties.fabric_profile.discriminate_by("kind", "Vmss")
            disc_vmss.images = AAZListType(
                flags={"required": True},
            )
            disc_vmss.network_profile = AAZObjectType(
                serialized_name="networkProfile",
            )
            disc_vmss.os_profile = AAZObjectType(
                serialized_name="osProfile",
            )
            disc_vmss.sku = AAZObjectType(
                flags={"required": True},
            )
            disc_vmss.storage_profile = AAZObjectType(
                serialized_name="storageProfile",
            )

            images = cls._schema_on_200.value.Element.properties.fabric_profile.discriminate_by("kind", "Vmss").images
            images.Element = AAZObjectType()

            _element = cls._schema_on_200.value.Element.properties.fabric_profile.discriminate_by("kind", "Vmss").images.Element
            _element.aliases = AAZListType()
            _element.buffer = AAZStrType()
            _element.resource_id = AAZStrType(
                serialized_name="resourceId",
            )
            _element.well_known_image_name = AAZStrType(
                serialized_name="wellKnownImageName",
            )

            aliases = cls._schema_on_200.value.Element.properties.fabric_profile.discriminate_by("kind", "Vmss").images.Element.aliases
            aliases.Element = AAZStrType()

            network_profile = cls._schema_on_200.value.Element.properties.fabric_profile.discriminate_by("kind", "Vmss").network_profile
            network_profile.subnet_id = AAZStrType(
                serialized_name="subnetId",
                flags={"required": True},
            )

            os_profile = cls._schema_on_200.value.Element.properties.fabric_profile.discriminate_by("kind", "Vmss").os_profile
            os_profile.logon_type = AAZStrType(
                serialized_name="logonType",
            )
            os_profile.secrets_management_settings = AAZObjectType(
                serialized_name="secretsManagementSettings",
            )

            secrets_management_settings = cls._schema_on_200.value.Element.properties.fabric_profile.discriminate_by("kind", "Vmss").os_profile.secrets_management_settings
            secrets_management_settings.certificate_store_location = AAZStrType(
                serialized_name="certificateStoreLocation",
            )
            secrets_management_settings.key_exportable = AAZBoolType(
                serialized_name="keyExportable",
                flags={"required": True},
            )
            secrets_management_settings.observed_certificates = AAZListType(
                serialized_name="observedCertificates",
                flags={"required": True},
            )

            observed_certificates = cls._schema_on_200.value.Element.properties.fabric_profile.discriminate_by("kind", "Vmss").os_profile.secrets_management_settings.observed_certificates
            observed_certificates.Element = AAZStrType()

            sku = cls._schema_on_200.value.Element.properties.fabric_profile.discriminate_by("kind", "Vmss").sku
            sku.name = AAZStrType(
                flags={"required": True},
            )

            storage_profile = cls._schema_on_200.value.Element.properties.fabric_profile.discriminate_by("kind", "Vmss").storage_profile
            storage_profile.data_disks = AAZListType(
                serialized_name="dataDisks",
            )
            storage_profile.os_disk_storage_account_type = AAZStrType(
                serialized_name="osDiskStorageAccountType",
            )

            data_disks = cls._schema_on_200.value.Element.properties.fabric_profile.discriminate_by("kind", "Vmss").storage_profile.data_disks
            data_disks.Element = AAZObjectType()

            _element = cls._schema_on_200.value.Element.properties.fabric_profile.discriminate_by("kind", "Vmss").storage_profile.data_disks.Element
            _element.caching = AAZStrType()
            _element.disk_size_gi_b = AAZIntType(
                serialized_name="diskSizeGiB",
            )
            _element.drive_letter = AAZStrType(
                serialized_name="driveLetter",
            )
            _element.storage_account_type = AAZStrType(
                serialized_name="storageAccountType",
            )

            organization_profile = cls._schema_on_200.value.Element.properties.organization_profile
            organization_profile.kind = AAZStrType(
                flags={"required": True},
            )

            disc_azure_dev_ops = cls._schema_on_200.value.Element.properties.organization_profile.discriminate_by("kind", "AzureDevOps")
            disc_azure_dev_ops.organizations = AAZListType(
                flags={"required": True},
            )
            disc_azure_dev_ops.permission_profile = AAZObjectType(
                serialized_name="permissionProfile",
            )

            organizations = cls._schema_on_200.value.Element.properties.organization_profile.discriminate_by("kind", "AzureDevOps").organizations
            organizations.Element = AAZObjectType()

            _element = cls._schema_on_200.value.Element.properties.organization_profile.discriminate_by("kind", "AzureDevOps").organizations.Element
            _element.parallelism = AAZIntType()
            _element.projects = AAZListType()
            _element.url = AAZStrType(
                flags={"required": True},
            )

            projects = cls._schema_on_200.value.Element.properties.organization_profile.discriminate_by("kind", "AzureDevOps").organizations.Element.projects
            projects.Element = AAZStrType()

            permission_profile = cls._schema_on_200.value.Element.properties.organization_profile.discriminate_by("kind", "AzureDevOps").permission_profile
            permission_profile.groups = AAZListType()
            permission_profile.kind = AAZStrType(
                flags={"required": True},
            )
            permission_profile.users = AAZListType()

            groups = cls._schema_on_200.value.Element.properties.organization_profile.discriminate_by("kind", "AzureDevOps").permission_profile.groups
            groups.Element = AAZStrType()

            users = cls._schema_on_200.value.Element.properties.organization_profile.discriminate_by("kind", "AzureDevOps").permission_profile.users
            users.Element = AAZStrType()

            disc_git_hub = cls._schema_on_200.value.Element.properties.organization_profile.discriminate_by("kind", "GitHub")
            disc_git_hub.organizations = AAZListType(
                flags={"required": True},
            )

            organizations = cls._schema_on_200.value.Element.properties.organization_profile.discriminate_by("kind", "GitHub").organizations
            organizations.Element = AAZObjectType()

            _element = cls._schema_on_200.value.Element.properties.organization_profile.discriminate_by("kind", "GitHub").organizations.Element
            _element.repositories = AAZListType()
            _element.url = AAZStrType(
                flags={"required": True},
            )

            repositories = cls._schema_on_200.value.Element.properties.organization_profile.discriminate_by("kind", "GitHub").organizations.Element.repositories
            repositories.Element = AAZStrType()

            system_data = cls._schema_on_200.value.Element.system_data
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

            tags = cls._schema_on_200.value.Element.tags
            tags.Element = AAZStrType()

            return cls._schema_on_200

    class PoolsListBySubscription(AAZHttpOperation):
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
                "/subscriptions/{subscriptionId}/providers/Microsoft.DevOpsInfrastructure/pools",
                **self.url_parameters
            )

        @property
        def method(self):
            return "GET"

        @property
        def error_format(self):
            return "MgmtErrorFormat"

        @property
        def url_parameters(self):
            parameters = {
                **self.serialize_url_param(
                    "subscriptionId", self.ctx.subscription_id,
                    required=True,
                ),
            }
            return parameters

        @property
        def query_parameters(self):
            parameters = {
                **self.serialize_query_param(
                    "api-version", "2024-10-19",
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

            _schema_on_200 = cls._schema_on_200
            _schema_on_200.next_link = AAZStrType(
                serialized_name="nextLink",
            )
            _schema_on_200.value = AAZListType(
                flags={"required": True},
            )

            value = cls._schema_on_200.value
            value.Element = AAZObjectType()

            _element = cls._schema_on_200.value.Element
            _element.id = AAZStrType(
                flags={"read_only": True},
            )
            _element.identity = AAZObjectType()
            _element.location = AAZStrType(
                flags={"required": True},
            )
            _element.name = AAZStrType(
                flags={"read_only": True},
            )
            _element.properties = AAZObjectType(
                flags={"client_flatten": True},
            )
            _element.system_data = AAZObjectType(
                serialized_name="systemData",
                flags={"read_only": True},
            )
            _element.tags = AAZDictType()
            _element.type = AAZStrType(
                flags={"read_only": True},
            )

            identity = cls._schema_on_200.value.Element.identity
            identity.principal_id = AAZStrType(
                serialized_name="principalId",
                flags={"read_only": True},
            )
            identity.tenant_id = AAZStrType(
                serialized_name="tenantId",
                flags={"read_only": True},
            )
            identity.type = AAZStrType(
                flags={"required": True},
            )
            identity.user_assigned_identities = AAZDictType(
                serialized_name="userAssignedIdentities",
            )

            user_assigned_identities = cls._schema_on_200.value.Element.identity.user_assigned_identities
            user_assigned_identities.Element = AAZObjectType(
                nullable=True,
            )

            _element = cls._schema_on_200.value.Element.identity.user_assigned_identities.Element
            _element.client_id = AAZStrType(
                serialized_name="clientId",
                flags={"read_only": True},
            )
            _element.principal_id = AAZStrType(
                serialized_name="principalId",
                flags={"read_only": True},
            )

            properties = cls._schema_on_200.value.Element.properties
            properties.agent_profile = AAZObjectType(
                serialized_name="agentProfile",
                flags={"required": True},
            )
            properties.dev_center_project_resource_id = AAZStrType(
                serialized_name="devCenterProjectResourceId",
                flags={"required": True},
            )
            properties.fabric_profile = AAZObjectType(
                serialized_name="fabricProfile",
                flags={"required": True},
            )
            properties.maximum_concurrency = AAZIntType(
                serialized_name="maximumConcurrency",
                flags={"required": True},
            )
            properties.organization_profile = AAZObjectType(
                serialized_name="organizationProfile",
                flags={"required": True},
            )
            properties.provisioning_state = AAZStrType(
                serialized_name="provisioningState",
            )

            agent_profile = cls._schema_on_200.value.Element.properties.agent_profile
            agent_profile.kind = AAZStrType(
                flags={"required": True},
            )
            agent_profile.resource_predictions = AAZObjectType(
                serialized_name="resourcePredictions",
            )
            agent_profile.resource_predictions_profile = AAZObjectType(
                serialized_name="resourcePredictionsProfile",
            )

            resource_predictions_profile = cls._schema_on_200.value.Element.properties.agent_profile.resource_predictions_profile
            resource_predictions_profile.kind = AAZStrType(
                flags={"required": True},
            )

            disc_automatic = cls._schema_on_200.value.Element.properties.agent_profile.resource_predictions_profile.discriminate_by("kind", "Automatic")
            disc_automatic.prediction_preference = AAZStrType(
                serialized_name="predictionPreference",
            )

            disc_stateful = cls._schema_on_200.value.Element.properties.agent_profile.discriminate_by("kind", "Stateful")
            disc_stateful.grace_period_time_span = AAZStrType(
                serialized_name="gracePeriodTimeSpan",
            )
            disc_stateful.max_agent_lifetime = AAZStrType(
                serialized_name="maxAgentLifetime",
            )

            fabric_profile = cls._schema_on_200.value.Element.properties.fabric_profile
            fabric_profile.kind = AAZStrType(
                flags={"required": True},
            )

            disc_vmss = cls._schema_on_200.value.Element.properties.fabric_profile.discriminate_by("kind", "Vmss")
            disc_vmss.images = AAZListType(
                flags={"required": True},
            )
            disc_vmss.network_profile = AAZObjectType(
                serialized_name="networkProfile",
            )
            disc_vmss.os_profile = AAZObjectType(
                serialized_name="osProfile",
            )
            disc_vmss.sku = AAZObjectType(
                flags={"required": True},
            )
            disc_vmss.storage_profile = AAZObjectType(
                serialized_name="storageProfile",
            )

            images = cls._schema_on_200.value.Element.properties.fabric_profile.discriminate_by("kind", "Vmss").images
            images.Element = AAZObjectType()

            _element = cls._schema_on_200.value.Element.properties.fabric_profile.discriminate_by("kind", "Vmss").images.Element
            _element.aliases = AAZListType()
            _element.buffer = AAZStrType()
            _element.resource_id = AAZStrType(
                serialized_name="resourceId",
            )
            _element.well_known_image_name = AAZStrType(
                serialized_name="wellKnownImageName",
            )

            aliases = cls._schema_on_200.value.Element.properties.fabric_profile.discriminate_by("kind", "Vmss").images.Element.aliases
            aliases.Element = AAZStrType()

            network_profile = cls._schema_on_200.value.Element.properties.fabric_profile.discriminate_by("kind", "Vmss").network_profile
            network_profile.subnet_id = AAZStrType(
                serialized_name="subnetId",
                flags={"required": True},
            )

            os_profile = cls._schema_on_200.value.Element.properties.fabric_profile.discriminate_by("kind", "Vmss").os_profile
            os_profile.logon_type = AAZStrType(
                serialized_name="logonType",
            )
            os_profile.secrets_management_settings = AAZObjectType(
                serialized_name="secretsManagementSettings",
            )

            secrets_management_settings = cls._schema_on_200.value.Element.properties.fabric_profile.discriminate_by("kind", "Vmss").os_profile.secrets_management_settings
            secrets_management_settings.certificate_store_location = AAZStrType(
                serialized_name="certificateStoreLocation",
            )
            secrets_management_settings.key_exportable = AAZBoolType(
                serialized_name="keyExportable",
                flags={"required": True},
            )
            secrets_management_settings.observed_certificates = AAZListType(
                serialized_name="observedCertificates",
                flags={"required": True},
            )

            observed_certificates = cls._schema_on_200.value.Element.properties.fabric_profile.discriminate_by("kind", "Vmss").os_profile.secrets_management_settings.observed_certificates
            observed_certificates.Element = AAZStrType()

            sku = cls._schema_on_200.value.Element.properties.fabric_profile.discriminate_by("kind", "Vmss").sku
            sku.name = AAZStrType(
                flags={"required": True},
            )

            storage_profile = cls._schema_on_200.value.Element.properties.fabric_profile.discriminate_by("kind", "Vmss").storage_profile
            storage_profile.data_disks = AAZListType(
                serialized_name="dataDisks",
            )
            storage_profile.os_disk_storage_account_type = AAZStrType(
                serialized_name="osDiskStorageAccountType",
            )

            data_disks = cls._schema_on_200.value.Element.properties.fabric_profile.discriminate_by("kind", "Vmss").storage_profile.data_disks
            data_disks.Element = AAZObjectType()

            _element = cls._schema_on_200.value.Element.properties.fabric_profile.discriminate_by("kind", "Vmss").storage_profile.data_disks.Element
            _element.caching = AAZStrType()
            _element.disk_size_gi_b = AAZIntType(
                serialized_name="diskSizeGiB",
            )
            _element.drive_letter = AAZStrType(
                serialized_name="driveLetter",
            )
            _element.storage_account_type = AAZStrType(
                serialized_name="storageAccountType",
            )

            organization_profile = cls._schema_on_200.value.Element.properties.organization_profile
            organization_profile.kind = AAZStrType(
                flags={"required": True},
            )

            disc_azure_dev_ops = cls._schema_on_200.value.Element.properties.organization_profile.discriminate_by("kind", "AzureDevOps")
            disc_azure_dev_ops.organizations = AAZListType(
                flags={"required": True},
            )
            disc_azure_dev_ops.permission_profile = AAZObjectType(
                serialized_name="permissionProfile",
            )

            organizations = cls._schema_on_200.value.Element.properties.organization_profile.discriminate_by("kind", "AzureDevOps").organizations
            organizations.Element = AAZObjectType()

            _element = cls._schema_on_200.value.Element.properties.organization_profile.discriminate_by("kind", "AzureDevOps").organizations.Element
            _element.parallelism = AAZIntType()
            _element.projects = AAZListType()
            _element.url = AAZStrType(
                flags={"required": True},
            )

            projects = cls._schema_on_200.value.Element.properties.organization_profile.discriminate_by("kind", "AzureDevOps").organizations.Element.projects
            projects.Element = AAZStrType()

            permission_profile = cls._schema_on_200.value.Element.properties.organization_profile.discriminate_by("kind", "AzureDevOps").permission_profile
            permission_profile.groups = AAZListType()
            permission_profile.kind = AAZStrType(
                flags={"required": True},
            )
            permission_profile.users = AAZListType()

            groups = cls._schema_on_200.value.Element.properties.organization_profile.discriminate_by("kind", "AzureDevOps").permission_profile.groups
            groups.Element = AAZStrType()

            users = cls._schema_on_200.value.Element.properties.organization_profile.discriminate_by("kind", "AzureDevOps").permission_profile.users
            users.Element = AAZStrType()

            disc_git_hub = cls._schema_on_200.value.Element.properties.organization_profile.discriminate_by("kind", "GitHub")
            disc_git_hub.organizations = AAZListType(
                flags={"required": True},
            )

            organizations = cls._schema_on_200.value.Element.properties.organization_profile.discriminate_by("kind", "GitHub").organizations
            organizations.Element = AAZObjectType()

            _element = cls._schema_on_200.value.Element.properties.organization_profile.discriminate_by("kind", "GitHub").organizations.Element
            _element.repositories = AAZListType()
            _element.url = AAZStrType(
                flags={"required": True},
            )

            repositories = cls._schema_on_200.value.Element.properties.organization_profile.discriminate_by("kind", "GitHub").organizations.Element.repositories
            repositories.Element = AAZStrType()

            system_data = cls._schema_on_200.value.Element.system_data
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

            tags = cls._schema_on_200.value.Element.tags
            tags.Element = AAZStrType()

            return cls._schema_on_200


class _ListHelper:
    """Helper class for List"""


__all__ = ["List"]
