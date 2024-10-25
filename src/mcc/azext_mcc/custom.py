# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#
# Code generated by aaz-dev-tools
# --------------------------------------------------------------------------------------------

# pylint: disable=too-many-lines
# pylint: disable=too-many-statements
# pylint: disable=line-too-long
# pylint: disable=protected-access
# pylint: disable=too-many-nested-blocks
# pylint: disable=too-many-branches
# pylint: disable=unused-argument

from .aaz.latest.mcc.ent.resource._create import Create as _MccEntResourceCreate
from .aaz.latest.mcc.ent.resource._delete import Delete as _MccEntResourceDelete
from .aaz.latest.mcc.ent.resource._list import List as _MccEntResourceList

from .aaz.latest.mcc.ent.node._create import Create as _MccEntNodeCreate
from .aaz.latest.mcc.ent.node._update import Update as _MccEntNodeUpdate
from .aaz.latest.mcc.ent.node._delete import Delete as _MccEntNodeDelete
from .aaz.latest.mcc.ent.node._list import List as _MccEntNodeList
from .aaz.latest.mcc.ent.node._show import Show as _MccEntNodeShow
from .aaz.latest.mcc.ent.node._get_provisioning_details import GetProvisioningDetails as _MccEntNodeGetProvisioningDetails

from azure.cli.core.aaz import has_value

from azure.cli.core.util import CLIError
from azure.cli.core.azclierror import ValidationError

from knack.log import get_logger
logger = get_logger(__name__)


class MccEntResourceCreate(_MccEntResourceCreate):
    @classmethod
    def _build_arguments_schema(cls, *args, **kwargs):
        args_schema = super()._build_arguments_schema(*args, **kwargs)

        args_schema.customer._registered = False
        args_schema.additional_customer_properties._registered = False

        args_schema.no_wait._registered = False

        return args_schema

    def _output(self, *args, **kwargs):
        result = self.deserialize_output(self.ctx.vars.instance, client_flatten=True)

        cleanOutput = {}

        try:
            cleanOutput["mccResourceId"] = result["properties"]["customer"]["customerId"]
        except KeyError:
            pass

        try:
            cleanOutput["mccResourceName"] = result["properties"]["customer"]["customerName"]
        except KeyError:
            pass

        try:
            cleanOutput["location"] = result["location"]
        except KeyError:
            pass

        try:
            fullyQualifiedResourceIdParts = str(result["id"]).split('/')
            cleanOutput["resourceGroup"] = fullyQualifiedResourceIdParts[4]
        except KeyError:
            pass

        try:
            cleanOutput["operationStatus"] = result["properties"]["provisioningState"]
        except KeyError:
            pass

        return cleanOutput


class MccEntResourceDelete(_MccEntResourceDelete):
    @classmethod
    def _build_arguments_schema(cls, *args, **kwargs):
        args_schema = super()._build_arguments_schema(*args, **kwargs)
        args_schema.no_wait._registered = False

        return args_schema

    def _output(self):
        result = self.deserialize_output(self.ctx.vars.instance, client_flatten=True)
        return result


class MccEntResourceList(_MccEntResourceList):
    @classmethod
    def _build_arguments_schema(cls, *args, **kwargs):

        args_schema = super()._build_arguments_schema(*args, **kwargs)

        return args_schema

    def _output(self, *args, **kwargs):
        result = self.deserialize_output(self.ctx.vars.instance.value, client_flatten=True)
        next_link = self.deserialize_output(self.ctx.vars.instance.next_link)

        cleanOutput = []

        for customer in result:
            try:
                if "isp" in str(customer["type"]):
                    continue
            except KeyError:
                pass

            cleanCustomer = {}

            try:
                cleanCustomer["mccResourceId"] = customer["properties"]["customer"]["customerId"]
            except KeyError:
                pass

            try:
                cleanCustomer["mccResourceName"] = customer["properties"]["customer"]["customerName"]
            except KeyError:
                pass

            try:
                cleanCustomer["location"] = customer["location"]
            except KeyError:
                pass

            cleanOutput.append(cleanCustomer)

        return cleanOutput, next_link


