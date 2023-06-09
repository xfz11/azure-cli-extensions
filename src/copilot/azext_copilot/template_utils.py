from ._constants import CREATE_APP_TEMPLATE, CREATE_STORAGE_TEMPLATE, CREATE_CREATION_TEMPLATE, DEFAULT_RESOURCE_GROUP, DEFAULT_RESOURCE_GROUP_NAME
from .resource_utils import get_resource_client, get_storage_client, get_resource_group_list, get_app_service_plan_list, get_storage_sku_list, get_resource_id_list

def create_app_template(subscription_id, use_default=True):
    resource_client = get_resource_client(subscription_id)
    if not use_default:
        group_list, rg_name = get_resource_group_list(resource_client)
    else:
        group_list = DEFAULT_RESOURCE_GROUP
        rg_name = DEFAULT_RESOURCE_GROUP_NAME
    plan_list_str = get_app_service_plan_list(resource_client, rg_name)
    template = CREATE_APP_TEMPLATE.format(
        subscription_id=subscription_id,
        resource_group_list=group_list,
        app_service_plan_list=plan_list_str,
    )
    return template

def create_storage_template(subscription_id, use_default=True):
    storage_client = get_storage_client(subscription_id)
    if not use_default:
        resource_client = get_resource_client(subscription_id)
        group_list, _ = get_resource_group_list(resource_client)
    else:
        group_list = DEFAULT_RESOURCE_GROUP
    sku_list_str = get_storage_sku_list(storage_client)
    template = CREATE_STORAGE_TEMPLATE.format(
        subscription_id=subscription_id,
        resource_group_list=group_list,
        storage_sku_list=sku_list_str
    )
    return template

def create_connection_template(source_resource_type, target_resource_type, subscription_id, use_default=True):
    if not use_default:
        resource_client = get_resource_client(subscription_id)
        _, rg_name = get_resource_group_list(resource_client)
    else:
        rg_name = DEFAULT_RESOURCE_GROUP_NAME

    resource_id_list = get_resource_id_list(source_resource_type, target_resource_type, subscription_id, rg_name)
    print(len(resource_id_list))

    resource_id_list_str = "[{\n" + ",\n".join(resource_id_list) + "\n}]"
    template = CREATE_CREATION_TEMPLATE.format(resource_id_list=resource_id_list_str)

    return template

get_template = {
    'create resource': {
        'web app': create_app_template,
        'storage': create_storage_template,
    },
    'connect resources':create_connection_template
}
