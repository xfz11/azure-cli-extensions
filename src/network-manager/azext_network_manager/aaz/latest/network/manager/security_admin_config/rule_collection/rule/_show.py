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
    "network manager security-admin-config rule-collection rule show",
)
class Show(AAZCommand):
    """Get a network manager security configuration admin rule.

    :example: Get security admin rule
        az network manager security-admin-config rule-collection rule show --configuration-name "myTestSecurityConfig" --network-manager-name "testNetworkManager" --resource-group "rg1" --rule-collection-name "myTestCollection" --rule-name "SampleAdminRule"
    """

    _aaz_info = {
        "version": "2024-05-01",
        "resources": [
            ["mgmt-plane", "/subscriptions/{}/resourcegroups/{}/providers/microsoft.network/networkmanagers/{}/securityadminconfigurations/{}/rulecollections/{}/rules/{}", "2024-05-01"],
        ]
    }

    def _handler(self, command_args):
        super()._handler(command_args)
        self._execute_operations()
        return self._output()

    _args_schema = None

    @classmethod
    def _build_arguments_schema(cls, *args, **kwargs):
        if cls._args_schema is not None:
            return cls._args_schema
        cls._args_schema = super()._build_arguments_schema(*args, **kwargs)

        # define Arg Group ""

        _args_schema = cls._args_schema
        _args_schema.configuration_name = AAZStrArg(
            options=["--config", "--config-name", "--configuration-name"],
            help="Name of the network manager security configuration.",
            required=True,
            id_part="child_name_1",
        )
        _args_schema.network_manager_name = AAZStrArg(
            options=["-n", "--name", "--network-manager-name"],
            help="The name of the network manager.",
            required=True,
            id_part="name",
            fmt=AAZStrArgFormat(
                pattern="^[0-9a-zA-Z]([0-9a-zA-Z_.-]{0,62}[0-9a-zA-Z_])?$",
            ),
        )
        _args_schema.resource_group = AAZResourceGroupNameArg(
            required=True,
        )
        _args_schema.rule_collection_name = AAZStrArg(
            options=["--rc", "--rule-collection-name"],
            help="The name of the network manager security Configuration rule collection.",
            required=True,
            id_part="child_name_2",
        )
        _args_schema.rule_name = AAZStrArg(
            options=["--rule-name"],
            help="The name of the rule.",
            required=True,
            id_part="child_name_3",
        )
        return cls._args_schema

    def _execute_operations(self):
        self.pre_operations()
        self.AdminRulesGet(ctx=self.ctx)()
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

    class AdminRulesGet(AAZHttpOperation):
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
                "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/networkManagers/{networkManagerName}/securityAdminConfigurations/{configurationName}/ruleCollections/{ruleCollectionName}/rules/{ruleName}",
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
                    "configurationName", self.ctx.args.configuration_name,
                    required=True,
                ),
                **self.serialize_url_param(
                    "networkManagerName", self.ctx.args.network_manager_name,
                    required=True,
                ),
                **self.serialize_url_param(
                    "resourceGroupName", self.ctx.args.resource_group,
                    required=True,
                ),
                **self.serialize_url_param(
                    "ruleCollectionName", self.ctx.args.rule_collection_name,
                    required=True,
                ),
                **self.serialize_url_param(
                    "ruleName", self.ctx.args.rule_name,
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
                    "api-version", "2024-05-01",
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
            _schema_on_200.id = AAZStrType(
                flags={"read_only": True},
            )
            _schema_on_200.kind = AAZStrType(
                flags={"required": True},
            )
            _schema_on_200.name = AAZStrType(
                flags={"read_only": True},
            )
            _schema_on_200.system_data = AAZObjectType(
                serialized_name="systemData",
                flags={"read_only": True},
            )
            _schema_on_200.type = AAZStrType(
                flags={"read_only": True},
            )

            system_data = cls._schema_on_200.system_data
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

            disc_custom = cls._schema_on_200.discriminate_by("kind", "Custom")
            disc_custom.properties = AAZObjectType(
                flags={"client_flatten": True},
            )

            properties = cls._schema_on_200.discriminate_by("kind", "Custom").properties
            properties.access = AAZStrType(
                flags={"required": True},
            )
            properties.description = AAZStrType()
            properties.destination_port_ranges = AAZListType(
                serialized_name="destinationPortRanges",
            )
            properties.destinations = AAZListType()
            properties.direction = AAZStrType(
                flags={"required": True},
            )
            properties.priority = AAZIntType(
                flags={"required": True},
            )
            properties.protocol = AAZStrType(
                flags={"required": True},
            )
            properties.provisioning_state = AAZStrType(
                serialized_name="provisioningState",
                flags={"read_only": True},
            )
            properties.resource_guid = AAZStrType(
                serialized_name="resourceGuid",
                flags={"read_only": True},
            )
            properties.source_port_ranges = AAZListType(
                serialized_name="sourcePortRanges",
            )
            properties.sources = AAZListType()

            destination_port_ranges = cls._schema_on_200.discriminate_by("kind", "Custom").properties.destination_port_ranges
            destination_port_ranges.Element = AAZStrType()

            destinations = cls._schema_on_200.discriminate_by("kind", "Custom").properties.destinations
            destinations.Element = AAZObjectType()
            _ShowHelper._build_schema_address_prefix_item_read(destinations.Element)

            source_port_ranges = cls._schema_on_200.discriminate_by("kind", "Custom").properties.source_port_ranges
            source_port_ranges.Element = AAZStrType()

            sources = cls._schema_on_200.discriminate_by("kind", "Custom").properties.sources
            sources.Element = AAZObjectType()
            _ShowHelper._build_schema_address_prefix_item_read(sources.Element)

            disc_default = cls._schema_on_200.discriminate_by("kind", "Default")
            disc_default.properties = AAZObjectType(
                flags={"client_flatten": True},
            )

            properties = cls._schema_on_200.discriminate_by("kind", "Default").properties
            properties.access = AAZStrType(
                flags={"read_only": True},
            )
            properties.description = AAZStrType(
                flags={"read_only": True},
            )
            properties.destination_port_ranges = AAZListType(
                serialized_name="destinationPortRanges",
                flags={"read_only": True},
            )
            properties.destinations = AAZListType(
                flags={"read_only": True},
            )
            properties.direction = AAZStrType(
                flags={"read_only": True},
            )
            properties.flag = AAZStrType()
            properties.priority = AAZIntType(
                flags={"read_only": True},
            )
            properties.protocol = AAZStrType(
                flags={"read_only": True},
            )
            properties.provisioning_state = AAZStrType(
                serialized_name="provisioningState",
                flags={"read_only": True},
            )
            properties.resource_guid = AAZStrType(
                serialized_name="resourceGuid",
                flags={"read_only": True},
            )
            properties.source_port_ranges = AAZListType(
                serialized_name="sourcePortRanges",
                flags={"read_only": True},
            )
            properties.sources = AAZListType(
                flags={"read_only": True},
            )

            destination_port_ranges = cls._schema_on_200.discriminate_by("kind", "Default").properties.destination_port_ranges
            destination_port_ranges.Element = AAZStrType()

            destinations = cls._schema_on_200.discriminate_by("kind", "Default").properties.destinations
            destinations.Element = AAZObjectType()
            _ShowHelper._build_schema_address_prefix_item_read(destinations.Element)

            source_port_ranges = cls._schema_on_200.discriminate_by("kind", "Default").properties.source_port_ranges
            source_port_ranges.Element = AAZStrType()

            sources = cls._schema_on_200.discriminate_by("kind", "Default").properties.sources
            sources.Element = AAZObjectType()
            _ShowHelper._build_schema_address_prefix_item_read(sources.Element)

            return cls._schema_on_200


class _ShowHelper:
    """Helper class for Show"""

    _schema_address_prefix_item_read = None

    @classmethod
    def _build_schema_address_prefix_item_read(cls, _schema):
        if cls._schema_address_prefix_item_read is not None:
            _schema.address_prefix = cls._schema_address_prefix_item_read.address_prefix
            _schema.address_prefix_type = cls._schema_address_prefix_item_read.address_prefix_type
            return

        cls._schema_address_prefix_item_read = _schema_address_prefix_item_read = AAZObjectType()

        address_prefix_item_read = _schema_address_prefix_item_read
        address_prefix_item_read.address_prefix = AAZStrType(
            serialized_name="addressPrefix",
        )
        address_prefix_item_read.address_prefix_type = AAZStrType(
            serialized_name="addressPrefixType",
        )

        _schema.address_prefix = cls._schema_address_prefix_item_read.address_prefix
        _schema.address_prefix_type = cls._schema_address_prefix_item_read.address_prefix_type


__all__ = ["Show"]