class MccEntNodeCreate(_MccEntNodeCreate):
    @classmethod
    def _build_arguments_schema(cls, *args, **kwargs):
        args_schema = super()._build_arguments_schema(*args, **kwargs)

        args_schema.location._required = False
        args_schema.location._registered = False

        args_schema.host_os._required = True

        args_schema.cache_node._registered = False

        args_schema.auto_update_version._registered = False
        args_schema.bgp_configuration._registered = False
        args_schema.cache_node_properties_details_issues_list._registered = False
        args_schema.optional_property1._registered = False
        args_schema.optional_property2._registered = False
        args_schema.optional_property3._registered = False
        args_schema.optional_property4._registered = False
        args_schema.optional_property5._registered = False
        args_schema.proxy_url._registered = False
        args_schema.update_cycle_type._registered = False
        args_schema.update_info_details._registered = False
        args_schema.update_requested_date_time._registered = False
        args_schema.enable_proxy._registered = False
        args_schema.proxy_host._registered = False
        args_schema.status_code._registered = False
        args_schema.status_details._registered = False
        args_schema.status_text._registered = False
        args_schema.cache_drive._registered = False

        args_schema.no_wait._registered = False

        return args_schema

    def pre_operations(self):
        args = self.ctx.args

        args.cache_node.is_enabled = True
        args.optional_property1 = "1"

        if has_value(args.host_os):
            if str(args.host_os).lower() == str("Eflow").lower():
                err_msg = "ValidationError: Parameter --host-os is set to \"Eflow\", this operating system type is deprecated for new cache nodes. Please use \'Windows\' or \'Linux\'."
                raise ValidationError(err_msg)

        try:
            from .aaz.latest.mcc.ent.resource._show import Show
            ShowOutput = Show(cli_ctx=self.cli_ctx)(command_args={
                "mcc_resource_name": args.mcc_resource_name,
                "resource_group": args.resource_group
            })
            args.location = str(ShowOutput["location"])
        except:
            err_msg = "Cache node resource creation failed. CLI could not find the specified MCC resource with name \'" + str(args.cache_node_name) + "\' that the cache node would be created on."
            raise CLIError(err_msg)

    def _output(self, *args, **kwargs):
        result = self.deserialize_output(self.ctx.vars.instance, client_flatten=True)

        cleanOutput = {}

        try:
            cleanOutput["cacheNodeId"] = result["properties"]["cacheNode"]["cacheNodeId"]
        except KeyError:
            pass

        try:
            cleanOutput["hostOs"] = result["properties"]["additionalCacheNodeProperties"]["osType"]
        except KeyError:
            pass

        try:
            cleanOutput["cacheNodeName"] = result["properties"]["cacheNode"]["cacheNodeName"]
        except KeyError:
            pass

        try:
            cleanOutput["cacheNodeState"] = result["properties"]["additionalCacheNodeProperties"]["cacheNodeStateShortText"]
        except KeyError:
            pass

        try:
            cleanOutput["operationStatus"] = result["properties"]["provisioningState"]
        except KeyError:
            pass

        return cleanOutput


