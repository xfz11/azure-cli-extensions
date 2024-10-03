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
    "networkcloud storageappliance update",
    is_preview=True,
)
class Update(AAZCommand):
    """Update properties of the provided storage appliance, or update tags associated with the storage appliance Properties and tag updates can be done independently.

    :example: Patch storage appliance
        az networkcloud storageappliance update --resource-group "resourceGroupName" --storage-appliance-name "storageApplianceName" --serial-number "BM1219XXX" --tags key1="myvalue1" key2="myvalue2"
    """

    _aaz_info = {
        "version": "2024-07-01",
        "resources": [
            ["mgmt-plane", "/subscriptions/{}/resourcegroups/{}/providers/microsoft.networkcloud/storageappliances/{}", "2024-07-01"],
        ]
    }

    AZ_SUPPORT_NO_WAIT = True

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
        _args_schema.storage_appliance_name = AAZStrArg(
            options=["-n", "--name", "--storage-appliance-name"],
            help="The name of the storage appliance.",
            required=True,
            id_part="name",
            fmt=AAZStrArgFormat(
                pattern="^([a-zA-Z0-9][a-zA-Z0-9-_]{0,28}[a-zA-Z0-9])$",
            ),
        )

        # define Arg Group "Properties"

        _args_schema = cls._args_schema
        _args_schema.serial_number = AAZStrArg(
            options=["--serial-number"],
            arg_group="Properties",
            help="The serial number for the storage appliance.",
        )

        # define Arg Group "StorageApplianceUpdateParameters"

        _args_schema = cls._args_schema
        _args_schema.tags = AAZDictArg(
            options=["--tags"],
            arg_group="StorageApplianceUpdateParameters",
            help="The Azure resource tags that will replace the existing ones.",
        )

        tags = cls._args_schema.tags
        tags.Element = AAZStrArg()
        return cls._args_schema

    def _execute_operations(self):
        self.pre_operations()
        yield self.StorageAppliancesUpdate(ctx=self.ctx)()
        self.post_operations()

    @register_callback
    def pre_operations(self):
        pass

    @register_callback
    def post_operations(self):
        pass

    def _output(self, *args, **kwargs):
        result = self.deserialize_output(self.ctx.vars.instance, client_flatten=True)
        return result

    class StorageAppliancesUpdate(AAZHttpOperation):
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
                "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.NetworkCloud/storageAppliances/{storageApplianceName}",
                **self.url_parameters
            )

        @property
        def method(self):
            return "PATCH"

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
                    "storageApplianceName", self.ctx.args.storage_appliance_name,
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
                    "api-version", "2024-07-01",
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
                typ=AAZObjectType,
                typ_kwargs={"flags": {"client_flatten": True}}
            )
            _builder.set_prop("properties", AAZObjectType, typ_kwargs={"flags": {"client_flatten": True}})
            _builder.set_prop("tags", AAZDictType, ".tags")

            properties = _builder.get(".properties")
            if properties is not None:
                properties.set_prop("serialNumber", AAZStrType, ".serial_number")

            tags = _builder.get(".tags")
            if tags is not None:
                tags.set_elements(AAZStrType, ".")

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
            _UpdateHelper._build_schema_storage_appliance_read(cls._schema_on_200)

            return cls._schema_on_200


