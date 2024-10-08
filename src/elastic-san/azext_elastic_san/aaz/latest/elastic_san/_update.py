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
    "elastic-san update",
)
class Update(AAZCommand):
    """Update an Elastic SAN.

    :example: Update an Elastic SAN.
        az elastic-san update -n "san_name" -g "rg" --tags '{key1710:bbbb}' --base-size-tib 25 --extended-capacity-size-tib 15
    """

    _aaz_info = {
        "version": "2024-05-01",
        "resources": [
            ["mgmt-plane", "/subscriptions/{}/resourcegroups/{}/providers/microsoft.elasticsan/elasticsans/{}", "2024-05-01"],
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
        _args_schema.elastic_san_name = AAZStrArg(
            options=["-n", "--name", "--elastic-san-name"],
            help="The name of the ElasticSan.",
            required=True,
            id_part="name",
            fmt=AAZStrArgFormat(
                pattern="^[A-Za-z0-9]+((-|_)[a-z0-9A-Z]+)*$",
                max_length=24,
                min_length=3,
            ),
        )
        _args_schema.resource_group = AAZResourceGroupNameArg(
            required=True,
        )

        # define Arg Group "Parameters"

        _args_schema = cls._args_schema
        _args_schema.tags = AAZDictArg(
            options=["--tags"],
            arg_group="Parameters",
            help="Azure resource tags.",
            nullable=True,
        )

        tags = cls._args_schema.tags
        tags.Element = AAZStrArg(
            nullable=True,
        )

        # define Arg Group "Properties"

        _args_schema = cls._args_schema
        _args_schema.availability_zones = AAZListArg(
            options=["--availability-zones"],
            arg_group="Properties",
            help="Logical zone for Elastic San resource; example: [\"1\"].",
            nullable=True,
        )
        _args_schema.base_size_tib = AAZIntArg(
            options=["--base-size-tib"],
            arg_group="Properties",
            help="Base size of the Elastic San appliance in TiB.",
        )
        _args_schema.extended_capacity_size_tib = AAZIntArg(
            options=["--extended-size", "--extended-capacity-size-tib"],
            arg_group="Properties",
            help="Extended size of the Elastic San appliance in TiB.",
        )
        _args_schema.public_network_access = AAZStrArg(
            options=["--public-network-access"],
            arg_group="Properties",
            help="Allow or disallow public network access to ElasticSan. Value is optional but if passed in, must be 'Enabled' or 'Disabled'.",
            nullable=True,
            enum={"Disabled": "Disabled", "Enabled": "Enabled"},
        )
        _args_schema.sku = AAZObjectArg(
            options=["--sku"],
            arg_group="Properties",
            help="resource sku",
        )

        availability_zones = cls._args_schema.availability_zones
        availability_zones.Element = AAZStrArg(
            nullable=True,
        )

        sku = cls._args_schema.sku
        sku.name = AAZStrArg(
            options=["name"],
            help="The sku name.",
            enum={"Premium_LRS": "Premium_LRS", "Premium_ZRS": "Premium_ZRS"},
        )
        sku.tier = AAZStrArg(
            options=["tier"],
            help="The sku tier.",
            nullable=True,
            enum={"Premium": "Premium"},
        )
        return cls._args_schema

    def _execute_operations(self):
        self.pre_operations()
        self.ElasticSansGet(ctx=self.ctx)()
        self.pre_instance_update(self.ctx.vars.instance)
        self.InstanceUpdateByJson(ctx=self.ctx)()
        self.InstanceUpdateByGeneric(ctx=self.ctx)()
        self.post_instance_update(self.ctx.vars.instance)
        yield self.ElasticSansCreate(ctx=self.ctx)()
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

    class ElasticSansGet(AAZHttpOperation):
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
                "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ElasticSan/elasticSans/{elasticSanName}",
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
                    "elasticSanName", self.ctx.args.elastic_san_name,
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
            _UpdateHelper._build_schema_elastic_san_read(cls._schema_on_200)

            return cls._schema_on_200

    class ElasticSansCreate(AAZHttpOperation):
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
                    lro_options={"final-state-via": "location"},
                    path_format_arguments=self.url_parameters,
                )
            if session.http_response.status_code in [200, 201]:
                return self.client.build_lro_polling(
                    self.ctx.args.no_wait,
                    session,
                    self.on_200_201,
                    self.on_error,
                    lro_options={"final-state-via": "location"},
                    path_format_arguments=self.url_parameters,
                )

            return self.on_error(session.http_response)

        @property
        def url(self):
            return self.client.format_url(
                "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ElasticSan/elasticSans/{elasticSanName}",
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
                    "elasticSanName", self.ctx.args.elastic_san_name,
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
                    "api-version", "2024-05-01",
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
            _UpdateHelper._build_schema_elastic_san_read(cls._schema_on_200_201)

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
            _builder.set_prop("tags", AAZDictType, ".tags")

            properties = _builder.get(".properties")
            if properties is not None:
                properties.set_prop("availabilityZones", AAZListType, ".availability_zones")
                properties.set_prop("baseSizeTiB", AAZIntType, ".base_size_tib", typ_kwargs={"flags": {"required": True}})
                properties.set_prop("extendedCapacitySizeTiB", AAZIntType, ".extended_capacity_size_tib", typ_kwargs={"flags": {"required": True}})
                properties.set_prop("publicNetworkAccess", AAZStrType, ".public_network_access")
                properties.set_prop("sku", AAZObjectType, ".sku", typ_kwargs={"flags": {"required": True}})

            availability_zones = _builder.get(".properties.availabilityZones")
            if availability_zones is not None:
                availability_zones.set_elements(AAZStrType, ".")

            sku = _builder.get(".properties.sku")
            if sku is not None:
                sku.set_prop("name", AAZStrType, ".name", typ_kwargs={"flags": {"required": True}})
                sku.set_prop("tier", AAZStrType, ".tier")

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

    _schema_elastic_san_read = None

    @classmethod
    def _build_schema_elastic_san_read(cls, _schema):
        if cls._schema_elastic_san_read is not None:
            _schema.id = cls._schema_elastic_san_read.id
            _schema.location = cls._schema_elastic_san_read.location
            _schema.name = cls._schema_elastic_san_read.name
            _schema.properties = cls._schema_elastic_san_read.properties
            _schema.system_data = cls._schema_elastic_san_read.system_data
            _schema.tags = cls._schema_elastic_san_read.tags
            _schema.type = cls._schema_elastic_san_read.type
            return

        cls._schema_elastic_san_read = _schema_elastic_san_read = AAZObjectType()

        elastic_san_read = _schema_elastic_san_read
        elastic_san_read.id = AAZStrType(
            flags={"read_only": True},
        )
        elastic_san_read.location = AAZStrType(
            flags={"required": True},
        )
        elastic_san_read.name = AAZStrType(
            flags={"read_only": True},
        )
        elastic_san_read.properties = AAZObjectType(
            flags={"required": True, "client_flatten": True},
        )
        elastic_san_read.system_data = AAZObjectType(
            serialized_name="systemData",
            flags={"read_only": True},
        )
        cls._build_schema_system_data_read(elastic_san_read.system_data)
        elastic_san_read.tags = AAZDictType()
        elastic_san_read.type = AAZStrType(
            flags={"read_only": True},
        )

        properties = _schema_elastic_san_read.properties
        properties.availability_zones = AAZListType(
            serialized_name="availabilityZones",
        )
        properties.base_size_ti_b = AAZIntType(
            serialized_name="baseSizeTiB",
            flags={"required": True},
        )
        properties.extended_capacity_size_ti_b = AAZIntType(
            serialized_name="extendedCapacitySizeTiB",
            flags={"required": True},
        )
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
        properties.sku = AAZObjectType(
            flags={"required": True},
        )
        properties.total_iops = AAZIntType(
            serialized_name="totalIops",
            flags={"read_only": True},
        )
        properties.total_m_bps = AAZIntType(
            serialized_name="totalMBps",
            flags={"read_only": True},
        )
        properties.total_size_ti_b = AAZIntType(
            serialized_name="totalSizeTiB",
            flags={"read_only": True},
        )
        properties.total_volume_size_gi_b = AAZIntType(
            serialized_name="totalVolumeSizeGiB",
            flags={"read_only": True},
        )
        properties.volume_group_count = AAZIntType(
            serialized_name="volumeGroupCount",
            flags={"read_only": True},
        )

        availability_zones = _schema_elastic_san_read.properties.availability_zones
        availability_zones.Element = AAZStrType()

        private_endpoint_connections = _schema_elastic_san_read.properties.private_endpoint_connections
        private_endpoint_connections.Element = AAZObjectType()

        _element = _schema_elastic_san_read.properties.private_endpoint_connections.Element
        _element.id = AAZStrType(
            flags={"read_only": True},
        )
        _element.name = AAZStrType(
            flags={"read_only": True},
        )
        _element.properties = AAZObjectType(
            flags={"required": True, "client_flatten": True},
        )
        _element.system_data = AAZObjectType(
            serialized_name="systemData",
            flags={"read_only": True},
        )
        cls._build_schema_system_data_read(_element.system_data)
        _element.type = AAZStrType(
            flags={"read_only": True},
        )

        properties = _schema_elastic_san_read.properties.private_endpoint_connections.Element.properties
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

        group_ids = _schema_elastic_san_read.properties.private_endpoint_connections.Element.properties.group_ids
        group_ids.Element = AAZStrType()

        private_endpoint = _schema_elastic_san_read.properties.private_endpoint_connections.Element.properties.private_endpoint
        private_endpoint.id = AAZStrType(
            flags={"read_only": True},
        )

        private_link_service_connection_state = _schema_elastic_san_read.properties.private_endpoint_connections.Element.properties.private_link_service_connection_state
        private_link_service_connection_state.actions_required = AAZStrType(
            serialized_name="actionsRequired",
        )
        private_link_service_connection_state.description = AAZStrType()
        private_link_service_connection_state.status = AAZStrType()

        sku = _schema_elastic_san_read.properties.sku
        sku.name = AAZStrType(
            flags={"required": True},
        )
        sku.tier = AAZStrType()

        tags = _schema_elastic_san_read.tags
        tags.Element = AAZStrType()

        _schema.id = cls._schema_elastic_san_read.id
        _schema.location = cls._schema_elastic_san_read.location
        _schema.name = cls._schema_elastic_san_read.name
        _schema.properties = cls._schema_elastic_san_read.properties
        _schema.system_data = cls._schema_elastic_san_read.system_data
        _schema.tags = cls._schema_elastic_san_read.tags
        _schema.type = cls._schema_elastic_san_read.type

    _schema_system_data_read = None

    @classmethod
    def _build_schema_system_data_read(cls, _schema):
        if cls._schema_system_data_read is not None:
            _schema.created_at = cls._schema_system_data_read.created_at
            _schema.created_by = cls._schema_system_data_read.created_by
            _schema.created_by_type = cls._schema_system_data_read.created_by_type
            _schema.last_modified_at = cls._schema_system_data_read.last_modified_at
            _schema.last_modified_by = cls._schema_system_data_read.last_modified_by
            _schema.last_modified_by_type = cls._schema_system_data_read.last_modified_by_type
            return

        cls._schema_system_data_read = _schema_system_data_read = AAZObjectType(
            flags={"read_only": True}
        )

        system_data_read = _schema_system_data_read
        system_data_read.created_at = AAZStrType(
            serialized_name="createdAt",
        )
        system_data_read.created_by = AAZStrType(
            serialized_name="createdBy",
        )
        system_data_read.created_by_type = AAZStrType(
            serialized_name="createdByType",
        )
        system_data_read.last_modified_at = AAZStrType(
            serialized_name="lastModifiedAt",
        )
        system_data_read.last_modified_by = AAZStrType(
            serialized_name="lastModifiedBy",
        )
        system_data_read.last_modified_by_type = AAZStrType(
            serialized_name="lastModifiedByType",
        )

        _schema.created_at = cls._schema_system_data_read.created_at
        _schema.created_by = cls._schema_system_data_read.created_by
        _schema.created_by_type = cls._schema_system_data_read.created_by_type
        _schema.last_modified_at = cls._schema_system_data_read.last_modified_at
        _schema.last_modified_by = cls._schema_system_data_read.last_modified_by
        _schema.last_modified_by_type = cls._schema_system_data_read.last_modified_by_type


__all__ = ["Update"]