class MccEntNodeUpdate(_MccEntNodeUpdate):
    def pre_operations(self):
        args = self.ctx.args

        if has_value(args.auto_update_week):
            week = args.auto_update_week
            if week < 1:
                err_msg = "InvalidArgumentValue: --auto-update-week: Invalid format: \'" + str(week) + "\' is less than 1"
                raise ValidationError(err_msg)
            if week > 4:
                err_msg = "InvalidArgumentValue: --auto-update-week: Invalid format: \'" + str(week) + "\' is greater than 4"
                raise ValidationError(err_msg)

        if has_value(args.proxy):
            if args.proxy == "Required":
                err_msg = "ValidationError: Parameter --enable-proxy is set to \"Required\", must set to \"Enabled\"."
                raise ValidationError(err_msg)
            if args.proxy == "None":
                err_msg = "ValidationError: Parameter --enable-proxy is set to \"None\", must set to \"Disabled\"."
                raise ValidationError(err_msg)

        if has_value(args.cache_drive):
            driveArray = args.cache_drive
            index = 0
            driveNumber = 1
            for drive in driveArray:
                if has_value(drive.cache_number):
                    err_msg = "ValidationError: --cache-drive[" + str(index) + "].cache-number: Cannot be present"
                    raise ValidationError(err_msg)

                drive.cache_number = driveNumber

                if has_value(drive.nginx_mapping):
                    err_msg = "ValidationError: --cache-drive[" + str(index) + "].nginx-mapping: Cannot be present"
                    raise ValidationError(err_msg)

                if not has_value(drive.physical_path):
                    err_msg = "ValidationError: --cache-drive[" + str(index) + "].physical-path: Cannot be Undefined"
                    raise ValidationError(err_msg)

                if not has_value(drive.size_in_gb):
                    err_msg = "ValidationError: --cache-drive[" + str(index) + "].size-in-gb: Cannot be Undefined"
                    raise ValidationError(err_msg)

                if drive.size_in_gb < 50:
                    err_msg = "ValidationError: --cache-drive[" + str(index) + "].size-in-gb: Invalid format: '" + str(drive.size_in_gb) + "' is less than 50"
                    raise ValidationError(err_msg)

                if drive.size_in_gb > 10000:
                    err_msg = "ValidationError: --cache-drive[" + str(index) + "].size-in-gb: Invalid format: '" + str(drive.size_in_gb) + "' is greater than 10000GB (10TB)"
                    raise ValidationError(err_msg)

                index += 1
                driveNumber += 1

    def pre_instance_update(self, instance):
        args = self.ctx.args

        instanceOsType = None

        try:
            instanceOsType = instance.properties.additionalCacheNodeProperties.osType
        except KeyError:
            pass

        if instanceOsType is not None:
            if has_value(args.cache_drive):
                if instanceOsType == "Windows":
                    if len(args.cache_drive) > 1:
                        err_msg = "ValidationError: --cache-drive must not include more than 1 drive when updating a \'Windows\' cache node."
                        raise ValidationError(err_msg)

                    driveArray = args.cache_drive
                    index = 0
                    for drive in driveArray:
                        if has_value(drive.physical_path):
                            if drive.physical_path != "/var/mcc":
                                err_msg = "ValidationError: --cache-drive[" + str(index) + "].physical-path: Must be \'/var/mcc\'"
                                raise ValidationError(err_msg)
                if instanceOsType == "Linux":
                    if len(args.cache_drive) > 9:
                        err_msg = "ValidationError: --cache-drive must not include more than 9 drives when updating a \'Linux\' cache node."
                        raise ValidationError(err_msg)

        instanceIsProxyRequired = None

        try:
            instanceIsProxyRequired = instance.properties.additionalCacheNodeProperties.isProxyRequired
        except KeyError:
            pass

        if instanceIsProxyRequired is not None:
            if instanceIsProxyRequired == "Enabled":
                if has_value(args.proxy):
                    if args.proxy == "Disabled":
                        if has_value(args.proxy_host) or has_value(args.proxy_port):
                            err_msg = "ValidationError: Parameter --enable-proxy is set to \"Disabled\": --proxy-host and --proxy-port cannot be provided."
                            raise ValidationError(err_msg)
                        args.proxy_host = None
                        args.proxy_port = None
                        instance.properties.additionalCacheNodeProperties.proxyUrlConfiguration = None
                    else:
                        oldProxyUrl = instance.properties.additionalCacheNodeProperties.proxyUrlConfiguration.proxyUrl
                        oldProxyUrlParts = str(oldProxyUrl).split(":")
                        newProxyHost = None
                        newProxyPort = None

                        if has_value(args.proxy_host):
                            if ':' in str(args.proxy_host):
                                err_msg = "ValidationError: --proxy-host must not include \':\'."
                                raise ValidationError(err_msg)
                            newProxyHost = args.proxy_host
                        else:
                            newProxyHost = oldProxyUrlParts[0]

                        if has_value(args.proxy_port):
                            if ':' in str(args.proxy_port):
                                err_msg = "ValidationError: --proxy-port must not include \':\'."
                                raise ValidationError(err_msg)
                            newProxyPort = args.proxy_port
                        else:
                            newProxyPort = oldProxyUrlParts[1]

                        args.proxy_host = str(newProxyHost) + ":" + str(newProxyPort)
                else:
                    oldProxyUrl = instance.properties.additionalCacheNodeProperties.proxyUrlConfiguration.proxyUrl
                    oldProxyUrlParts = str(oldProxyUrl).split(":")
                    newProxyHost = None
                    newProxyPort = None

                    if has_value(args.proxy_host):
                        if ':' in str(args.proxy_host):
                            err_msg = "ValidationError: --proxy-host must not include \':\'."
                            raise ValidationError(err_msg)
                        newProxyHost = args.proxy_host
                    else:
                        newProxyHost = oldProxyUrlParts[0]

                    if has_value(args.proxy_port):
                        if ':' in str(args.proxy_port):
                            err_msg = "ValidationError: --proxy-port must not include \':\'."
                            raise ValidationError(err_msg)
                        newProxyPort = args.proxy_port
                    else:
                        newProxyPort = oldProxyUrlParts[1]

                    args.proxy_host = str(newProxyHost) + ":" + str(newProxyPort)
            else:
                if has_value(args.proxy):
                    if args.proxy == "Enabled":
                        if not has_value(args.proxy_host) or not has_value(args.proxy_port):
                            err_msg = "ValidationError: Parameter --enable-proxy is set to \"Enabled\", must provide --proxy-host and --proxy-port parameter."
                            raise ValidationError(err_msg)

                        if ':' in str(args.proxy_host) or ':' in str(args.proxy_port):
                            err_msg = "ValidationError: --proxy-host and --proxy-port must not include \':\'."
                            raise ValidationError(err_msg)

                        args.proxy_host = str(args.proxy_host) + ":" + str(args.proxy_port)
                    else:
                        if has_value(args.proxy_host) or has_value(args.proxy_port):
                            err_msg = "ValidationError: Parameter --enable-proxy is set not provided and cache node is in proxy state \"Disabled\": --proxy-host and --proxy-port cannot be provided."
                            raise ValidationError(err_msg)
                else:
                    if has_value(args.proxy_host) or has_value(args.proxy_port):
                        err_msg = "ValidationError: Parameter --enable-proxy is set not provided and cache node is in proxy state \"Disabled\": --proxy-host and --proxy-port cannot be provided."
                        raise ValidationError(err_msg)
        else:
            if args.proxy == "Enabled":
                if not has_value(args.proxy_host) or not has_value(args.proxy_port):
                    err_msg = "ValidationError: Parameter --enable-proxy is set to \"Enabled\", must provide --proxy-host and --proxy-port parameter."
                    raise ValidationError(err_msg)

                if ':' in str(args.proxy_host) or ':' in str(args.proxy_port):
                    err_msg = "ValidationError: --proxy-host and --proxy-port must not include \':\'."
                    raise ValidationError(err_msg)

                args.proxy_host = str(args.proxy_host) + ":" + str(args.proxy_port)
            else:
                if has_value(args.proxy_host) or has_value(args.proxy_port):
                    err_msg = "ValidationError: Parameter --enable-proxy is set to \"Disabled\": --proxy-host and --proxy-port cannot be provided."
                    raise ValidationError(err_msg)

        instanceAutoUpdateRing = None

        try:
            instanceAutoUpdateRing = instance.properties.cacheNode.autoUpdateRingType
        except KeyError:
            pass

        if instanceAutoUpdateRing is not None:
            if str(instanceAutoUpdateRing) == "Fast":
                if has_value(args.auto_update_ring):
                    if str(args.auto_update_ring) == "Slow":
                        if not has_value(args.auto_update_day) or not has_value(args.auto_update_week) or not has_value(args.auto_update_time):
                            err_msg = "ValidationError: Switching cache node auto update ring from \"Fast\" to \"Slow\", --auto-update-day, --auto-update-week, and --auto-update-time must not be Undefined"
                            raise ValidationError(err_msg)
                    else:
                        if has_value(args.auto_update_day) or has_value(args.auto_update_week) or has_value(args.auto_update_time):
                            err_msg = "ValidationError: Parameter --auto-update-ring is set to \"Fast\" and cache node is already on \"Fast\" ring type, --auto-update-day, --auto-update-week, and --auto-update-time must be Undefined"
                            raise ValidationError(err_msg)
                else:
                    if has_value(args.auto_update_day) or has_value(args.auto_update_week) or has_value(args.auto_update_time):
                        err_msg = "ValidationError: Parameter --auto-update-ring is Undefined, --auto-update-day, --auto-update-week, and --auto-update-time must be Undefined"
                        raise ValidationError(err_msg)
            else:
                if has_value(args.auto_update_ring):
                    if str(args.auto_update_ring) == "Fast":
                        if has_value(args.auto_update_day) or has_value(args.auto_update_week) or has_value(args.auto_update_time):
                            err_msg = "ValidationError: Switching cache node auto update ring from \"Slow\" to \"Fast\", --auto-update-day, --auto-update-week, and --auto-update-time must be Undefined"
                            raise ValidationError(err_msg)

    @classmethod
    def _build_arguments_schema(cls, *args, **kwargs):
        from azure.cli.core.aaz import AAZIntArg

        args_schema = super()._build_arguments_schema(*args, **kwargs)

        args_schema.proxy_port = AAZIntArg(
            options=["--proxy-port"],
            help="Port number for proxy host.",
            arg_group="Configuration",
            nullable=True
        )

        args_schema.cache_node_id._registered = False
        args_schema.cidr_csv._registered = False
        args_schema.cidr_selection_type._registered = False
        args_schema.customer_asn._registered = False
        args_schema.customer_index._registered = False
        args_schema.customer_name._registered = False
        args_schema.fully_qualified_resource_id._registered = False
        args_schema.is_enabled._registered = False
        args_schema.is_enterprise_managed._registered = False
        args_schema.max_allowable_egress_in_mbps._registered = False
        args_schema.should_migrate._registered = False
        args_schema.ip_address._registered = False

        args_schema.auto_update_version._registered = False
        args_schema.bgp_configuration._registered = False
        args_schema.cache_node_properties_details_issues_list._registered = False
        args_schema.optional_property1._registered = False
        args_schema.optional_property2._registered = False
        args_schema.optional_property3._registered = False
        args_schema.optional_property4._registered = False
        args_schema.optional_property5._registered = False
        args_schema.host_os._registered = False
        args_schema.proxy_url._registered = False
        args_schema.update_cycle_type._registered = False
        args_schema.update_info_details._registered = False
        args_schema.update_requested_date_time._registered = False
        args_schema.cache_drive.Element.nginx_mapping._registered = False
        args_schema.cache_drive.Element.cache_number._registered = False
        args_schema.update_requested_date_time._registered = False
        args_schema.fully_qualified_domain_name._registered = False

        args_schema.status_code._registered = False
        args_schema.status_details._registered = False
        args_schema.status_text._registered = False

        args_schema.no_wait._registered = False
        args_schema.cache_node_name_1._registered = False

        return args_schema

    def _output(self, *args, **kwargs):
        result = self.deserialize_output(self.ctx.vars.instance, client_flatten=True)

        cleanOutput = {}

        try:
            cleanOutput["cacheNodeState"] = result["properties"]["additionalCacheNodeProperties"]["cacheNodeStateShortText"]
        except KeyError:
            pass

        try:
            cleanOutput["hostOs"] = result["properties"]["additionalCacheNodeProperties"]["osType"]
        except KeyError:
            pass

        try:
            driveArray = result["properties"]["additionalCacheNodeProperties"]["driveConfiguration"]
            cleanDriveArray = []
            for drive in driveArray:
                cleanDrive = {"physicalPath": drive["physicalPath"], "sizeInGb": drive["sizeInGb"]}
                cleanDriveArray.append(cleanDrive)
            cleanOutput["driveConfiguration"] = cleanDriveArray
        except KeyError:
            pass

        try:
            proxyUrl = result["properties"]["additionalCacheNodeProperties"]["proxyUrlConfiguration"]["proxyUrl"]
            proxyUrlParts = proxyUrl.split(":")
            if len(proxyUrlParts) == 2:
                proxyConfiguration = {"proxyHostName": proxyUrlParts[0], "proxyPort": proxyUrlParts[1]}
                cleanOutput["proxyConfiguration"] = proxyConfiguration
            else:
                proxyConfiguration = {"proxyHostName": result["properties"]["additionalCacheNodeProperties"]["proxyUrlConfiguration"]["proxyUrl"]}
                cleanOutput["proxyConfiguration"] = proxyConfiguration
        except KeyError:
            pass

        try:
            cleanOutput["cacheNodeId"] = result["properties"]["cacheNode"]["cacheNodeId"]
        except KeyError:
            pass

        try:
            cleanOutput["cacheNodeName"] = result["properties"]["cacheNode"]["cacheNodeName"]
        except KeyError:
            pass

        try:
            cleanOutput["softwareVersion"] = result["properties"]["additionalCacheNodeProperties"]["productVersion"]
        except KeyError:
            pass

        hasAutoUpdateRing = None

        try:
            cleanOutput["autoUpdateRing"] = result["properties"]["cacheNode"]["autoUpdateRingType"]
            hasAutoUpdateRing = result["properties"]["cacheNode"]["autoUpdateRingType"]
        except KeyError:
            pass

        if hasAutoUpdateRing is not None:
            if str(hasAutoUpdateRing) == "Slow":
                try:
                    cleanOutput["autoUpdateWeek"] = result["properties"]["cacheNode"]["autoUpdateRequestedWeek"]
                except KeyError:
                    pass

                try:
                    cleanOutput["autoUpdateDay"] = result["properties"]["cacheNode"]["autoUpdateRequestedDay"]
                except KeyError:
                    pass

                try:
                    cleanOutput["autoUpdateTime"] = result["properties"]["cacheNode"]["autoUpdateRequestedTime"]
                except KeyError:
                    pass

        try:
            cleanOutput["operationStatus"] = result["properties"]["provisioningState"]
        except KeyError:
            pass

        return cleanOutput