class _UpdateHelper:
    """Helper class for Update"""

    _schema_storage_appliance_read = None

    @classmethod
    def _build_schema_storage_appliance_read(cls, _schema):
        if cls._schema_storage_appliance_read is not None:
            _schema.extended_location = cls._schema_storage_appliance_read.extended_location
            _schema.id = cls._schema_storage_appliance_read.id
            _schema.location = cls._schema_storage_appliance_read.location
            _schema.name = cls._schema_storage_appliance_read.name
            _schema.properties = cls._schema_storage_appliance_read.properties
            _schema.system_data = cls._schema_storage_appliance_read.system_data
            _schema.tags = cls._schema_storage_appliance_read.tags
            _schema.type = cls._schema_storage_appliance_read.type
            return

        cls._schema_storage_appliance_read = _schema_storage_appliance_read = AAZObjectType()

        storage_appliance_read = _schema_storage_appliance_read
        storage_appliance_read.extended_location = AAZObjectType(
            serialized_name="extendedLocation",
            flags={"required": True},
        )
        storage_appliance_read.id = AAZStrType(
            flags={"read_only": True},
        )
        storage_appliance_read.location = AAZStrType(
            flags={"required": True},
        )
        storage_appliance_read.name = AAZStrType(
            flags={"read_only": True},
        )
        storage_appliance_read.properties = AAZObjectType(
            flags={"required": True, "client_flatten": True},
        )
        storage_appliance_read.system_data = AAZObjectType(
            serialized_name="systemData",
            flags={"read_only": True},
        )
        storage_appliance_read.tags = AAZDictType()
        storage_appliance_read.type = AAZStrType(
            flags={"read_only": True},
        )

        extended_location = _schema_storage_appliance_read.extended_location
        extended_location.name = AAZStrType(
            flags={"required": True},
        )
        extended_location.type = AAZStrType(
            flags={"required": True},
        )

        properties = _schema_storage_appliance_read.properties
        properties.administrator_credentials = AAZObjectType(
            serialized_name="administratorCredentials",
            flags={"required": True},
        )
        properties.capacity = AAZIntType(
            flags={"read_only": True},
        )
        properties.capacity_used = AAZIntType(
            serialized_name="capacityUsed",
            flags={"read_only": True},
        )
        properties.cluster_id = AAZStrType(
            serialized_name="clusterId",
            flags={"read_only": True},
        )
        properties.detailed_status = AAZStrType(
            serialized_name="detailedStatus",
            flags={"read_only": True},
        )
        properties.detailed_status_message = AAZStrType(
            serialized_name="detailedStatusMessage",
            flags={"read_only": True},
        )
        properties.management_ipv4_address = AAZStrType(
            serialized_name="managementIpv4Address",
            flags={"read_only": True},
        )
        properties.manufacturer = AAZStrType(
            flags={"read_only": True},
        )
        properties.model = AAZStrType(
            flags={"read_only": True},
        )
        properties.provisioning_state = AAZStrType(
            serialized_name="provisioningState",
            flags={"read_only": True},
        )
        properties.rack_id = AAZStrType(
            serialized_name="rackId",
            flags={"required": True},
        )
        properties.rack_slot = AAZIntType(
            serialized_name="rackSlot",
            flags={"required": True},
        )
        properties.remote_vendor_management_feature = AAZStrType(
            serialized_name="remoteVendorManagementFeature",
            flags={"read_only": True},
        )
        properties.remote_vendor_management_status = AAZStrType(
            serialized_name="remoteVendorManagementStatus",
            flags={"read_only": True},
        )
        properties.secret_rotation_status = AAZListType(
            serialized_name="secretRotationStatus",
            flags={"read_only": True},
        )
        properties.serial_number = AAZStrType(
            serialized_name="serialNumber",
            flags={"required": True},
        )
        properties.storage_appliance_sku_id = AAZStrType(
            serialized_name="storageApplianceSkuId",
            flags={"required": True},
        )
        properties.version = AAZStrType(
            flags={"read_only": True},
        )

        administrator_credentials = _schema_storage_appliance_read.properties.administrator_credentials
        administrator_credentials.password = AAZStrType(
            flags={"secret": True},
        )
        administrator_credentials.username = AAZStrType(
            flags={"required": True},
        )

        secret_rotation_status = _schema_storage_appliance_read.properties.secret_rotation_status
        secret_rotation_status.Element = AAZObjectType()

        _element = _schema_storage_appliance_read.properties.secret_rotation_status.Element
        _element.expire_period_days = AAZIntType(
            serialized_name="expirePeriodDays",
            flags={"read_only": True},
        )
        _element.last_rotation_time = AAZStrType(
            serialized_name="lastRotationTime",
            flags={"read_only": True},
        )
        _element.rotation_period_days = AAZIntType(
            serialized_name="rotationPeriodDays",
            flags={"read_only": True},
        )
        _element.secret_archive_reference = AAZObjectType(
            serialized_name="secretArchiveReference",
            flags={"read_only": True},
        )
        _element.secret_type = AAZStrType(
            serialized_name="secretType",
            flags={"read_only": True},
        )

        secret_archive_reference = _schema_storage_appliance_read.properties.secret_rotation_status.Element.secret_archive_reference
        secret_archive_reference.key_vault_id = AAZStrType(
            serialized_name="keyVaultId",
            flags={"read_only": True},
        )
        secret_archive_reference.secret_name = AAZStrType(
            serialized_name="secretName",
            flags={"read_only": True},
        )
        secret_archive_reference.secret_version = AAZStrType(
            serialized_name="secretVersion",
            flags={"read_only": True},
        )

        system_data = _schema_storage_appliance_read.system_data
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

        tags = _schema_storage_appliance_read.tags
        tags.Element = AAZStrType()

        _schema.extended_location = cls._schema_storage_appliance_read.extended_location
        _schema.id = cls._schema_storage_appliance_read.id
        _schema.location = cls._schema_storage_appliance_read.location
        _schema.name = cls._schema_storage_appliance_read.name
        _schema.properties = cls._schema_storage_appliance_read.properties
        _schema.system_data = cls._schema_storage_appliance_read.system_data
        _schema.tags = cls._schema_storage_appliance_read.tags
        _schema.type = cls._schema_storage_appliance_read.type


__all__ = ["Update"]
