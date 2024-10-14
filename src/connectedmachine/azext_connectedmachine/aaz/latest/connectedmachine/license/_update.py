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
    "connectedmachine license update",
)
class Update(AAZCommand):
    """Update operation to update a license.

    :example: Sample command for license update
        az connectedmachine license create --name licenseName --resource-group myResourceGroup --location 'eastus2euap' --license-type 'ESU' --state 'Deactivated' --target 'Windows Server 2012' --edition 'Datacenter' --type 'pCore' --processors 16 --subscription mySubscription
    """

    _aaz_info = {
        "version": "2024-07-10",
        "resources": [
            ["mgmt-plane", "/subscriptions/{}/resourcegroups/{}/providers/microsoft.hybridcompute/licenses/{}", "2024-07-10"],
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
        _args_schema.license_name = AAZStrArg(
            options=["-n", "--name", "--license-name"],
            help="The name of the license.",
            required=True,
            id_part="name",
            fmt=AAZStrArgFormat(
                pattern="[a-zA-Z0-9-_\.]+",
            ),
        )
        _args_schema.resource_group = AAZResourceGroupNameArg(
            required=True,
        )

        # define Arg Group "LicenseDetails"

        _args_schema = cls._args_schema
        _args_schema.edition = AAZStrArg(
            options=["--edition"],
            arg_group="LicenseDetails",
            help="Describes the edition of the license. The values are either Standard or Datacenter.",
            nullable=True,
            enum={"Datacenter": "Datacenter", "Standard": "Standard"},
        )
        _args_schema.processors = AAZIntArg(
            options=["--processors"],
            arg_group="LicenseDetails",
            help="Describes the number of processors.",
            nullable=True,
        )
        _args_schema.state = AAZStrArg(
            options=["--state"],
            arg_group="LicenseDetails",
            help="Describes the state of the license.",
            nullable=True,
            enum={"Activated": "Activated", "Deactivated": "Deactivated"},
        )
        _args_schema.target = AAZStrArg(
            options=["--target"],
            arg_group="LicenseDetails",
            help="Describes the license target server.",
            nullable=True,
            enum={"Windows Server 2012": "Windows Server 2012", "Windows Server 2012 R2": "Windows Server 2012 R2"},
        )
        _args_schema.type = AAZStrArg(
            options=["--type"],
            arg_group="LicenseDetails",
            help="Describes the license core type (pCore or vCore).",
            nullable=True,
            enum={"pCore": "pCore", "vCore": "vCore"},
        )
        _args_schema.volume_license_details = AAZListArg(
            options=["--volume-license-details"],
            arg_group="LicenseDetails",
            help="A list of volume license details.",
            nullable=True,
        )

        volume_license_details = cls._args_schema.volume_license_details
        volume_license_details.Element = AAZObjectArg(
            nullable=True,
        )

        _element = cls._args_schema.volume_license_details.Element
        _element.invoice_id = AAZStrArg(
            options=["invoice-id"],
            help="The invoice id for the volume license.",
            nullable=True,
        )
        _element.program_year = AAZStrArg(
            options=["program-year"],
            help="Describes the program year the volume license is for.",
            nullable=True,
            enum={"Year 1": "Year 1", "Year 2": "Year 2", "Year 3": "Year 3"},
        )

        # define Arg Group "Parameters"

        _args_schema = cls._args_schema
        _args_schema.tags = AAZDictArg(
            options=["--tags"],
            arg_group="Parameters",
            help="Resource tags.",
            nullable=True,
        )

        tags = cls._args_schema.tags
        tags.Element = AAZStrArg(
            nullable=True,
        )

        # define Arg Group "Properties"

        _args_schema = cls._args_schema
        _args_schema.license_type = AAZStrArg(
            options=["--license-type"],
            arg_group="Properties",
            help="The type of the license resource.",
            nullable=True,
            enum={"ESU": "ESU"},
        )
        _args_schema.tenant_id = AAZStrArg(
            options=["--tenant-id"],
            arg_group="Properties",
            help="Describes the tenant id.",
            nullable=True,
        )
        return cls._args_schema

    def _execute_operations(self):
        self.pre_operations()
        self.LicensesGet(ctx=self.ctx)()
        self.pre_instance_update(self.ctx.vars.instance)
        self.InstanceUpdateByJson(ctx=self.ctx)()
        self.InstanceUpdateByGeneric(ctx=self.ctx)()
        self.post_instance_update(self.ctx.vars.instance)
        yield self.LicensesCreateOrUpdate(ctx=self.ctx)()
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

    class LicensesGet(AAZHttpOperation):
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
                "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HybridCompute/licenses/{licenseName}",
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
                    "licenseName", self.ctx.args.license_name,
                    required=True,
                ),
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
                    "api-version", "2024-07-10",
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
            _UpdateHelper._build_schema_license_read(cls._schema_on_200)

            return cls._schema_on_200

    class LicensesCreateOrUpdate(AAZHttpOperation):
        CLIENT_TYPE = "MgmtClient"

        def __call__(self, *args, **kwargs):
            request = self.make_request()
            session = self.client.send_request(request=request, stream=False, **kwargs)
            if session.http_response.status_code in [202]:
                return self.client.build_lro_polling(
                    self.ctx.args.no_wait,
                    session,
                    self.on_200,
                    self.on_error,
                    lro_options={"final-state-via": "azure-async-operation"},
                    path_format_arguments=self.url_parameters,
                )
            if session.http_response.status_code in [200]:
                return self.client.build_lro_polling(
                    self.ctx.args.no_wait,
                    session,
                    self.on_200,
                    self.on_error,
                    lro_options={"final-state-via": "azure-async-operation"},
                    path_format_arguments=self.url_parameters,
                )

            return self.on_error(session.http_response)

        @property
        def url(self):
            return self.client.format_url(
                "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.HybridCompute/licenses/{licenseName}",
                **self.url_parameters
            )

        @property
        def method(self):
            return "PUT"

        @property
        def error_format(self):
            return "MgmtErrorFormat"

        @property
        def url_parameters(self):
            parameters = {
                **self.serialize_url_param(
                    "licenseName", self.ctx.args.license_name,
                    required=True,
                ),
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
                    "api-version", "2024-07-10",
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
            _UpdateHelper._build_schema_license_read(cls._schema_on_200)

            return cls._schema_on_200

    class InstanceUpdateByJson(AAZJsonInstanceUpdateOperation):

        def __call__(self, *args, **kwargs):
            self._update_instance(self.ctx.vars.instance)

        def _update_instance(self, instance):
            _instance_value, _builder = self.new_content_builder(
                self.ctx.args,
                value=instance,
                typ=AAZObjectType
            )
            _builder.set_prop("properties", AAZObjectType, typ_kwargs={"flags": {"client_flatten": True}})
            _builder.set_prop("tags", AAZDictType, ".tags")

            properties = _builder.get(".properties")
            if properties is not None:
                properties.set_prop("licenseDetails", AAZObjectType)
                properties.set_prop("licenseType", AAZStrType, ".license_type")
                properties.set_prop("tenantId", AAZStrType, ".tenant_id")

            license_details = _builder.get(".properties.licenseDetails")
            if license_details is not None:
                license_details.set_prop("edition", AAZStrType, ".edition")
                license_details.set_prop("processors", AAZIntType, ".processors")
                license_details.set_prop("state", AAZStrType, ".state")
                license_details.set_prop("target", AAZStrType, ".target")
                license_details.set_prop("type", AAZStrType, ".type")
                license_details.set_prop("volumeLicenseDetails", AAZListType, ".volume_license_details")

            volume_license_details = _builder.get(".properties.licenseDetails.volumeLicenseDetails")
            if volume_license_details is not None:
                volume_license_details.set_elements(AAZObjectType, ".")

            _elements = _builder.get(".properties.licenseDetails.volumeLicenseDetails[]")
            if _elements is not None:
                _elements.set_prop("invoiceId", AAZStrType, ".invoice_id")
                _elements.set_prop("programYear", AAZStrType, ".program_year")

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

    _schema_license_read = None

    @classmethod
    def _build_schema_license_read(cls, _schema):
        if cls._schema_license_read is not None:
            _schema.id = cls._schema_license_read.id
            _schema.location = cls._schema_license_read.location
            _schema.name = cls._schema_license_read.name
            _schema.properties = cls._schema_license_read.properties
            _schema.system_data = cls._schema_license_read.system_data
            _schema.tags = cls._schema_license_read.tags
            _schema.type = cls._schema_license_read.type
            return

        cls._schema_license_read = _schema_license_read = AAZObjectType()

        license_read = _schema_license_read
        license_read.id = AAZStrType(
            flags={"read_only": True},
        )
        license_read.location = AAZStrType(
            flags={"required": True},
        )
        license_read.name = AAZStrType(
            flags={"read_only": True},
        )
        license_read.properties = AAZObjectType(
            flags={"client_flatten": True},
        )
        license_read.system_data = AAZObjectType(
            serialized_name="systemData",
            flags={"read_only": True},
        )
        license_read.tags = AAZDictType()
        license_read.type = AAZStrType(
            flags={"read_only": True},
        )

        properties = _schema_license_read.properties
        properties.license_details = AAZObjectType(
            serialized_name="licenseDetails",
        )
        properties.license_type = AAZStrType(
            serialized_name="licenseType",
        )
        properties.provisioning_state = AAZStrType(
            serialized_name="provisioningState",
            flags={"read_only": True},
        )
        properties.tenant_id = AAZStrType(
            serialized_name="tenantId",
        )

        license_details = _schema_license_read.properties.license_details
        license_details.assigned_licenses = AAZIntType(
            serialized_name="assignedLicenses",
            flags={"read_only": True},
        )
        license_details.edition = AAZStrType()
        license_details.immutable_id = AAZStrType(
            serialized_name="immutableId",
            flags={"read_only": True},
        )
        license_details.processors = AAZIntType()
        license_details.state = AAZStrType()
        license_details.target = AAZStrType()
        license_details.type = AAZStrType()
        license_details.volume_license_details = AAZListType(
            serialized_name="volumeLicenseDetails",
        )

        volume_license_details = _schema_license_read.properties.license_details.volume_license_details
        volume_license_details.Element = AAZObjectType()

        _element = _schema_license_read.properties.license_details.volume_license_details.Element
        _element.invoice_id = AAZStrType(
            serialized_name="invoiceId",
        )
        _element.program_year = AAZStrType(
            serialized_name="programYear",
        )

        system_data = _schema_license_read.system_data
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

        tags = _schema_license_read.tags
        tags.Element = AAZStrType()

        _schema.id = cls._schema_license_read.id
        _schema.location = cls._schema_license_read.location
        _schema.name = cls._schema_license_read.name
        _schema.properties = cls._schema_license_read.properties
        _schema.system_data = cls._schema_license_read.system_data
        _schema.tags = cls._schema_license_read.tags
        _schema.type = cls._schema_license_read.type


__all__ = ["Update"]