class MccEntNodeDelete(_MccEntNodeDelete):
    @classmethod
    def _build_arguments_schema(cls, *args, **kwargs):
        args_schema = super()._build_arguments_schema(*args, **kwargs)
        args_schema.no_wait._registered = False

        return args_schema

    def _output(self, *args, **kwargs):
        result = self.deserialize_output(self.ctx.vars.instance, client_flatten=True)
        return result


class MccEntNodeList(_MccEntNodeList):
    @classmethod
    def _build_arguments_schema(cls, *args, **kwargs):
        from azure.cli.core.aaz import AAZBoolArg

        args_schema = super()._build_arguments_schema(*args, **kwargs)

        args_schema.expanded = AAZBoolArg(
            options=["--expand-output"],
            help="Use this flag to expand command output and see more details."
        )

        args_schema.expanded._blank = "True"

        return args_schema

    def _output(self, *args, **kwargs):
        result = self.deserialize_output(self.ctx.vars.instance.value, client_flatten=True)
        args = self.ctx.args
        next_link = self.deserialize_output(self.ctx.vars.instance.next_link)

        cleanOutput = []

        for cacheNode in result:
            try:
                if "isp" in str(cacheNode["type"]):
                    continue
            except KeyError:
                pass

            cleanCacheNode = {}

            try:
                cleanCacheNode["cacheNodeState"] = cacheNode["properties"]["additionalCacheNodeProperties"]["cacheNodeStateShortText"]
            except KeyError:
                pass

            try:
                cleanCacheNode["cacheNodeId"] = cacheNode["properties"]["cacheNode"]["cacheNodeId"]
            except KeyError:
                pass

            try:
                cleanCacheNode["cacheNodeName"] = cacheNode["properties"]["cacheNode"]["cacheNodeName"]
            except KeyError:
                pass

            try:
                cleanCacheNode["hostOs"] = cacheNode["properties"]["additionalCacheNodeProperties"]["osType"]
            except KeyError:
                pass

            try:
                cleanCacheNode["softwareVersion"] = cacheNode["properties"]["additionalCacheNodeProperties"]["productVersion"]
            except KeyError:
                pass

            try:
                cleanCacheNode["autoUpdateRing"] = cacheNode["properties"]["cacheNode"]["autoUpdateRingType"]
                hasAutoUpdateRing = cacheNode["properties"]["cacheNode"]["autoUpdateRingType"]
            except KeyError:
                pass

            if hasAutoUpdateRing is not None:
                if str(hasAutoUpdateRing) == "Slow":
                    try:
                        cleanCacheNode["autoUpdateWeek"] = cacheNode["properties"]["cacheNode"]["autoUpdateRequestedWeek"]
                    except KeyError:
                        pass

                    try:
                        cleanCacheNode["autoUpdateDay"] = cacheNode["properties"]["cacheNode"]["autoUpdateRequestedDay"]
                    except KeyError:
                        pass

                    try:
                        cleanCacheNode["autoUpdateTime"] = cacheNode["properties"]["cacheNode"]["autoUpdateRequestedTime"]
                    except KeyError:
                        pass

            if has_value(args.expanded):
                try:
                    cleanCacheNode["cacheNodeStateDetails"] = cacheNode["properties"]["additionalCacheNodeProperties"]["cacheNodeStateDetailedText"]
                except KeyError:
                    pass

                try:
                    cleanCacheNode["proxy"] = cacheNode["properties"]["additionalCacheNodeProperties"]["isProxyRequired"]
                except KeyError:
                    pass

                try:
                    cleanCacheNode["location"] = cacheNode["properties"]["location"]
                except KeyError:
                    pass

                try:
                    driveArray = cacheNode["properties"]["additionalCacheNodeProperties"]["driveConfiguration"]
                    cleanDriveArray = []
                    for drive in driveArray:
                        cleanDrive = {"physicalPath": drive["physicalPath"], "sizeInGb": drive["sizeInGb"]}
                        cleanDriveArray.append(cleanDrive)
                    cleanCacheNode["driveConfiguration"] = cleanDriveArray
                except KeyError:
                    pass

                try:
                    proxyUrl = cacheNode["properties"]["additionalCacheNodeProperties"]["proxyUrlConfiguration"]["proxyUrl"]
                    proxyUrlParts = proxyUrl.split(":")
                    if len(proxyUrlParts) == 2:
                        proxyConfiguration = {"proxyHostName": proxyUrlParts[0], "proxyPort": proxyUrlParts[1]}
                        cleanCacheNode["proxyConfiguration"] = proxyConfiguration
                    else:
                        proxyConfiguration = {"proxyHostName": cacheNode["properties"]["additionalCacheNodeProperties"]["proxyUrlConfiguration"]["proxyUrl"]}
                        cleanCacheNode["proxyConfiguration"] = proxyConfiguration
                except KeyError:
                    pass

            cleanOutput.append(cleanCacheNode)

        return cleanOutput, next_link


