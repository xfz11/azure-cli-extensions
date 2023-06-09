from azure.identity import AzureCliCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient
import requests
import json
import time
from azure.cli.core.azclierror import CLIInternalError

def get_resource_client(subscription_id):
    credential = AzureCliCredential()
    subscription_id = subscription_id
    resource_client = ResourceManagementClient(credential, subscription_id)
    return resource_client

def get_storage_client(subscription_id):
    credential = AzureCliCredential()
    storage_client = StorageManagementClient(credential, subscription_id)
    return storage_client

def get_resource_group_list(resource_client):
    group_list = list(resource_client.resource_groups.list())

    groups = []
    for group in group_list[:5]:
        groups.append(f"{'{'}\n\"id\": \"{group.id}\",\n\"location\": \"{group.location}\", \n\"name\": \"{group.name}\"\n{'}'}")
    
    group_list_str = "\n".join(groups)
    # add default?
    return group_list_str, list(group_list)[0].name

def get_app_service_plan_list(resource_client, resource_group):
    plan_list = list(resource_client.resources.list_by_resource_group(resource_group, filter = "resourceType eq 'Microsoft.Web/serverFarms'"))

    plans = []
    for plan in plan_list[:5]:
        plans.append(f"{'{'}\n\"id\": \"{plan.id}\",\n\"location\": \"{plan.location}\", \n\"kind\": \"{plan.kind}\", \n\"sku\": {'{'}\n \"tier\": \"{plan.sku.tier}\"\n{'}'}\n{'}'}")
    
    plan_list_str = "\n".join(plans)
    # add default?
    return plan_list_str

def get_storage_sku_list(storage_client):
    sku_list = list(storage_client.skus.list())
    skus = []

    for sku in sku_list[:5]:
        locations = "[\"" +  "\", \"".join(sku.locations) + "\"]"
        skus.append(f"{'{'}\n\"name\": \"{sku.name}\", \n\"kind\": \"{sku.kind}\", \n\"tier\": \"{sku.tier}\", \n \"locations\": {locations}\n{'}'}")
    
    sku_list_str = "\n".join(skus)
    return sku_list_str

def get_app_id_list(resource_client, resource_group):
    app_list = list(resource_client.resources.list_by_resource_group(resource_group, filter = "resourceType eq 'Microsoft.Web/sites'"))

    apps = []
    for app in app_list:
        apps.append(f"\"id\": \"{app.id}\"")
    return apps

def get_source_resource_id_list(source_resource_type, resource_client, rg_name):
    if source_resource_type == "web app":
        return get_app_id_list(resource_client, rg_name)
    else:
        print("Waiting for future release.")

def get_storage_id_list(resource_client, rg_name):
    storage_list = list(resource_client.resources.list_by_resource_group(rg_name, filter = "resourceType eq 'Microsoft.Storage/storageAccounts'"))

    storages = []
    for storage in storage_list:
        storages.append(f"\"id\": \"{storage.id}\"")
    return storages

def get_target_resource_id_list(target_resource_type, resource_client, rg_name):
    if target_resource_type == "storage":
        return get_storage_id_list(resource_client, rg_name)
    else:
        print("Waiting for future release.")

def get_resource_id_list(source_resource_type, target_resource_type, subscription_id, rg_name):
    resource_client = get_resource_client(subscription_id)
    return get_source_resource_id_list(source_resource_type, resource_client, rg_name) + get_target_resource_id_list(target_resource_type, resource_client, rg_name)

def run_cli_cmd(cmd, retry=0, interval=0, should_retry_func=None):
    '''Run a CLI command
        :param cmd: The CLI command to be executed
        :param retry: The times to re-try
        :param interval: The seconds wait before retry
    '''
    import subprocess
    output = subprocess.run(cmd, shell=True, check=False,
                            stderr=subprocess.PIPE, stdout=subprocess.PIPE)

    if output.returncode != 0 or (should_retry_func and should_retry_func(output)):
        if retry:
            time.sleep(interval)
            return run_cli_cmd(cmd, retry - 1, interval)
        err = output.stderr.decode(encoding='UTF-8', errors='ignore')
        raise CLIInternalError('Command execution failed, command is: ' + '{}, error message is: \n {}'.format(cmd, err))
    try:
        return json.loads(output.stdout.decode(encoding='UTF-8', errors='ignore')) if output.stdout else None
    except ValueError as e:
        return output.stdout or None

def create_resource(payload):
    payload = json.loads(payload)
    if "linkerName" in payload:
        uri = payload["resourceUri"] + "/providers/Microsoft.ServiceLinker/linkers/" + payload["linkerName"] + "?api-version=" + payload["api-version"]
    else:
        uri = payload["id"]
    uri = "https://management.azure.com" + uri

    cmd = "az rest --method put --url " + uri + " --body \"" + str(payload["payload"]) + "\""
    run_cli_cmd(cmd)
