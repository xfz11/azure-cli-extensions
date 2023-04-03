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
    "confidentialledger managedccfs list",
    is_preview=True,
)
class List(AAZCommand):
    """View the Azure Managed CCF instances in a resource group.

    :example: View the Managed CCF instances
        az confidentialledger managedccfs list --resource-group "myResourceGroup"
    """

    _aaz_info = {
        "version": "2023-01-26-preview",
        "resources": [
            ["mgmt-plane", "/subscriptions/{}/providers/microsoft.confidentialledger/managedccfs/", "2023-01-26-preview"],
            ["mgmt-plane", "/subscriptions/{}/resourcegroups/{}/providers/microsoft.confidentialledger/managedccfs", "2023-01-26-preview"],
        ]
    }

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
        condition_0 = has_value(self.ctx.subscription_id) and has_value(self.ctx.args.resource_group) is not True
        condition_1 = has_value(self.ctx.args.resource_group) and has_value(self.ctx.subscription_id)
        if condition_0:
            self.ManagedCCFListBySubscription(ctx=self.ctx)()
        if condition_1:
            self.ManagedCCFListByResourceGroup(ctx=self.ctx)()
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

    class ManagedCCFListBySubscription(AAZHttpOperation):
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
                "/subscriptions/{subscriptionId}/providers/Microsoft.ConfidentialLedger/managedCCFs/",
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
                    "api-version", "2023-01-26-preview",
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
            _schema_on_200.value = AAZListType()

            value = cls._schema_on_200.value
            value.Element = AAZObjectType()

            _element = cls._schema_on_200.value.Element
            _element.id = AAZStrType(
                flags={"read_only": True},
            )
            _element.location = AAZStrType(
                flags={"required": True},
            )
            _element.name = AAZStrType(
                flags={"read_only": True},
            )
            _element.properties = AAZObjectType()
            _element.system_data = AAZObjectType(
                serialized_name="systemData",
                flags={"read_only": True},
            )
            _element.tags = AAZDictType()
            _element.type = AAZStrType(
                flags={"read_only": True},
            )

            properties = cls._schema_on_200.value.Element.properties
            properties.app_name = AAZStrType(
                serialized_name="appName",
                flags={"read_only": True},
            )
            properties.app_uri = AAZStrType(
                serialized_name="appUri",
                flags={"read_only": True},
            )
            properties.deployment_type = AAZObjectType(
                serialized_name="deploymentType",
            )
            properties.identity_service_uri = AAZStrType(
                serialized_name="identityServiceUri",
                flags={"read_only": True},
            )
            properties.member_identity_certificates = AAZListType(
                serialized_name="memberIdentityCertificates",
            )
            properties.node_count = AAZIntType(
                serialized_name="nodeCount",
            )
            properties.provisioning_state = AAZStrType(
                serialized_name="provisioningState",
            )

            deployment_type = cls._schema_on_200.value.Element.properties.deployment_type
            deployment_type.app_source_uri = AAZStrType(
                serialized_name="appSourceUri",
            )
            deployment_type.language_runtime = AAZStrType(
                serialized_name="languageRuntime",
            )

            member_identity_certificates = cls._schema_on_200.value.Element.properties.member_identity_certificates
            member_identity_certificates.Element = AAZObjectType()

            _element = cls._schema_on_200.value.Element.properties.member_identity_certificates.Element
            _element.certificate = AAZStrType()
            _element.encryptionkey = AAZStrType()
            _element.tags = AAZDictType()

            tags = cls._schema_on_200.value.Element.properties.member_identity_certificates.Element.tags
            tags.Element = AAZStrType()

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

    class ManagedCCFListByResourceGroup(AAZHttpOperation):
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
                "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ConfidentialLedger/managedCCFs",
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
                    "api-version", "2023-01-26-preview",
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
            _schema_on_200.value = AAZListType()

            value = cls._schema_on_200.value
            value.Element = AAZObjectType()

            _element = cls._schema_on_200.value.Element
            _element.id = AAZStrType(
                flags={"read_only": True},
            )
            _element.location = AAZStrType(
                flags={"required": True},
            )
            _element.name = AAZStrType(
                flags={"read_only": True},
            )
            _element.properties = AAZObjectType()
            _element.system_data = AAZObjectType(
                serialized_name="systemData",
                flags={"read_only": True},
            )
            _element.tags = AAZDictType()
            _element.type = AAZStrType(
                flags={"read_only": True},
            )

            properties = cls._schema_on_200.value.Element.properties
            properties.app_name = AAZStrType(
                serialized_name="appName",
                flags={"read_only": True},
            )
            properties.app_uri = AAZStrType(
                serialized_name="appUri",
                flags={"read_only": True},
            )
            properties.deployment_type = AAZObjectType(
                serialized_name="deploymentType",
            )
            properties.identity_service_uri = AAZStrType(
                serialized_name="identityServiceUri",
                flags={"read_only": True},
            )
            properties.member_identity_certificates = AAZListType(
                serialized_name="memberIdentityCertificates",
            )
            properties.node_count = AAZIntType(
                serialized_name="nodeCount",
            )
            properties.provisioning_state = AAZStrType(
                serialized_name="provisioningState",
            )

            deployment_type = cls._schema_on_200.value.Element.properties.deployment_type
            deployment_type.app_source_uri = AAZStrType(
                serialized_name="appSourceUri",
            )
            deployment_type.language_runtime = AAZStrType(
                serialized_name="languageRuntime",
            )

            member_identity_certificates = cls._schema_on_200.value.Element.properties.member_identity_certificates
            member_identity_certificates.Element = AAZObjectType()

            _element = cls._schema_on_200.value.Element.properties.member_identity_certificates.Element
            _element.certificate = AAZStrType()
            _element.encryptionkey = AAZStrType()
            _element.tags = AAZDictType()

            tags = cls._schema_on_200.value.Element.properties.member_identity_certificates.Element.tags
            tags.Element = AAZStrType()

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