class MccEntNodeShow(_MccEntNodeShow):
    @classmethod
    def _build_arguments_schema(cls, *args, **kwargs):
        from azure.cli.core.aaz import AAZBoolArg

        args_schema = super()._build_arguments_schema(*args, **kwargs)

        args_schema.expanded = AAZBoolArg(
            options=["--expand-output"],
            help="Use this flag to expand command output and see more details."
        )

        args_schema.expanded._blank = "True"

        return args_schema

    def _output(self, *args, **kwargs):
        result = self.deserialize_output(self.ctx.vars.instance, client_flatten=True)
        args = self.ctx.args

        cleanOutput = {}

        try:
            cleanOutput["cacheNodeState"] = result["properties"]["additionalCacheNodeProperties"]["cacheNodeStateShortText"]
        except KeyError:
            pass

        try:
            cleanOutput["hostOs"] = result["properties"]["additionalCacheNodeProperties"]["osType"]
        except KeyError:
            pass

        try:
            driveArray = result["properties"]["additionalCacheNodeProperties"]["driveConfiguration"]
            cleanDriveArray = []
            for drive in driveArray:
                cleanDrive = {"physicalPath": drive["physicalPath"], "sizeInGb": drive["sizeInGb"]}
                cleanDriveArray.append(cleanDrive)
            cleanOutput["driveConfiguration"] = cleanDriveArray
        except KeyError:
            pass

        try:
            proxyUrl = result["properties"]["additionalCacheNodeProperties"]["proxyUrlConfiguration"]["proxyUrl"]
            proxyUrlParts = proxyUrl.split(":")
            if len(proxyUrlParts) == 2:
                proxyConfiguration = {"proxyHostName": proxyUrlParts[0], "proxyPort": proxyUrlParts[1]}
                cleanOutput["proxyConfiguration"] = proxyConfiguration
            else:
                proxyConfiguration = {"proxyHostName": result["properties"]["additionalCacheNodeProperties"]["proxyUrlConfiguration"]["proxyUrl"]}
                cleanOutput["proxyConfiguration"] = proxyConfiguration
        except KeyError:
            pass

        try:
            cleanOutput["cacheNodeId"] = result["properties"]["cacheNode"]["cacheNodeId"]
        except KeyError:
            pass

        try:
            cleanOutput["cacheNodeName"] = result["properties"]["cacheNode"]["cacheNodeName"]
        except KeyError:
            pass

        try:
            cleanOutput["softwareVersion"] = result["properties"]["additionalCacheNodeProperties"]["productVersion"]
        except KeyError:
            pass

        hasAutoUpdateRing = None

        try:
            cleanOutput["autoUpdateRing"] = result["properties"]["cacheNode"]["autoUpdateRingType"]
            hasAutoUpdateRing = result["properties"]["cacheNode"]["autoUpdateRingType"]
        except KeyError:
            pass

        if hasAutoUpdateRing is not None:
            if str(hasAutoUpdateRing) == "Slow":
                try:
                    cleanOutput["autoUpdateWeek"] = result["properties"]["cacheNode"]["autoUpdateRequestedWeek"]
                except KeyError:
                    pass

                try:
                    cleanOutput["autoUpdateDay"] = result["properties"]["cacheNode"]["autoUpdateRequestedDay"]
                except KeyError:
                    pass

                try:
                    cleanOutput["autoUpdateTime"] = result["properties"]["cacheNode"]["autoUpdateRequestedTime"]
                except KeyError:
                    pass

        if has_value(args.expanded):
            try:
                cleanOutput["cacheNodeStateDetails"] = result["properties"]["additionalCacheNodeProperties"]["cacheNodeStateDetailedText"]
            except KeyError:
                pass

            try:
                cleanOutput["location"] = result["properties"]["location"]
            except KeyError:
                pass

        return cleanOutput


