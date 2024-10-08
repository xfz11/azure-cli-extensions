# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#
# Code generated by aaz-dev-tools
# --------------------------------------------------------------------------------------------

from azure.cli.testsdk import (ScenarioTest, JMESPathCheck, ResourceGroupPreparer)
import time


class ElasticSanScenario(ScenarioTest):
    @ResourceGroupPreparer(location='eastus2euap', name_prefix='clitest.rg.testelasticsan')
    def test_elastic_san_scenarios(self, resource_group):
        self.kwargs.update({
            "san_name": self.create_random_name('elastic-san', 24)
        })
        self.cmd('az elastic-san create -n {san_name} -g {rg} --tags {{key1810:aaaa}} -l eastus2euap '
                 '--base-size-tib 23 --extended-capacity-size-tib 14 '
                 '--sku {{name:Premium_LRS,tier:Premium}} --public-network-access Enabled',
                 checks=[JMESPathCheck('name', self.kwargs.get('san_name', '')),
                         JMESPathCheck('location', "eastus2euap"),
                         JMESPathCheck('tags', {"key1810": "aaaa"}),
                         JMESPathCheck('baseSizeTiB', 23),
                         JMESPathCheck('extendedCapacitySizeTiB', 14),
                         JMESPathCheck('sku', {"name": "Premium_LRS",
                                               "tier": "Premium"}),
                         JMESPathCheck('publicNetworkAccess', "Enabled")])
        self.cmd('az elastic-san show -g {rg} -n {san_name}',
                 checks=[JMESPathCheck('name', self.kwargs.get('san_name', '')),
                         JMESPathCheck('location', "eastus2euap"),
                         JMESPathCheck('tags', {"key1810": "aaaa"}),
                         JMESPathCheck('baseSizeTiB', 23),
                         JMESPathCheck('extendedCapacitySizeTiB', 14),
                         JMESPathCheck('sku', {"name": "Premium_LRS", "tier": "Premium"})
                         ])
        self.cmd('az elastic-san list -g {rg}', checks=[JMESPathCheck('length(@)', 1)])
        self.cmd('az elastic-san list-sku')
        self.cmd('az elastic-san update -n {san_name} -g {rg} --tags {{key1710:bbbb}} '
                 '--base-size-tib 25 --extended-capacity-size-tib 15 --public-network-access Disabled',
                 checks=[JMESPathCheck('name', self.kwargs.get('san_name', '')),
                         JMESPathCheck('tags', {"key1710": "bbbb"}),
                         JMESPathCheck('baseSizeTiB', 25),
                         JMESPathCheck('extendedCapacitySizeTiB', 15),
                         JMESPathCheck('publicNetworkAccess', "Disabled")])
        self.cmd('az elastic-san delete -g {rg} -n {san_name} -y')
        time.sleep(20)
        self.cmd('az elastic-san list -g {rg}', checks=[JMESPathCheck('length(@)', 0)])

    @ResourceGroupPreparer(location='eastus2euap', name_prefix='clitest.rg.testelasticsan.volumegroup')
    def test_elastic_san_volume_group_and_volume_scenarios(self, resource_group):
        self.kwargs.update({
            "san_name": self.create_random_name('elastic-san', 24),
            "vg_name": self.create_random_name('volume-group', 24),
            "vnet_name": self.create_random_name('vnet', 24),
            "subnet_name": self.create_random_name('subnet', 24),
            "subnet_name_2": self.create_random_name('subnet', 24),
            "volume_name": self.create_random_name('volume', 24)
        })
        self.cmd('az elastic-san create -n {san_name} -g {rg} --tags {{key1810:aaaa}} -l eastus2euap '
                 '--base-size-tib 23 --extended-capacity-size-tib 14 '
                 '--sku {{name:Premium_LRS,tier:Premium}}')
        subnet_id = self.cmd('az network vnet create -g {rg} -n {vnet_name} --address-prefix 10.0.0.0/16 '
                             '--subnet-name {subnet_name} '
                             '--subnet-prefix 10.0.0.0/24').get_output_in_json()["newVNet"]["subnets"][0]["id"]
        self.kwargs.update({"subnet_id": subnet_id})
        self.cmd('az elastic-san volume-group create -e {san_name} -n {vg_name} -g {rg} '
                 '--encryption EncryptionAtRestWithPlatformKey --protocol-type Iscsi '
                 '--network-acls {{virtual-network-rules:[{{id:{subnet_id},action:Allow}}]}} '
                 '--enforce-data-integrity-check-for-iscsi true')
        self.cmd('az elastic-san volume-group show -g {rg} -e {san_name} -n {vg_name}',
                 checks=[JMESPathCheck('name', self.kwargs.get('vg_name', '')),
                         JMESPathCheck('encryption', "EncryptionAtRestWithPlatformKey"),
                         JMESPathCheck('protocolType', "iSCSI"),
                         JMESPathCheck('networkAcls', {"virtualNetworkRules": [{
                             "action": "Allow",
                             "id": subnet_id,
                             "resourceGroup": self.kwargs.get('rg', '')}]}),
                         JMESPathCheck('enforceDataIntegrityCheckForIscsi', True)])
        self.cmd('az elastic-san volume-group list -g {rg} -e {san_name}', checks=[JMESPathCheck('length(@)', 1)])

        subnet_id_2 = self.cmd('az network vnet subnet create -g {rg} --vnet-name {vnet_name} --name {subnet_name_2} '
                               '--address-prefixes 10.0.1.0/24 '
                               '--service-endpoints Microsoft.Storage').get_output_in_json()["id"]
        self.kwargs.update({"subnet_id_2": subnet_id_2})
        self.cmd('az elastic-san volume-group update -e {san_name} -n {vg_name} -g {rg} '
                 '--protocol-type None '
                 '--network-acls {{virtual-network-rules:[{{id:{subnet_id_2},action:Allow}}]}} '
                 '--enforce-data-integrity-check-for-iscsi false',
                 checks=[JMESPathCheck('protocolType', "None"),
                         JMESPathCheck('networkAcls.virtualNetworkRules[0].id', subnet_id_2),
                         JMESPathCheck('enforceDataIntegrityCheckForIscsi', False)])

        self.cmd('az elastic-san volume create -g {rg} -e {san_name} -v {vg_name} -n {volume_name} --size-gib 2')
        self.cmd('az elastic-san volume show -g {rg} -e {san_name} -v {vg_name} -n {volume_name}',
                 checks=[JMESPathCheck('name', self.kwargs.get('volume_name', '')),
                         JMESPathCheck('sizeGiB', 2)])
        self.cmd('az elastic-san volume list -g {rg} -e {san_name} -v {vg_name}',
                 checks=[JMESPathCheck('length(@)', 1)])
        self.cmd('az elastic-san volume update -g {rg} -e {san_name} -v {vg_name} -n {volume_name} --size-gib 3',
                 checks=[JMESPathCheck('sizeGiB', 3)])
        self.cmd('az elastic-san volume delete -g {rg} -e {san_name} -v {vg_name} -n {volume_name} -y')
        self.cmd('az elastic-san volume list -g {rg} -e {san_name} -v {vg_name}',
                 checks=[JMESPathCheck('length(@)', 0)])

        self.cmd('az elastic-san volume-group delete -g {rg} -e {san_name} -n {vg_name} -y')
        time.sleep(20)
        self.cmd('az elastic-san delete -g {rg} -n {san_name} -y')

    @ResourceGroupPreparer(location='eastus2euap', name_prefix='clitest.rg.testelasticsan.snapshot')
    def test_elastic_san_snapshot_scenarios(self, resource_group):
        self.kwargs.update({
            "san_name": self.create_random_name('elastic-san', 24),
            "vnet_name": self.create_random_name('vnet', 24),
            "subnet_name": self.create_random_name('subnet', 24),
            "vg_name": self.create_random_name('volume-group', 24),
            "volume_name": self.create_random_name('volume', 24),
            "volume_name_2": self.create_random_name('volume', 24),
            "snapshot_name": self.create_random_name('snapshot', 24),
            "snapshot2_name": self.create_random_name('snapshot', 24),
            "snapshot3_name": self.create_random_name('snapshot', 24)
        })
        self.cmd('az elastic-san create -n {san_name} -g {rg} --tags {{key1810:aaaa}} -l eastus2euap '
                 '--base-size-tib 23 --extended-capacity-size-tib 14 '
                 '--sku {{name:Premium_LRS,tier:Premium}}')
        self.cmd('az network vnet create -g {rg} -n {vnet_name} --address-prefix 10.0.0.0/16')
        subnet_id = self.cmd('az network vnet subnet create -g {rg} --vnet-name {vnet_name} --name {subnet_name} '
                             '--address-prefixes 10.0.0.0/24 '
                             '--service-endpoints Microsoft.Storage').get_output_in_json()["id"]
        self.kwargs.update({"subnet_id": subnet_id})
        self.cmd('az elastic-san volume-group create -e {san_name} -n {vg_name} -g {rg} '
                 '--encryption EncryptionAtRestWithPlatformKey --protocol-type Iscsi '
                 '--network-acls {{virtual-network-rules:[{{id:{subnet_id},action:Allow}}]}}')
        self.cmd('az elastic-san volume create -g {rg} -e {san_name} -v {vg_name} -n {volume_name} --size-gib 2')
        volume_id = self.cmd('az elastic-san volume show -g {rg} -e {san_name} -v {vg_name} '
                             '-n {volume_name}').get_output_in_json()["id"]
        self.kwargs.update({"volume_id": volume_id})
        self.cmd('az elastic-san volume snapshot create -g {rg} -e {san_name} -v {vg_name} -n {snapshot_name} '
                 '--creation-data {{source-id:{volume_id}}}')
        self.cmd('az elastic-san volume snapshot show -g {rg} -e {san_name} -v {vg_name} -n {snapshot_name}',
                 checks=[JMESPathCheck('name', self.kwargs.get('snapshot_name', '')),
                         JMESPathCheck('creationData.sourceId', self.kwargs.get("volume_id"))])
        self.cmd('az elastic-san volume snapshot list -g {rg} -e {san_name} -v {vg_name}',
                 checks=[JMESPathCheck('length(@)', 1)])
        self.cmd('az elastic-san volume snapshot delete -g {rg} -e {san_name} -v {vg_name} -n {snapshot_name} -y')
        self.cmd('az elastic-san volume snapshot list -g {rg} -e {san_name} -v {vg_name}',
                 checks=[JMESPathCheck('length(@)', 0)])

        self.cmd('az elastic-san volume snapshot create -g {rg} -e {san_name} -v {vg_name} -n {snapshot2_name} '
                 '--creation-data {{source-id:{volume_id}}}')
        snapshot_id = self.cmd('az elastic-san volume snapshot show -g {rg} -e {san_name} -v {vg_name} '
                               '-n {snapshot2_name}').get_output_in_json()["id"]
        self.kwargs.update({"snapshot_id": snapshot_id})
        self.cmd('az elastic-san volume create -g {rg} -e {san_name} -v {vg_name} -n {volume_name_2} --size-gib 2 '
                 '--creation-data {{source-id:{snapshot_id},create-source:VolumeSnapshot}}')
        self.cmd('az elastic-san volume snapshot list -g {rg} -e {san_name} -v {vg_name}',
                 checks=[JMESPathCheck('length(@)', 1)])
        self.cmd('az elastic-san volume delete -g {rg} -e {san_name} -v {vg_name} -n {volume_name_2} -y ')
        self.cmd('az elastic-san volume delete -g {rg} -e {san_name} -v {vg_name} -n {volume_name} -y '
                 '--x-ms-delete-snapshots true --x-ms-force-delete true')
        self.cmd('az elastic-san volume snapshot list -g {rg} -e {san_name} -v {vg_name}',
                 checks=[JMESPathCheck('length(@)', 0)])
        self.cmd('az elastic-san volume-group delete -g {rg} -e {san_name} -n {vg_name} -y')
        time.sleep(20)
        self.cmd('az elastic-san delete -g {rg} -n {san_name} -y')

    @ResourceGroupPreparer(location='eastus2euap', name_prefix='clitest.rg.testelasticsan.cmk.sai.')
    def test_elastic_san_customer_managed_key_system_assigned_identity_scenarios(self, resource_group):
        logged_in_user = self.cmd('ad signed-in-user show').get_output_in_json()
        logged_in_user = logged_in_user["id"] if logged_in_user is not None else "a7250e3a-0e5e-48e2-9a34-45f1f5e1a91e"
        self.kwargs.update({
            "san_name": self.create_random_name('elastic-san', 24),
            "kv_name": self.create_random_name('keyvault', 24),
            "key_name": self.create_random_name('key', 24),
            "logged_in_user": logged_in_user,
            "vnet_name": self.create_random_name('vnet', 24),
            "subnet_name": self.create_random_name('subnet', 24),
            "vg_name": self.create_random_name('volume-group', 24),
            "volume_name": self.create_random_name('volume', 24)
        })
        self.cmd('az elastic-san create -n {san_name} -g {rg} --tags {{key1810:aaaa}} -l eastus2euap '
                 '--base-size-tib 23 --extended-capacity-size-tib 14 '
                 '--sku {{name:Premium_LRS,tier:Premium}}')
        # 1. Create a key vault with a key in it. Key type should be RSA
        self.cmd('az keyvault create --name {kv_name} --resource-group {rg} --location eastus2 '
                 '--enable-purge-protection --retention-days 7 --enable-rbac-authorization false')
        kv = self.cmd('az keyvault show --name {kv_name} --resource-group {rg}').get_output_in_json()
        self.kwargs.update({"vault_uri": kv["properties"]["vaultUri"]})
        self.cmd('az keyvault set-policy -n {kv_name} --object-id {logged_in_user} '
                 '--key-permissions backup create delete get import get list update restore ')
        self.cmd('az keyvault key create --vault-name {kv_name} -n {key_name} --protection software')
        # 2. PUT a volume group with PMK and a system assigned identity with it
        vg = self.cmd('az elastic-san volume-group create -e {san_name} -n {vg_name} -g {rg} '
                      '--encryption EncryptionAtRestWithPlatformKey --protocol-type Iscsi --identity '
                      '{{type:SystemAssigned}}',
                      checks=[JMESPathCheck('encryption', "EncryptionAtRestWithPlatformKey"),
                              JMESPathCheck('identity.type', "SystemAssigned")]).get_output_in_json()
        vg_identity_principal_id = vg["identity"]["principalId"]
        self.kwargs.update({"vg_identity_principal_id": vg_identity_principal_id})
        # 3. Get the system identity's principalId from the response of PUT volume group request.
        # Grant access to  the system assigned identity to the key vault created in  step1
        # (key permissions: Get, Unwrap Key, Wrap Key)
        self.cmd('az keyvault set-policy -n {kv_name} --object-id {vg_identity_principal_id} '
                 '--key-permissions backup create delete get import get list update restore get wrapkey unwrapkey')
        # 4. PATCH the volume group with the key created in step 1
        self.cmd("az elastic-san volume-group update -e {san_name} -n {vg_name} -g {rg} "
                 "--encryption EncryptionAtRestWithCustomerManagedKey --encryption-properties "
                 "\"{{key-vault-properties:{{key-name:{key_name},key-vault-uri:\'{vault_uri}\'}}}}\"",
                 checks=[JMESPathCheck('encryption', "EncryptionAtRestWithCustomerManagedKey"),
                         JMESPathCheck('encryptionProperties.keyVaultProperties.keyVaultUri', self.kwargs.get("vault_uri")),
                         JMESPathCheck('encryptionProperties.keyVaultProperties.keyName', self.kwargs.get("key_name")),
                         ]).get_output_in_json()
        self.cmd('az elastic-san volume create -g {rg} -e {san_name} -v {vg_name} -n {volume_name} --size-gib 2')
        self.cmd('az elastic-san volume delete -g {rg} -e {san_name} -v {vg_name} -n {volume_name} -y')
        self.cmd('az elastic-san volume-group delete -g {rg} -e {san_name} -n {vg_name} -y')
        time.sleep(20)
        self.cmd('az elastic-san delete -g {rg} -n {san_name} -y')

    @ResourceGroupPreparer(location='eastus2euap', name_prefix='clitest.rg.testelasticsan.cmk.uai.')
    def test_elastic_san_customer_managed_key_user_assigned_identity_scenarios(self, resource_group):
        logged_in_user = self.cmd('ad signed-in-user show').get_output_in_json()
        logged_in_user = logged_in_user["id"] if logged_in_user is not None else "a7250e3a-0e5e-48e2-9a34-45f1f5e1a91e"
        self.kwargs.update({
            "san_name": self.create_random_name('elastic-san', 24),
            "kv_name": self.create_random_name('keyvault', 24),
            "key_name": self.create_random_name('key', 24),
            "user_assigned_identity_name": self.create_random_name('uai', 24),
            "user_assigned_identity_name_2": self.create_random_name('uai', 24),
            "logged_in_user": logged_in_user,
            "vnet_name": self.create_random_name('vnet', 24),
            "subnet_name": self.create_random_name('subnet', 24),
            "vg_name": self.create_random_name('volume-group', 24),
            "volume_name": self.create_random_name('volume', 24)
        })
        self.cmd('az elastic-san create -n {san_name} -g {rg} --tags {{key1810:aaaa}} -l eastus2euap '
                 '--base-size-tib 23 --extended-capacity-size-tib 14 '
                 '--sku {{name:Premium_LRS,tier:Premium}}')
        # 1. Create a user assigned identity and grant it the access to the key vault
        uai = self.cmd('az identity create -g {rg} -n {user_assigned_identity_name}').get_output_in_json()
        self.kwargs.update({"uai_principal_id": uai["principalId"],
                            "uai_id": uai["id"],
                            "uai_client_id": uai["clientId"]})
        self.cmd('az keyvault create --name {kv_name} --resource-group {rg} --location eastus2 '
                 '--enable-purge-protection --retention-days 7 --enable-rbac-authorization false')
        kv = self.cmd('az keyvault show --name {kv_name} --resource-group {rg}').get_output_in_json()
        self.kwargs.update({"vault_uri": kv["properties"]["vaultUri"]})
        self.cmd('az keyvault set-policy -n {kv_name} --object-id {uai_principal_id} '
                 '--key-permissions get wrapkey unwrapkey ')
        self.cmd('az keyvault key create --vault-name {kv_name} -n {key_name} --protection software')
        # 2.PUT a volume group with CMK
        self.cmd("az elastic-san volume-group create -e {san_name} -n {vg_name} -g {rg} "
                 "--encryption EncryptionAtRestWithCustomerManagedKey --protocol-type Iscsi --identity "
                 "{{type:UserAssigned,user-assigned-identity:{uai_id}}} --encryption-properties "
                 "\"{{key-vault-properties:{{key-name:{key_name},key-vault-uri:\'{vault_uri}\'}},"
                 "identity:{{user-assigned-identity:{uai_id}}}}}\"",
                 checks=[JMESPathCheck('encryption', "EncryptionAtRestWithCustomerManagedKey"),
                         JMESPathCheck('encryptionProperties.keyVaultProperties.keyVaultUri',
                                       self.kwargs.get("vault_uri")),
                         JMESPathCheck('encryptionProperties.keyVaultProperties.keyName',
                                       self.kwargs.get("key_name")),
                         JMESPathCheck('identity.type', "UserAssigned"),
                         JMESPathCheck('identity.userAssignedIdentities', {
                             self.kwargs.get("uai_id"): {
                                 "principalId": self.kwargs.get("uai_principal_id"),
                                 "clientId": self.kwargs.get("uai_client_id")
                             }}),
                         JMESPathCheck('encryptionProperties.identity.userAssignedIdentity',
                                       self.kwargs.get("uai_id")),
                         ]).get_output_in_json()
        self.cmd('az elastic-san volume create -g {rg} -e {san_name} -v {vg_name} -n {volume_name} --size-gib 2')
        # 3. Change to another user assigned identity
        uai_2 = self.cmd('az identity create -g {rg} -n {user_assigned_identity_name_2}').get_output_in_json()
        self.kwargs.update({"uai_2_principal_id": uai_2["principalId"],
                            "uai_2_id": uai_2["id"],
                            "uai_2_client_id": uai_2["clientId"]})
        self.cmd('az keyvault set-policy -n {kv_name} --object-id {uai_2_principal_id} '
                 '--key-permissions get wrapkey unwrapkey ')
        self.cmd("az elastic-san volume-group update -e {san_name} -n {vg_name} -g {rg} --identity "
                 "{{type:UserAssigned,user-assigned-identity:{uai_2_id}}} --encryption-properties "
                 "\"{{key-vault-properties:{{key-name:{key_name},key-vault-uri:\'{vault_uri}\'}},"
                 "identity:{{user-assigned-identity:{uai_2_id}}}}}\"",
                 checks=[JMESPathCheck('encryption', "EncryptionAtRestWithCustomerManagedKey"),
                         JMESPathCheck('identity.userAssignedIdentities', {
                             self.kwargs.get("uai_2_id"): {
                                 "principalId": self.kwargs.get("uai_2_principal_id"),
                                 "clientId": self.kwargs.get("uai_2_client_id")
                             }}),
                         JMESPathCheck('encryptionProperties.identity.userAssignedIdentity',
                                       self.kwargs.get("uai_2_id")),
                         ]).get_output_in_json()
        # 4. Change to pmk
        self.cmd("az elastic-san volume-group update -e {san_name} -n {vg_name} -g {rg} "
                 "--encryption EncryptionAtRestWithPlatformKey",
                 checks=[JMESPathCheck('encryption', "EncryptionAtRestWithPlatformKey"),
                         ]).get_output_in_json()

        # 5. Change to system assigned identity
        self.cmd("az elastic-san volume-group update -e {san_name} -n {vg_name} -g {rg} "
                 "--identity {{type:SystemAssigned}}",
                 checks=[JMESPathCheck('identity.type', "SystemAssigned")
                         ]).get_output_in_json()
