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
    "networkcloud trunkednetwork create",
    is_preview=True,
)
class Create(AAZCommand):
    """Create a new trunked network or update the properties of the existing trunked network.

    :example: Create or update trunked network
        az networkcloud trunkednetwork create --resource-group "resourceGroupName" --name "trunkedNetworkName" --extended-location name="/subscriptions/subscriptionId/resourceGroups/resourceGroupName/providers/Microsoft.ExtendedLocation/customLocations/clusterExtendedLocationName" type="CustomLocation" --location "location" --interface-name "eth0" --isolation-domain-ids "/subscriptions/subscriptionId/resourceGroups/resourceGroupName/providers/Microsoft.ManagedNetworkFabric/l2IsolationDomains/l2IsolationDomainName" "/subscriptions/subscriptionId/resourceGroups/resourceGroupName/providers/Microsoft.ManagedNetworkFabric/l3IsolationDomains/l3IsolationDomainName" --vlans 12 14 --tags key1="myvalue1" key2="myvalue2"
    """

    _aaz_info = {
        "version": "2024-07-01",
        "resources": [
            ["mgmt-plane", "/subscriptions/{}/resourcegroups/{}/providers/microsoft.networkcloud/trunkednetworks/{}", "2024-07-01"],
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
        _args_schema.trunked_network_name = AAZStrArg(
            options=["-n", "--name", "--trunked-network-name"],
            help="The name of the trunked network.",
            required=True,
            fmt=AAZStrArgFormat(
                pattern="^([a-zA-Z0-9][a-zA-Z0-9-_]{0,28}[a-zA-Z0-9])$",
            ),
        )

        # define Arg Group "Properties"

        _args_schema = cls._args_schema
        _args_schema.interface_name = AAZStrArg(
            options=["--interface-name"],
            arg_group="Properties",
            help="The default interface name for this trunked network in the virtual machine. This name can be overridden by the name supplied in the network attachment configuration of that virtual machine.",
            fmt=AAZStrArgFormat(
                pattern="^[a-zA-Z0-9@._-]*$",
                max_length=12,
            ),
        )
        _args_schema.isolation_domain_ids = AAZListArg(
            options=["--isolation-domain-ids"],
            arg_group="Properties",
            help="The list of resource IDs representing the Network Fabric isolation domains. It can be any combination of l2IsolationDomain and l3IsolationDomain resources.",
            required=True,
        )
        _args_schema.vlans = AAZListArg(
            options=["--vlans"],
            arg_group="Properties",
            help="The list of vlans that are selected from the isolation domains for trunking.",
            required=True,
        )

        isolation_domain_ids = cls._args_schema.isolation_domain_ids
        isolation_domain_ids.Element = AAZStrArg()

        vlans = cls._args_schema.vlans
        vlans.Element = AAZIntArg()

        # define Arg Group "TrunkedNetworkParameters"

        _args_schema = cls._args_schema
        _args_schema.extended_location = AAZObjectArg(
            options=["--extended-location"],
            arg_group="TrunkedNetworkParameters",
            help="The extended location of the cluster associated with the resource.",
            required=True,
        )
        _args_schema.location = AAZResourceLocationArg(
            arg_group="TrunkedNetworkParameters",
            help="The geo-location where the resource lives",
            required=True,
            fmt=AAZResourceLocationArgFormat(
                resource_group_arg="resource_group",
            ),
        )
        _args_schema.tags = AAZDictArg(
            options=["--tags"],
            arg_group="TrunkedNetworkParameters",
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
        return cls._args_schema

    def _execute_operations(self):
        self.pre_operations()
        yield self.TrunkedNetworksCreateOrUpdate(ctx=self.ctx)()
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

    class TrunkedNetworksCreateOrUpdate(AAZHttpOperation):
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
                "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.NetworkCloud/trunkedNetworks/{trunkedNetworkName}",
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
                    "resourceGroupName", self.ctx.args.resource_group,
                    required=True,
                ),
                **self.serialize_url_param(
                    "subscriptionId", self.ctx.subscription_id,
                    required=True,
                ),
                **self.serialize_url_param(
                    "trunkedNetworkName", self.ctx.args.trunked_network_name,
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
            _builder.set_prop("properties", AAZObjectType, ".", typ_kwargs={"flags": {"required": True, "client_flatten": True}})
            _builder.set_prop("tags", AAZDictType, ".tags")

            extended_location = _builder.get(".extendedLocation")
            if extended_location is not None:
                extended_location.set_prop("name", AAZStrType, ".name", typ_kwargs={"flags": {"required": True}})
                extended_location.set_prop("type", AAZStrType, ".type", typ_kwargs={"flags": {"required": True}})

            properties = _builder.get(".properties")
            if properties is not None:
                properties.set_prop("interfaceName", AAZStrType, ".interface_name")
                properties.set_prop("isolationDomainIds", AAZListType, ".isolation_domain_ids", typ_kwargs={"flags": {"required": True}})
                properties.set_prop("vlans", AAZListType, ".vlans", typ_kwargs={"flags": {"required": True}})

            isolation_domain_ids = _builder.get(".properties.isolationDomainIds")
            if isolation_domain_ids is not None:
                isolation_domain_ids.set_elements(AAZStrType, ".")

            vlans = _builder.get(".properties.vlans")
            if vlans is not None:
                vlans.set_elements(AAZIntType, ".")

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
                flags={"required": True, "client_flatten": True},
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
            properties.hybrid_aks_clusters_associated_ids = AAZListType(
                serialized_name="hybridAksClustersAssociatedIds",
                flags={"read_only": True},
            )
            properties.hybrid_aks_plugin_type = AAZStrType(
                serialized_name="hybridAksPluginType",
            )
            properties.interface_name = AAZStrType(
                serialized_name="interfaceName",
            )
            properties.isolation_domain_ids = AAZListType(
                serialized_name="isolationDomainIds",
                flags={"required": True},
            )
            properties.provisioning_state = AAZStrType(
                serialized_name="provisioningState",
                flags={"read_only": True},
            )
            properties.virtual_machines_associated_ids = AAZListType(
                serialized_name="virtualMachinesAssociatedIds",
                flags={"read_only": True},
            )
            properties.vlans = AAZListType(
                flags={"required": True},
            )

            associated_resource_ids = cls._schema_on_200_201.properties.associated_resource_ids
            associated_resource_ids.Element = AAZStrType()

            hybrid_aks_clusters_associated_ids = cls._schema_on_200_201.properties.hybrid_aks_clusters_associated_ids
            hybrid_aks_clusters_associated_ids.Element = AAZStrType()

            isolation_domain_ids = cls._schema_on_200_201.properties.isolation_domain_ids
            isolation_domain_ids.Element = AAZStrType()

            virtual_machines_associated_ids = cls._schema_on_200_201.properties.virtual_machines_associated_ids
            virtual_machines_associated_ids.Element = AAZStrType()

            vlans = cls._schema_on_200_201.properties.vlans
            vlans.Element = AAZIntType()

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


__all__ = ["Create"]