class MccEntNodeGetProvisioningDetails(_MccEntNodeGetProvisioningDetails):
    @classmethod
    def _build_arguments_schema(cls, *args, **kwargs):
        args_schema = super()._build_arguments_schema(*args, **kwargs)

        return args_schema

    def _output(self, *args, **kwargs):
        result = self.deserialize_output(self.ctx.vars.instance, client_flatten=True, secret_hidden=False)
        args = self.ctx.args

        ShowOutput = None

        try:
            from .aaz.latest.mcc.ent.node._show import Show
            ShowOutput = Show(cli_ctx=self.cli_ctx)(command_args={
                "cache_node_name": args.cache_node_name,
                "mcc_resource_name": args.mcc_resource_name,
                "resource_group": args.resource_group
            })
        except:
            err_msg = "Cache node get-provisioning-details failed. CLI could not find the specified MCC cache node resource with name \'" + str(args.cache_node_name) + "\'."
            raise CLIError(err_msg)

        cleanOutput = {}

        if ShowOutput is not None:
            try:
                driveArray = ShowOutput["properties"]["additionalCacheNodeProperties"]["driveConfiguration"]
                cleanDriveArray = []
                for drive in driveArray:
                    cleanDrive = {"physicalPath": drive["physicalPath"], "sizeInGb": drive["sizeInGb"]}
                    cleanDriveArray.append(cleanDrive)
                cleanOutput["driveConfiguration"] = cleanDriveArray
            except KeyError:
                pass

            try:
                proxyUrl = ShowOutput["properties"]["additionalCacheNodeProperties"]["proxyUrlConfiguration"]["proxyUrl"]
                proxyUrlParts = proxyUrl.split(":")
                if len(proxyUrlParts) == 2:
                    proxyConfiguration = {"proxyHostName": proxyUrlParts[0], "proxyPort": proxyUrlParts[1]}
                    cleanOutput["proxyConfiguration"] = proxyConfiguration
                else:
                    proxyConfiguration = {"proxyHostName": ShowOutput["properties"]["additionalCacheNodeProperties"]["proxyUrlConfiguration"]["proxyUrl"]}
                    cleanOutput["proxyConfiguration"] = proxyConfiguration
            except KeyError:
                pass

            try:
                cleanOutput["cacheNodeState"] = ShowOutput["properties"]["additionalCacheNodeProperties"]["cacheNodeStateShortText"]
            except KeyError:
                pass

        try:
            cleanOutput["customerId"] = result["properties"]["customerId"]
        except KeyError:
            pass

        try:
            cleanOutput["cacheNodeId"] = result["properties"]["cacheNodeId"]
        except KeyError:
            pass

        try:
            cleanOutput["customerKey"] = result["properties"]["primaryAccountKey"]
        except KeyError:
            pass

        try:
            cleanOutput["registrationKey"] = result["properties"]["registrationKey"]
        except KeyError:
            pass

        return cleanOutput
