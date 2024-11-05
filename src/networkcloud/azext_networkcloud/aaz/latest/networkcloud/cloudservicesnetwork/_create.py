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
    "networkcloud cloudservicesnetwork create",
    is_preview=True,
)
class Create(AAZCommand):
    """Create a new cloud services network or update the properties of the existing cloud services network.

    :example: Create or update cloud services network
        az networkcloud cloudservicesnetwork create --name "cloudServicesNetworkName" --extended-location name="/subscriptions/subscriptionId/resourceGroups/resourceGroupName/providers/Microsoft.ExtendedLocation/customLocations/clusterExtendedLocationName" type="CustomLocation" --location "location" --additional-egress-endpoints "[{category:'azure-resource-management',endpoints:[{domainName:'storageaccountex.blob.core.windows.net',port:443}]}]" --enable-default-egress-endpoints "False" --tags key1="myvalue1" key2="myvalue2" --resource-group "resourceGroupName"
    """

    _aaz_info = {
        "version": "2024-07-01",
        "resources": [
            ["mgmt-plane", "/subscriptions/{}/resourcegroups/{}/providers/microsoft.networkcloud/cloudservicesnetworks/{}", "2024-07-01"],
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
        _args_schema.cloud_services_network_name = AAZStrArg(
            options=["-n", "--name", "--cloud-services-network-name"],
            help="The name of the cloud services network.",
            required=True,
            fmt=AAZStrArgFormat(
                pattern="^([a-zA-Z0-9][a-zA-Z0-9-_]{0,28}[a-zA-Z0-9])$",
            ),
        )
        _args_schema.resource_group = AAZResourceGroupNameArg(
            required=True,
        )

        # define Arg Group "CloudServicesNetworkParameters"

        _args_schema = cls._args_schema
        _args_schema.extended_location = AAZObjectArg(
            options=["--extended-location"],
            arg_group="CloudServicesNetworkParameters",
            help="The extended location of the cluster associated with the resource.",
            required=True,
        )
        _args_schema.location = AAZResourceLocationArg(
            arg_group="CloudServicesNetworkParameters",
            help="The geo-location where the resource lives",
            required=True,
            fmt=AAZResourceLocationArgFormat(
                resource_group_arg="resource_group",
            ),
        )
        _args_schema.tags = AAZDictArg(
            options=["--tags"],
            arg_group="CloudServicesNetworkParameters",
            help="Resource tags.",
        )

        extended_location = cls._args_schema.extended_location
        extended_location.name = AAZStrArg(
            options=["name"],
            help="The resource ID of the extended location on which the resource will be created.",
            required=True,
        )
        extended_location.type = AAZStrArg(
            options=["type"],
            help="The extended location type, for example, CustomLocation.",
            required=True,
        )

        tags = cls._args_schema.tags
        tags.Element = AAZStrArg()

        # define Arg Group "Properties"

        _args_schema = cls._args_schema
        _args_schema.additional_egress_endpoints = AAZListArg(
            options=["--additional-egress-endpoints"],
            arg_group="Properties",
            help="The list of egress endpoints. This allows for connection from a Hybrid AKS cluster to the specified endpoint.",
        )
        _args_schema.enable_default_egress_endpoints = AAZStrArg(
            options=["--enable-default-egress-endpoints"],
            arg_group="Properties",
            help="The indicator of whether the platform default endpoints are allowed for the egress traffic.",
            default="True",
            enum={"False": "False", "True": "True"},
        )

        additional_egress_endpoints = cls._args_schema.additional_egress_endpoints
        additional_egress_endpoints.Element = AAZObjectArg()

        _element = cls._args_schema.additional_egress_endpoints.Element
        _element.category = AAZStrArg(
            options=["category"],
            help="The descriptive category name of endpoints accessible by the AKS agent node. For example, azure-resource-management, API server, etc. The platform egress endpoints provided by default will use the category 'default'.",
            required=True,
        )
        _element.endpoints = AAZListArg(
            options=["endpoints"],
            help="The list of endpoint dependencies.",
            required=True,
            fmt=AAZListArgFormat(
                min_length=1,
            ),
        )

        endpoints = cls._args_schema.additional_egress_endpoints.Element.endpoints
        endpoints.Element = AAZObjectArg()

        _element = cls._args_schema.additional_egress_endpoints.Element.endpoints.Element
        _element.domain_name = AAZStrArg(
            options=["domain-name"],
            help="The domain name of the dependency.",
            required=True,
        )
        _element.port = AAZIntArg(
            options=["port"],
            help="The port of this endpoint.",
            fmt=AAZIntArgFormat(
                maximum=65535,
                minimum=1,
            ),
        )
        return cls._args_schema

    def _execute_operations(self):
        self.pre_operations()
        yield self.CloudServicesNetworksCreateOrUpdate(ctx=self.ctx)()
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

    class CloudServicesNetworksCreateOrUpdate(AAZHttpOperation):
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
                "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.NetworkCloud/cloudServicesNetworks/{cloudServicesNetworkName}",
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
                    "cloudServicesNetworkName", self.ctx.args.cloud_services_network_name,
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
                typ_kwargs={"flags": {"required": True, "client_flatten": True}}
            )
            _builder.set_prop("extendedLocation", AAZObjectType, ".extended_location", typ_kwargs={"flags": {"required": True}})
            _builder.set_prop("location", AAZStrType, ".location", typ_kwargs={"flags": {"required": True}})
            _builder.set_prop("properties", AAZObjectType, typ_kwargs={"flags": {"client_flatten": True}})
            _builder.set_prop("tags", AAZDictType, ".tags")

            extended_location = _builder.get(".extendedLocation")
            if extended_location is not None:
                extended_location.set_prop("name", AAZStrType, ".name", typ_kwargs={"flags": {"required": True}})
                extended_location.set_prop("type", AAZStrType, ".type", typ_kwargs={"flags": {"required": True}})

            properties = _builder.get(".properties")
            if properties is not None:
                properties.set_prop("additionalEgressEndpoints", AAZListType, ".additional_egress_endpoints")
                properties.set_prop("enableDefaultEgressEndpoints", AAZStrType, ".enable_default_egress_endpoints")

            additional_egress_endpoints = _builder.get(".properties.additionalEgressEndpoints")
            if additional_egress_endpoints is not None:
                additional_egress_endpoints.set_elements(AAZObjectType, ".")

            _elements = _builder.get(".properties.additionalEgressEndpoints[]")
            if _elements is not None:
                _elements.set_prop("category", AAZStrType, ".category", typ_kwargs={"flags": {"required": True}})
                _elements.set_prop("endpoints", AAZListType, ".endpoints", typ_kwargs={"flags": {"required": True}})

            endpoints = _builder.get(".properties.additionalEgressEndpoints[].endpoints")
            if endpoints is not None:
                endpoints.set_elements(AAZObjectType, ".")

            _elements = _builder.get(".properties.additionalEgressEndpoints[].endpoints[]")
            if _elements is not None:
                _elements.set_prop("domainName", AAZStrType, ".domain_name", typ_kwargs={"flags": {"required": True}})
                _elements.set_prop("port", AAZIntType, ".port")

            tags = _builder.get(".tags")
            if tags is not None:
                tags.set_elements(AAZStrType, ".")

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

            _schema_on_200_201 = cls._schema_on_200_201
            _schema_on_200_201.extended_location = AAZObjectType(
                serialized_name="extendedLocation",
                flags={"required": True},
            )
            _schema_on_200_201.id = AAZStrType(
                flags={"read_only": True},
            )
            _schema_on_200_201.location = AAZStrType(
                flags={"required": True},
            )
            _schema_on_200_201.name = AAZStrType(
                flags={"read_only": True},
            )
            _schema_on_200_201.properties = AAZObjectType(
                flags={"client_flatten": True},
            )
            _schema_on_200_201.system_data = AAZObjectType(
                serialized_name="systemData",
                flags={"read_only": True},
            )
            _schema_on_200_201.tags = AAZDictType()
            _schema_on_200_201.type = AAZStrType(
                flags={"read_only": True},
            )

            extended_location = cls._schema_on_200_201.extended_location
            extended_location.name = AAZStrType(
                flags={"required": True},
            )
            extended_location.type = AAZStrType(
                flags={"required": True},
            )

            properties = cls._schema_on_200_201.properties
            properties.additional_egress_endpoints = AAZListType(
                serialized_name="additionalEgressEndpoints",
            )
            properties.associated_resource_ids = AAZListType(
                serialized_name="associatedResourceIds",
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
            properties.enable_default_egress_endpoints = AAZStrType(
                serialized_name="enableDefaultEgressEndpoints",
            )
            properties.enabled_egress_endpoints = AAZListType(
                serialized_name="enabledEgressEndpoints",
                flags={"read_only": True},
            )
            properties.hybrid_aks_clusters_associated_ids = AAZListType(
                serialized_name="hybridAksClustersAssociatedIds",
                flags={"read_only": True},
            )
            properties.interface_name = AAZStrType(
                serialized_name="interfaceName",
                flags={"read_only": True},
            )
            properties.provisioning_state = AAZStrType(
                serialized_name="provisioningState",
                flags={"read_only": True},
            )
            properties.virtual_machines_associated_ids = AAZListType(
                serialized_name="virtualMachinesAssociatedIds",
                flags={"read_only": True},
            )

            additional_egress_endpoints = cls._schema_on_200_201.properties.additional_egress_endpoints
            additional_egress_endpoints.Element = AAZObjectType()
            _CreateHelper._build_schema_egress_endpoint_read(additional_egress_endpoints.Element)

            associated_resource_ids = cls._schema_on_200_201.properties.associated_resource_ids
            associated_resource_ids.Element = AAZStrType()

            enabled_egress_endpoints = cls._schema_on_200_201.properties.enabled_egress_endpoints
            enabled_egress_endpoints.Element = AAZObjectType()
            _CreateHelper._build_schema_egress_endpoint_read(enabled_egress_endpoints.Element)

            hybrid_aks_clusters_associated_ids = cls._schema_on_200_201.properties.hybrid_aks_clusters_associated_ids
            hybrid_aks_clusters_associated_ids.Element = AAZStrType()

            virtual_machines_associated_ids = cls._schema_on_200_201.properties.virtual_machines_associated_ids
            virtual_machines_associated_ids.Element = AAZStrType()

            system_data = cls._schema_on_200_201.system_data
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

            tags = cls._schema_on_200_201.tags
            tags.Element = AAZStrType()

            return cls._schema_on_200_201


class _CreateHelper:
    """Helper class for Create"""

    _schema_egress_endpoint_read = None

    @classmethod
    def _build_schema_egress_endpoint_read(cls, _schema):
        if cls._schema_egress_endpoint_read is not None:
            _schema.category = cls._schema_egress_endpoint_read.category
            _schema.endpoints = cls._schema_egress_endpoint_read.endpoints
            return

        cls._schema_egress_endpoint_read = _schema_egress_endpoint_read = AAZObjectType()

        egress_endpoint_read = _schema_egress_endpoint_read
        egress_endpoint_read.category = AAZStrType(
            flags={"required": True},
        )
        egress_endpoint_read.endpoints = AAZListType(
            flags={"required": True},
        )

        endpoints = _schema_egress_endpoint_read.endpoints
        endpoints.Element = AAZObjectType()

        _element = _schema_egress_endpoint_read.endpoints.Element
        _element.domain_name = AAZStrType(
            serialized_name="domainName",
            flags={"required": True},
        )
        _element.port = AAZIntType()

        _schema.category = cls._schema_egress_endpoint_read.category
        _schema.endpoints = cls._schema_egress_endpoint_read.endpoints


__all__ = ["Create"]
