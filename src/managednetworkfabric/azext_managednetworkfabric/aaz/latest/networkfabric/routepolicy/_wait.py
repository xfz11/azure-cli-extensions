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
    "networkfabric routepolicy wait",
)
class Wait(AAZWaitCommand):
    """Place the CLI in a waiting state until a condition is met.
    """

    _aaz_info = {
        "resources": [
            ["mgmt-plane", "/subscriptions/{}/resourcegroups/{}/providers/microsoft.managednetworkfabric/routepolicies/{}", "2023-06-15"],
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
        _args_schema.resource_group = AAZResourceGroupNameArg(
            help="Name of the resource group",
            required=True,
        )
        _args_schema.resource_name = AAZStrArg(
            options=["--resource-name"],
            help="Name of the Route Policy.",
            required=True,
            id_part="name",
        )
        return cls._args_schema

    def _execute_operations(self):
        self.pre_operations()
        self.RoutePoliciesGet(ctx=self.ctx)()
        self.post_operations()

    @register_callback
    def pre_operations(self):
        pass

    @register_callback
    def post_operations(self):
        pass

    def _output(self, *args, **kwargs):
        result = self.deserialize_output(self.ctx.vars.instance, client_flatten=False)
        return result

    class RoutePoliciesGet(AAZHttpOperation):
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
                "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedNetworkFabric/routePolicies/{routePolicyName}",
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
                    "routePolicyName", self.ctx.args.resource_name,
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
                    "api-version", "2023-06-15",
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
            _schema_on_200.location = AAZStrType(
                flags={"required": True},
            )
            _schema_on_200.name = AAZStrType(
                flags={"read_only": True},
            )
            _schema_on_200.properties = AAZObjectType(
                flags={"required": True, "client_flatten": True},
            )
            _schema_on_200.system_data = AAZObjectType(
                serialized_name="systemData",
                flags={"read_only": True},
            )
            _schema_on_200.tags = AAZDictType()
            _schema_on_200.type = AAZStrType(
                flags={"read_only": True},
            )

            properties = cls._schema_on_200.properties
            properties.address_family_type = AAZStrType(
                serialized_name="addressFamilyType",
            )
            properties.administrative_state = AAZStrType(
                serialized_name="administrativeState",
                flags={"read_only": True},
            )
            properties.annotation = AAZStrType()
            properties.configuration_state = AAZStrType(
                serialized_name="configurationState",
                flags={"read_only": True},
            )
            properties.default_action = AAZStrType(
                serialized_name="defaultAction",
            )
            properties.network_fabric_id = AAZStrType(
                serialized_name="networkFabricId",
                flags={"required": True},
            )
            properties.provisioning_state = AAZStrType(
                serialized_name="provisioningState",
                flags={"read_only": True},
            )
            properties.statements = AAZListType(
                flags={"required": True},
            )

            statements = cls._schema_on_200.properties.statements
            statements.Element = AAZObjectType()

            _element = cls._schema_on_200.properties.statements.Element
            _element.action = AAZObjectType(
                flags={"required": True},
            )
            _element.annotation = AAZStrType()
            _element.condition = AAZObjectType(
                flags={"required": True},
            )
            _element.sequence_number = AAZIntType(
                serialized_name="sequenceNumber",
                flags={"required": True},
            )

            action = cls._schema_on_200.properties.statements.Element.action
            action.action_type = AAZStrType(
                serialized_name="actionType",
                flags={"required": True},
            )
            action.ip_community_properties = AAZObjectType(
                serialized_name="ipCommunityProperties",
            )
            action.ip_extended_community_properties = AAZObjectType(
                serialized_name="ipExtendedCommunityProperties",
            )
            action.local_preference = AAZIntType(
                serialized_name="localPreference",
            )

            ip_community_properties = cls._schema_on_200.properties.statements.Element.action.ip_community_properties
            ip_community_properties.add = AAZObjectType()
            _WaitHelper._build_schema_ip_community_id_list_read(ip_community_properties.add)
            ip_community_properties.delete = AAZObjectType()
            _WaitHelper._build_schema_ip_community_id_list_read(ip_community_properties.delete)
            ip_community_properties.set = AAZObjectType()
            _WaitHelper._build_schema_ip_community_id_list_read(ip_community_properties.set)

            ip_extended_community_properties = cls._schema_on_200.properties.statements.Element.action.ip_extended_community_properties
            ip_extended_community_properties.add = AAZObjectType()
            _WaitHelper._build_schema_ip_extended_community_id_list_read(ip_extended_community_properties.add)
            ip_extended_community_properties.delete = AAZObjectType()
            _WaitHelper._build_schema_ip_extended_community_id_list_read(ip_extended_community_properties.delete)
            ip_extended_community_properties.set = AAZObjectType()
            _WaitHelper._build_schema_ip_extended_community_id_list_read(ip_extended_community_properties.set)

            condition = cls._schema_on_200.properties.statements.Element.condition
            condition.ip_community_ids = AAZListType(
                serialized_name="ipCommunityIds",
            )
            condition.ip_extended_community_ids = AAZListType(
                serialized_name="ipExtendedCommunityIds",
            )
            condition.ip_prefix_id = AAZStrType(
                serialized_name="ipPrefixId",
            )
            condition.type = AAZStrType()

            ip_community_ids = cls._schema_on_200.properties.statements.Element.condition.ip_community_ids
            ip_community_ids.Element = AAZStrType()

            ip_extended_community_ids = cls._schema_on_200.properties.statements.Element.condition.ip_extended_community_ids
            ip_extended_community_ids.Element = AAZStrType()

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

            tags = cls._schema_on_200.tags
            tags.Element = AAZStrType()

            return cls._schema_on_200


class _WaitHelper:
    """Helper class for Wait"""

    _schema_ip_community_id_list_read = None

    @classmethod
    def _build_schema_ip_community_id_list_read(cls, _schema):
        if cls._schema_ip_community_id_list_read is not None:
            _schema.ip_community_ids = cls._schema_ip_community_id_list_read.ip_community_ids
            return

        cls._schema_ip_community_id_list_read = _schema_ip_community_id_list_read = AAZObjectType()

        ip_community_id_list_read = _schema_ip_community_id_list_read
        ip_community_id_list_read.ip_community_ids = AAZListType(
            serialized_name="ipCommunityIds",
        )

        ip_community_ids = _schema_ip_community_id_list_read.ip_community_ids
        ip_community_ids.Element = AAZStrType()

        _schema.ip_community_ids = cls._schema_ip_community_id_list_read.ip_community_ids

    _schema_ip_extended_community_id_list_read = None

    @classmethod
    def _build_schema_ip_extended_community_id_list_read(cls, _schema):
        if cls._schema_ip_extended_community_id_list_read is not None:
            _schema.ip_extended_community_ids = cls._schema_ip_extended_community_id_list_read.ip_extended_community_ids
            return

        cls._schema_ip_extended_community_id_list_read = _schema_ip_extended_community_id_list_read = AAZObjectType()

        ip_extended_community_id_list_read = _schema_ip_extended_community_id_list_read
        ip_extended_community_id_list_read.ip_extended_community_ids = AAZListType(
            serialized_name="ipExtendedCommunityIds",
        )

        ip_extended_community_ids = _schema_ip_extended_community_id_list_read.ip_extended_community_ids
        ip_extended_community_ids.Element = AAZStrType()

        _schema.ip_extended_community_ids = cls._schema_ip_extended_community_id_list_read.ip_extended_community_ids


__all__ = ["Wait"]
