# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import struct
import sys
from knack.log import get_logger
from knack.prompting import prompt_y_n, NoTTYException
from msrestazure.tools import parse_resource_id
from azure.cli.core.azclierror import (
    AzureConnectionError,
    ValidationError,
    CLIInternalError,
    ResourceNotFoundError
)
from azure.cli.core.extension.operations import _install_deps_for_psycopg2, _run_pip
from azure.cli.core._profile import Profile
from azure.cli.command_modules.serviceconnector._utils import (
    run_cli_cmd,
    generate_random_string,
    is_packaged_installed,
    get_object_id_of_current_user
)
from azure.cli.command_modules.serviceconnector._resource_config import (
    RESOURCE,
    AUTH_TYPE
)
from azure.cli.command_modules.serviceconnector._validators import (
    get_source_resource_name,
    get_target_resource_name,
)

logger = get_logger(__name__)

AUTHTYPES = {
    AUTH_TYPE.SystemIdentity: 'systemAssignedIdentity',
    AUTH_TYPE.UserIdentity: 'userAssignedIdentity',
    AUTH_TYPE.ServicePrincipalSecret: 'servicePrincipalSecret',
    AUTH_TYPE.UserAccount: 'userAccount',
}
IP_ADDRESS_CHECKER = 'https://api.ipify.org'
OPEN_ALL_IP_MESSAGE = 'Do you want to enable access for all IPs to allow local environment connecting to database?'


# pylint: disable=line-too-long, consider-using-f-string
# For db(mysqlFlex/psql/psqlFlex/sql) linker with auth type=systemAssignedIdentity, enable AAD auth and create db user on data plane
# For other linker, ignore the steps
def get_enable_mi_for_db_linker_func(yes=False):

    def enable_mi_for_db_linker(cmd, source_id, target_id, auth_info, client_type, connection_name):
        # return if connection is not for db mi
        if auth_info['auth_type'] not in [AUTHTYPES[AUTH_TYPE.SystemIdentity],
                                          AUTHTYPES[AUTH_TYPE.UserIdentity],
                                          AUTHTYPES[AUTH_TYPE.UserAccount],
                                          AUTHTYPES[AUTH_TYPE.ServicePrincipalSecret]
                                          ]:
            return None

        source_type = get_source_resource_name(cmd)
        target_type = get_target_resource_name(cmd)
        source_handler = getSourceHandler(source_id, source_type)
        if source_handler is None:
            return None
        target_handler = getTargetHandler(
            cmd, target_id, target_type, auth_info, client_type, connection_name, skip_prompt=yes)
        if target_handler is None:
            return None

        user_object_id = auth_info.get('principal_id') if auth_info['auth_type'] == AUTHTYPES[AUTH_TYPE.UserAccount] else None
        if user_object_id is None:
            user_object_id = get_object_id_of_current_user()

        if user_object_id is None:
            raise Exception(
                "No object id for current user {}".format(target_handler.login_username))

        target_handler.user_object_id = user_object_id
        if auth_info['auth_type'] == AUTHTYPES[AUTH_TYPE.SystemIdentity]:
            # enable source mi
            source_object_id = source_handler.get_identity_pid()
            target_handler.identity_object_id = source_object_id
            try:
                identity_info = run_cli_cmd(
                    'az ad sp show --id {}'.format(source_object_id), 15, 10)
                target_handler.identity_client_id = identity_info.get(
                    'appId')
                target_handler.identity_name = identity_info.get(
                    'displayName')
            except CLIInternalError as e:
                if 'AADSTS530003' in e.error_msg:
                    logger.warning(
                        'Please ask your IT department for help to join this device to Azure Active Directory.')
                raise e
        elif auth_info['auth_type'] == AUTHTYPES[AUTH_TYPE.UserIdentity]:
            mi_client_id = auth_info.get('client_id')
            mi_sub_id = auth_info.get('subscription_id')
            umi_info = run_cli_cmd(
                f'az identity list --subscription {mi_sub_id} --query "[?clientId==\'{mi_client_id}\']"')
            if umi_info is None or len(umi_info) == 0:
                raise ResourceNotFoundError(
                    "No identity found for client id {}".format(mi_client_id))
            source_object_id = umi_info[0].get('principalId')
            target_handler.identity_object_id = source_object_id
            target_handler.identity_client_id = mi_client_id
            target_handler.identity_name = umi_info[0].get('name')
        elif auth_info['auth_type'] == AUTHTYPES[AUTH_TYPE.ServicePrincipalSecret]:
            sp_client_id = auth_info.get('client_id')
            sp_object_id = auth_info.get('principal_id')
            try:
                sp_info = run_cli_cmd(
                    'az ad sp show --id {}'.format(sp_client_id))
                if sp_info is None:
                    raise ResourceNotFoundError(
                        "Not found the service principal with client id {}".format(sp_client_id))
                target_handler.identity_object_id = sp_object_id
                target_handler.identity_client_id = sp_client_id
                target_handler.identity_name = sp_info.get('displayName')
            except CLIInternalError as e:
                if 'AADSTS530003' in e.error_msg:
                    logger.warning(
                        'Please ask your IT department for help to join this device to Azure Active Directory.')
                raise e

        # enable target aad authentication and set login user as db aad admin
        target_handler.enable_target_aad_auth()
        target_handler.set_user_admin(
            user_object_id, mysql_identity_id=auth_info.get('mysql-identity-id'))

        # create an aad user in db
        target_handler.create_aad_user()
        return target_handler.get_auth_config(user_object_id)

    return enable_mi_for_db_linker


# pylint: disable=no-self-use, unused-argument, too-many-instance-attributes
def getTargetHandler(cmd, target_id, target_type, auth_info, client_type, connection_name, skip_prompt):
    if target_type in {RESOURCE.Sql}:
        return SqlHandler(cmd, target_id, target_type, auth_info, connection_name, skip_prompt)
    if target_type in {RESOURCE.Postgres}:
        return PostgresSingleHandler(cmd, target_id, target_type, auth_info, connection_name, skip_prompt)
    if target_type in {RESOURCE.PostgresFlexible}:
        return PostgresFlexHandler(cmd, target_id, target_type, auth_info, connection_name, skip_prompt)
    if target_type in {RESOURCE.MysqlFlexible}:
        return MysqlFlexibleHandler(cmd, target_id, target_type, auth_info, connection_name, skip_prompt)
    return None


class TargetHandler:
    cmd = None
    auth_type = ""
    auth_info = None

    tenant_id = ""
    subscription = ""
    resource_group = ""
    target_id = ""
    target_type = ""
    endpoint = ""

    login_username = ""
    login_usertype = ""  # servicePrincipal, user
    user_object_id = ""
    aad_username = ""

    identity_name = ""
    identity_client_id = ""
    identity_object_id = ""

    connection_name = ""

    skip_prompt = False

    def __init__(self, cmd, target_id, target_type, auth_info, connection_name, skip_prompt):
        self.cmd = cmd
        self.target_id = target_id
        self.target_type = target_type
        self.tenant_id = Profile(
            cli_ctx=cmd.cli_ctx).get_subscription().get("tenantId")
        target_segments = parse_resource_id(target_id)
        self.subscription = target_segments.get('subscription')
        self.resource_group = target_segments.get('resource_group')
        self.auth_type = auth_info['auth_type']
        self.auth_info = auth_info
        self.login_username = run_cli_cmd(
            'az account show').get("user").get("name")
        self.login_usertype = run_cli_cmd(
            'az account show').get("user").get("type")
        if (self.login_usertype not in ['servicePrincipal', 'user']):
            raise CLIInternalError(
                f'{self.login_usertype} is not supported. Please login as user or servicePrincipal')
        self.aad_username = "aad_" + connection_name
        self.connection_name = connection_name
        self.skip_prompt = skip_prompt

    def enable_target_aad_auth(self):
        return

    def set_user_admin(self, user_object_id, **kwargs):
        return

    def set_target_firewall(self, is_add, ip_name, start_ip=None, end_ip=None):
        return

    def create_aad_user(self):
        return

    def get_auth_flag(self):
        if self.auth_type == AUTHTYPES[AUTH_TYPE.UserAccount]:
            return '--user-account'
        if self.auth_type == AUTHTYPES[AUTH_TYPE.SystemIdentity]:
            return '--system-identity'
        if self.auth_type == AUTHTYPES[AUTH_TYPE.UserIdentity]:
            return '--user-identity'
        if self.auth_type == AUTHTYPES[AUTH_TYPE.ServicePrincipalSecret]:
            return '--service-principal'
        return None

    def get_auth_config(self, user_object_id):
        if self.auth_type == AUTHTYPES[AUTH_TYPE.UserAccount]:
            return {
                'auth_type': self.auth_type,
                'username': self.aad_username,
                'principal_id': user_object_id
            }
        if self.auth_type == AUTHTYPES[AUTH_TYPE.SystemIdentity]:
            return {
                'auth_type': self.auth_type,
                'username': self.aad_username,
            }
        if self.auth_type == AUTHTYPES[AUTH_TYPE.UserIdentity]:
            return {
                'auth_type': self.auth_type,
                'username': self.aad_username,
                'client_id': self.identity_client_id,
                'subscription_id': self.auth_info['subscription_id'],
            }
        if self.auth_type == AUTHTYPES[AUTH_TYPE.ServicePrincipalSecret]:
            return {
                'auth_type': self.auth_type,
                'username': self.aad_username,
                'principal_id': self.identity_object_id,
                'client_id': self.identity_client_id,
                'secret': self.auth_info['secret'],
            }
        return None


class MysqlFlexibleHandler(TargetHandler):

    server = ""
    dbname = ""

    def __init__(self, cmd, target_id, target_type, auth_info, connection_name, skip_prompt):
        super().__init__(cmd, target_id, target_type,
                         auth_info, connection_name, skip_prompt)
        self.endpoint = cmd.cli_ctx.cloud.suffixes.mysql_server_endpoint
        target_segments = parse_resource_id(target_id)
        self.server = target_segments.get('name')
        self.dbname = target_segments.get('child_name_1')

    def set_user_admin(self, user_object_id, **kwargs):
        mysql_identity_id = kwargs['mysql_identity_id']
        admins = run_cli_cmd(
            'az mysql flexible-server ad-admin list -g {} -s {} --subscription {}'.format(
                self.resource_group, self.server, self.subscription)
        )
        is_admin = any(ad.get('sid') == user_object_id for ad in admins)
        if is_admin:
            return

        logger.warning('Set current user as DB Server AAD Administrators.')
        # set user as AAD admin
        if mysql_identity_id is None:
            raise ValidationError(
                "Provide '{} mysql-identity-id=<user-assigned managed identity ID>' to update AAD authentication.".format(
                    self.get_auth_flag()))
        mysql_umi = run_cli_cmd(
            'az mysql flexible-server identity list -g {} -s {} --subscription {}'.format(self.resource_group, self.server, self.subscription))
        if (not mysql_umi) or (not mysql_umi.get("userAssignedIdentities")) or mysql_identity_id not in mysql_umi.get("userAssignedIdentities"):
            run_cli_cmd('az mysql flexible-server identity assign -g {} -s {} --subscription {} --identity {}'.format(
                self.resource_group, self.server, self.subscription, mysql_identity_id))
        run_cli_cmd('az mysql flexible-server ad-admin create -g {} -s {} --subscription {} -u {} -i {} --identity {}'.format(
            self.resource_group, self.server, self.subscription, self.login_username, user_object_id, mysql_identity_id))

    def create_aad_user(self):
        query_list = self.get_create_query()
        connection_kwargs = self.get_connection_string()
        ip_name = generate_random_string(prefix='svc_').lower()
        try:
            logger.warning("Connecting to database...")
            self.create_aad_user_in_mysql(connection_kwargs, query_list)
        except AzureConnectionError as e:
            logger.warning(e)
            # allow local access
            from requests import get
            ip_address = get(IP_ADDRESS_CHECKER).text
            self.set_target_firewall(True, ip_name, ip_address, ip_address)
            # create again
            try:
                self.create_aad_user_in_mysql(connection_kwargs, query_list)
            except AzureConnectionError as e:
                logger.warning(e)
                try:
                    if not self.skip_prompt:
                        if not prompt_y_n(OPEN_ALL_IP_MESSAGE):
                            raise AzureConnectionError(
                                "Please confirm local environment can connect to database and try again.") from e
                except NoTTYException as e:
                    raise CLIInternalError(
                        'Unable to prompt for confirmation as no tty available. Use --yes.') from e
                # allow public access
                self.set_target_firewall(
                    True, ip_name, '0.0.0.0', '255.255.255.255')
                # create again
                self.create_aad_user_in_mysql(connection_kwargs, query_list)
            finally:
                self.set_target_firewall(False, ip_name)

    def set_target_firewall(self, is_add, ip_name, start_ip=None, end_ip=None):
        if is_add:
            target = run_cli_cmd(
                'az mysql flexible-server show --ids {}'.format(self.target_id))
            if target.get('network').get('publicNetworkAccess') == "Disabled":
                raise AzureConnectionError(
                    "The target resource doesn't allow public access. Connection can't be created.")
            logger.warning("Add firewall rule %s %s - %s...%s", ip_name, start_ip, end_ip,
                           ('(it will be removed after connection is created)' if self.auth_type != AUTHTYPES[
                               AUTH_TYPE.UserAccount] else '(Please delete it manually if it has security risk.)'))
            run_cli_cmd(
                'az mysql flexible-server firewall-rule create --resource-group {0} --name {1} --rule-name {2} '
                '--subscription {3} --start-ip-address {4} --end-ip-address {5}'.format(
                    self.resource_group, self.server, ip_name, self.subscription, start_ip, end_ip)
            )
        else:
            if self.auth_type == AUTHTYPES[AUTH_TYPE.UserAccount]:
                return
            logger.warning(
                "Remove database server firewall rule %s to recover...", ip_name)
            try:
                run_cli_cmd(
                    'az mysql flexible-server firewall-rule delete --resource-group {0} --name {1} --rule-name {2} '
                    '--subscription {3} --yes'.format(
                        self.resource_group, self.server, ip_name, self.subscription)
                )
            except CLIInternalError as e:
                logger.warning(
                    "Can't remove firewall rule %s. Please manually delete it to avoid security issue. %s", ip_name, str(e))

    def create_aad_user_in_mysql(self, connection_kwargs, query_list):
        if not is_packaged_installed('pymysql'):
            _run_pip(["install", "pymysql"])
        # pylint: disable=import-error
        try:
            import pymysql
            from pymysql.constants import CLIENT
        except ModuleNotFoundError as e:
            raise CLIInternalError(
                "Dependency pymysql can't be installed, please install it manually with `" + sys.executable + " -m pip install pymysql`.") from e

        connection_kwargs['client_flag'] = CLIENT.MULTI_STATEMENTS
        try:
            connection = pymysql.connect(**connection_kwargs)
            logger.warning(
                "Adding new AAD user %s to database...", self.aad_username)
            cursor = connection.cursor()
            for q in query_list:
                if q:
                    try:
                        logger.debug(q)
                        cursor.execute(q)
                    except Exception as e:  # pylint: disable=broad-except
                        logger.warning(
                            "Query %s, error: %s", q, str(e))
        except pymysql.Error as e:
            raise AzureConnectionError(
                "Fail to connect mysql. " + str(e)) from e
        if cursor is not None:
            try:
                cursor.close()
            except Exception as e:  # pylint: disable=broad-except
                raise CLIInternalError(
                    "Connection close failed." + str(e)) from e

    def get_connection_string(self):
        password = run_cli_cmd(
            'az account get-access-token --resource-type oss-rdbms').get('accessToken')

        return {
            'host': self.server + self.endpoint,
            'database': self.dbname,
            'user': self.login_username,
            'password': password,
            'ssl': {"fake_flag_to_enable_tls": True},
            'autocommit': True
        }

    def get_create_query(self):
        client_id = self.identity_client_id
        if self.auth_type == AUTHTYPES[AUTH_TYPE.UserAccount]:
            client_id = self.user_object_id
        return [
            "SET aad_auth_validate_oids_in_tenant = OFF;",
            "DROP USER IF EXISTS '{}'@'%';".format(self.aad_username),
            "CREATE AADUSER '{}' IDENTIFIED BY '{}';".format(
                self.aad_username, client_id),
            "GRANT ALL PRIVILEGES ON `{}`.* TO '{}'@'%';".format(
                self.dbname, self.aad_username),
            "FLUSH privileges;"
        ]


class SqlHandler(TargetHandler):

    server = ""
    dbname = ""
    ip = ""

    def __init__(self, cmd, target_id, target_type, auth_info, connection_name, skip_prompt):
        super().__init__(cmd, target_id, target_type,
                         auth_info, connection_name, skip_prompt)
        self.endpoint = cmd.cli_ctx.cloud.suffixes.sql_server_hostname
        target_segments = parse_resource_id(target_id)
        self.server = target_segments.get('name')
        self.dbname = target_segments.get('child_name_1')

    def set_user_admin(self, user_object_id, **kwargs):
        # pylint: disable=not-an-iterable
        admins = run_cli_cmd(
            'az sql server ad-admin list --ids {}'.format(self.target_id))
        is_admin = any(ad.get('sid') == user_object_id for ad in admins)
        if not is_admin:
            logger.warning('Setting current user as database server AAD admin:'
                           ' user=%s object id=%s', self.login_username, user_object_id)
            run_cli_cmd('az sql server ad-admin create -g {} --server-name {} --display-name {} --object-id {} --subscription {}'.format(
                self.resource_group, self.server, self.login_username, user_object_id, self.subscription)).get('objectId')

    def create_aad_user(self):

        query_list = self.get_create_query()
        connection_args = self.get_connection_string()
        ip_name = generate_random_string(prefix='svc_').lower()
        try:
            logger.warning("Connecting to database...")
            self.create_aad_user_in_sql(connection_args, query_list)
        except AzureConnectionError as e:
            if not self.ip:
                raise e
            logger.warning(e)
            # allow local access
            ip_address = self.ip
            self.set_target_firewall(True, ip_name, ip_address, ip_address)
            try:
                # create again
                self.create_aad_user_in_sql(connection_args, query_list)
            except AzureConnectionError as e:
                logger.warning(e)
                raise AzureConnectionError(
                    "Please confirm local environment can connect to database and try again.") from e
            finally:
                self.set_target_firewall(False, ip_name)

    def set_target_firewall(self, is_add, ip_name, start_ip=None, end_ip=None):
        if is_add:
            target = run_cli_cmd(
                'az sql server show --ids {}'.format(self.target_id))
            # logger.warning("Update database server firewall rule to connect...")
            if target.get('publicNetworkAccess') == "Disabled":
                raise AzureConnectionError(
                    "The target resource doesn't allow public access. Please enable it manually and try again.")
            logger.warning("Add firewall rule %s %s - %s...%s", ip_name, start_ip, end_ip,
                           ('(it will be removed after connection is created)' if self.auth_type != AUTHTYPES[
                               AUTH_TYPE.UserAccount] else '(Please delete it manually if it has security risk.)'))
            run_cli_cmd(
                'az sql server firewall-rule create -g {0} -s {1} -n {2} '
                '--subscription {3} --start-ip-address {4} --end-ip-address {5}'.format(
                    self.resource_group, self.server, ip_name, self.subscription, start_ip, end_ip)
            )
        else:
            if self.auth_type == AUTHTYPES[AUTH_TYPE.UserAccount]:
                return
            logger.warning(
                "Remove database server firewall rule %s to recover...", ip_name)
            try:
                run_cli_cmd(
                    'az sql server firewall-rule delete -g {0} -s {1} -n {2} --subscription {3}'.format(
                        self.resource_group, self.server, ip_name, self.subscription)
                )
            except CLIInternalError as e:
                logger.warning(
                    "Can't remove firewall rule %s. Please manually delete it to avoid security issue. %s", ip_name, str(e))

    def create_aad_user_in_sql(self, connection_args, query_list):

        if not is_packaged_installed('pyodbc'):
            _run_pip(["install", "pyodbc"])

        # pylint: disable=import-error, c-extension-no-member
        try:
            import pyodbc
        except ModuleNotFoundError as e:
            raise CLIInternalError(
                "Dependency pyodbc can't be installed, please install it manually with `" + sys.executable + " -m pip install pyodbc`.") from e
        drivers = [x for x in pyodbc.drivers() if x in [
            'ODBC Driver 17 for SQL Server', 'ODBC Driver 18 for SQL Server']]
        if not drivers:
            raise CLIInternalError(
                "Please manually install odbc 17/18 for SQL server, reference: https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server/")
        try:
            with pyodbc.connect(connection_args.get("connection_string").format(driver=drivers[0]), attrs_before=connection_args.get("attrs_before")) as conn:
                with conn.cursor() as cursor:
                    logger.warning(
                        "Adding new AAD user %s to database...", self.aad_username)
                    for execution_query in query_list:
                        try:
                            logger.debug(execution_query)
                            cursor.execute(execution_query)
                        except pyodbc.ProgrammingError as e:
                            logger.warning(e)
                        conn.commit()
        except pyodbc.Error as e:
            import re
            search_ip = re.search(
                "Client with IP address '(.*?)' is not allowed to access the server", str(e))
            if search_ip is not None:
                self.ip = search_ip.group(1)
            raise AzureConnectionError("Fail to connect sql." + str(e)) from e

    def get_connection_string(self):
        token_bytes = run_cli_cmd(
            'az account get-access-token --output json --resource https://database.windows.net/').get('accessToken').encode('utf-16-le')

        token_struct = struct.pack(
            f'<I{len(token_bytes)}s', len(token_bytes), token_bytes)
        # This connection option is defined by microsoft in msodbcsql.h
        SQL_COPT_SS_ACCESS_TOKEN = 1256
        conn_string = 'DRIVER={{{driver}}};server=' + \
            self.server + self.endpoint + ';database=' + self.dbname + ';'
        logger.debug(conn_string)
        return {'connection_string': conn_string, 'attrs_before': {SQL_COPT_SS_ACCESS_TOKEN: token_struct}}

    def get_create_query(self):
        if self.auth_type in [AUTHTYPES[AUTH_TYPE.SystemIdentity], AUTHTYPES[AUTH_TYPE.UserIdentity], AUTHTYPES[AUTH_TYPE.ServicePrincipalSecret]]:
            self.aad_username = self.identity_name
        if self.auth_type == AUTHTYPES[AUTH_TYPE.UserAccount]:
            self.aad_username = self.login_username
        role_q = "CREATE USER \"{}\" FROM EXTERNAL PROVIDER;".format(
            self.aad_username)
        grant_q = "GRANT CONTROL ON DATABASE::{} TO \"{}\";".format(
            self.dbname, self.aad_username)

        return [role_q, grant_q]


class PostgresFlexHandler(TargetHandler):

    db_server = ""
    host = ""
    dbname = ""
    ip = ""

    def __init__(self, cmd, target_id, target_type, auth_info, connection_name, skip_prompt):
        super().__init__(cmd, target_id, target_type,
                         auth_info, connection_name, skip_prompt)
        self.endpoint = cmd.cli_ctx.cloud.suffixes.postgresql_server_endpoint
        target_segments = parse_resource_id(target_id)
        self.db_server = target_segments.get('name')
        self.host = self.db_server + self.endpoint
        self.dbname = target_segments.get('child_name_1')

    def enable_target_aad_auth(self):
        target = run_cli_cmd(
            'az postgres flexible-server show --ids {}'.format(self.target_id))
        if target.get('authConfig').get('activeDirectoryAuth') == "Enabled":
            return
        run_cli_cmd('az postgres flexible-server update -g {} -n {} --subscription {} --active-directory-auth Enabled'.format(
            self.resource_group, self.db_server, self.subscription))

    def set_user_admin(self, user_object_id, **kwargs):
        admins = run_cli_cmd('az postgres flexible-server ad-admin list -g {} -s {} --subscription {}'.format(
            self.resource_group, self.db_server, self.subscription))

        is_admin = any(user_object_id in u.get("objectId", "") for u in admins)
        if is_admin:
            return
        logger.warning('Set current user as DB Server AAD Administrators.')
        run_cli_cmd('az postgres flexible-server ad-admin create -u {} -i {} -g {} -s {} --subscription {}'.format(
            self.login_username, user_object_id, self.resource_group, self.db_server, self.subscription))

    def create_aad_user(self):
        query_list = self.get_create_query()
        connection_string = self.get_connection_string()
        ip_name = generate_random_string(prefix='svc_').lower()

        try:
            logger.warning("Connecting to database...")
            self.create_aad_user_in_pg(connection_string, query_list)
        except AzureConnectionError as e:
            logger.warning(e)
            # allow local access
            from requests import get
            ip_address = self.ip or get(IP_ADDRESS_CHECKER).text
            self.set_target_firewall(True, ip_name, ip_address, ip_address)
            try:
                # create again
                self.create_aad_user_in_pg(connection_string, query_list)
            except AzureConnectionError as e:
                logger.warning(e)
                try:
                    if not self.skip_prompt:
                        if not prompt_y_n(OPEN_ALL_IP_MESSAGE):
                            raise AzureConnectionError(
                                "Please confirm local environment can connect to database and try again.") from e
                except NoTTYException as e:
                    raise CLIInternalError(
                        'Unable to prompt for confirmation as no tty available. Use --yes.') from e
                self.set_target_firewall(
                    True, ip_name, '0.0.0.0', '255.255.255.255')
                # create again
                self.create_aad_user_in_pg(connection_string, query_list)
            finally:
                self.set_target_firewall(False, ip_name)

    def set_target_firewall(self, is_add, ip_name, start_ip=None, end_ip=None):
        if is_add:
            target = run_cli_cmd(
                'az postgres flexible-server show --ids {}'.format(self.target_id))
            if target.get('network').get('publicNetworkAccess') == "Disabled":
                raise AzureConnectionError(
                    "The target resource doesn't allow public access. Connection can't be created.")
            logger.warning("Add firewall rule %s %s - %s...%s", ip_name, start_ip, end_ip,
                           ('(it will be removed after connection is created)' if self.auth_type != AUTHTYPES[
                               AUTH_TYPE.UserAccount] else '(Please delete it manually if it has security risk.)'))
            run_cli_cmd(
                'az postgres flexible-server firewall-rule create --resource-group {0} --name {1} --rule-name {2} '
                '--subscription {3} --start-ip-address {4} --end-ip-address {5}'.format(
                    self.resource_group, self.db_server, ip_name, self.subscription, start_ip, end_ip)
            )
        else:
            if self.auth_type == AUTHTYPES[AUTH_TYPE.UserAccount]:
                return
            logger.warning(
                "Remove database server firewall rule %s to recover...", ip_name)
            try:
                run_cli_cmd(
                    'az postgres flexible-server firewall-rule delete --resource-group {0} --name {1} --rule-name {2} '
                    '--subscription {3} --yes'.format(
                        self.resource_group, self.db_server, ip_name, self.subscription)
                )
            except CLIInternalError as e:
                logger.warning(
                    "Can't remove firewall rule %s. Please manually delete it to avoid security issue. %s", ip_name, str(e))

    def create_aad_user_in_pg(self, conn_string, query_list):
        if not is_packaged_installed('psycopg2'):
            _install_deps_for_psycopg2()
            _run_pip(["install", "psycopg2"])
        # pylint: disable=import-error
        try:
            import psycopg2
        except ModuleNotFoundError as e:
            raise CLIInternalError(
                "Dependency psycopg2 can't be installed, please install it manually with `" + sys.executable + " -m pip install psycopg2-binary`.") from e

        # pylint: disable=protected-access
        try:
            conn = psycopg2.connect(conn_string)
        except (psycopg2.Error, psycopg2.OperationalError) as e:
            import re
            # logger.warning(e)
            search_ip = re.search(
                'no pg_hba.conf entry for host "(.*)", user ', str(e))
            if search_ip is not None:
                self.ip = search_ip.group(1)
            raise AzureConnectionError(
                "Fail to connect to postgresql. " + str(e)) from e

        conn.autocommit = True
        cursor = conn.cursor()
        logger.warning("Adding new AAD user %s to database...",
                       self.aad_username)
        for execution_query in query_list:
            if execution_query:
                try:
                    logger.debug(execution_query)
                    cursor.execute(execution_query)
                except psycopg2.Error as e:  # role "aad_user" already exists
                    logger.warning(e)

        # Clean up
        conn.commit()
        cursor.close()
        conn.close()

    def get_connection_string(self):
        password = run_cli_cmd(
            'az account get-access-token --resource-type oss-rdbms').get('accessToken')

        # extension functions require the extension to be available, which is the case for postgres (default) database.
        conn_string = "host={} user={} dbname=postgres password={} sslmode=require".format(
            self.host, self.login_username, password)
        return conn_string

    def get_create_query(self):
        object_type = 'service'
        object_id = self.identity_object_id
        if self.auth_type == AUTHTYPES[AUTH_TYPE.UserAccount]:
            object_id = self.user_object_id
            object_type = 'user'
        return [
            # 'drop role IF EXISTS "{0}";'.format(self.aad_username),
            "select * from pgaadauth_create_principal_with_oid('{0}', '{1}', '{2}', false, false);".format(
                self.aad_username, object_id, object_type),
            'GRANT ALL PRIVILEGES ON DATABASE "{0}" TO "{1}";'.format(
                self.dbname, self.aad_username),
            'GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO "{}";'.format(
                self.aad_username),
            'GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO "{}";'.format(
                self.aad_username)]


class PostgresSingleHandler(PostgresFlexHandler):

    def enable_target_aad_auth(self):
        return

    def set_user_admin(self, user_object_id, **kwargs):
        sub = self.subscription
        rg = self.resource_group
        server = self.db_server
        is_admin = True

        # pylint: disable=not-an-iterable
        admins = run_cli_cmd(
            'az postgres server ad-admin list --ids {}'.format(self.target_id))
        is_admin = any(ad.get('sid') == user_object_id for ad in admins)
        if not is_admin:
            logger.warning('Setting current user as database server AAD admin:'
                           ' user=%s object id=%s', self.login_username, user_object_id)
            run_cli_cmd('az postgres server ad-admin create -g {} --server-name {} --display-name {} --object-id {}'
                        ' --subscription {}'.format(rg, server, self.login_username, user_object_id, sub)).get('objectId')

    def set_target_firewall(self, is_add, ip_name, start_ip=None, end_ip=None):
        sub = self.subscription
        rg = self.resource_group
        server = self.db_server
        target_id = self.target_id
        if is_add:
            target = run_cli_cmd(
                'az postgres server show --ids {}'.format(target_id))
            if target.get('publicNetworkAccess') == "Disabled":
                raise AzureConnectionError(
                    "The target resource doesn't allow public access. Please enable it manually and try again.")
            logger.warning("Add firewall rule %s %s - %s...%s", ip_name, start_ip, end_ip,
                           ('(it will be removed after connection is created)' if self.auth_type != AUTHTYPES[
                               AUTH_TYPE.UserAccount] else '(Please delete it manually if it has security risk.)'))
            run_cli_cmd(
                'az postgres server firewall-rule create -g {0} -s {1} -n {2} --subscription {3}'
                ' --start-ip-address {4} --end-ip-address {5}'.format(
                    rg, server, ip_name, sub, start_ip, end_ip)
            )
        else:
            if self.auth_type == AUTHTYPES[AUTH_TYPE.UserAccount]:
                return
            logger.warning(
                "Remove database server firewall rule %s to recover...", ip_name)
            try:
                run_cli_cmd(
                    'az postgres server firewall-rule delete -g {0} -s {1} -n {2} -y'.format(rg, server, ip_name))
            except CLIInternalError as e:
                logger.warning(
                    "Can't remove firewall rule %s. Please manually delete it to avoid security issue. %s", ip_name, str(e))

    def get_connection_string(self):
        password = run_cli_cmd(
            'az account get-access-token --resource-type oss-rdbms').get('accessToken')

        # extension functions require the extension to be available, which is the case for postgres (default) database.
        conn_string = "host={} user={} dbname={} password={} sslmode=require".format(
            self.host, self.login_username + '@' + self.db_server, self.dbname, password)
        return conn_string

    def get_create_query(self):
        client_id = self.identity_client_id
        if self.auth_type == AUTHTYPES[AUTH_TYPE.UserAccount]:
            client_id = self.user_object_id
        return [
            'SET aad_validate_oids_in_tenant = off;',
            # 'drop role IF EXISTS "{0}";'.format(self.aad_username),
            "CREATE ROLE \"{0}\" WITH LOGIN PASSWORD '{1}' IN ROLE azure_ad_user;".format(
                self.aad_username, client_id),
            'GRANT ALL PRIVILEGES ON DATABASE "{0}" TO "{1}";'.format(
                self.dbname, self.aad_username),
            'GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO "{}";'.format(
                self.aad_username),
            'GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO "{}";'.format(
                self.aad_username)
        ]


def getSourceHandler(source_id, source_type):
    if source_type in {RESOURCE.WebApp}:
        return WebappHandler(source_id, source_type)
    if source_type in {RESOURCE.ContainerApp}:
        return ContainerappHandler(source_id, source_type)
    if source_type in {RESOURCE.SpringCloud, RESOURCE.SpringCloudDeprecated}:
        return SpringHandler(source_id, source_type)
    if source_type in {RESOURCE.Local}:
        return LocalHandler(source_id, source_type)
    return None


# pylint: disable=too-few-public-methods
class SourceHandler:
    source_id = ""
    source_type = ""

    def __init__(self, source_id, source_type: RESOURCE):
        self.source_id = source_id
        self.source_type = source_type.value

    def get_identity_pid(self):
        return


def output_is_none(output):
    return not output.stdout


class LocalHandler(SourceHandler):
    def get_identity_pid(self):
        pass


class SpringHandler(SourceHandler):
    def get_identity_pid(self):
        segments = parse_resource_id(self.source_id)
        sub = segments.get('subscription')
        spring = segments.get('name')
        app = segments.get('child_name_1')
        rg = segments.get('resource_group')
        logger.warning(
            'Checking if Spring app enables System Identity...')
        identity = run_cli_cmd('az {} app identity show -g {} -s {} -n {} --subscription {}'.format(
            self.source_type, rg, spring, app, sub))
        if (identity is None or identity.get('type') != "SystemAssigned"):
            # assign system identity for spring-cloud
            logger.warning('Enabling Spring app System Identity...')
            run_cli_cmd(
                'az {} app identity assign -g {} -s {} -n {} --subscription {}'.format(
                    self.source_type, rg, spring, app, sub))

            identity = run_cli_cmd('az {} app identity show -g {} -s {} -n {} --subscription {}'.format(
                self.source_type, rg, spring, app, sub), 15, 5, output_is_none)

        if identity is None:
            raise CLIInternalError(
                "Unable to get system identity of Spring. Please try it later.")
        return identity.get('principalId')


class WebappHandler(SourceHandler):
    def get_identity_pid(self):
        logger.warning('Checking if WebApp enables System Identity...')
        identity = run_cli_cmd(
            'az webapp identity show --ids {}'.format(self.source_id))
        if (identity is None or "SystemAssigned" not in identity.get('type')):
            # assign system identity for spring-cloud
            logger.warning('Enabling WebApp System Identity...')
            run_cli_cmd(
                'az webapp identity assign --ids {}'.format(self.source_id))

            identity = run_cli_cmd(
                'az webapp identity show --ids {}'.format(self.source_id), 15, 5, output_is_none)

        if identity is None:
            raise CLIInternalError(
                "Unable to get system identity of Web App. Please try it later.")
        return identity.get('principalId')


class ContainerappHandler(SourceHandler):
    def get_identity_pid(self):
        logger.warning('Checking if Container App enables System Identity...')
        identity = run_cli_cmd(
            'az containerapp identity show --ids {}'.format(self.source_id))
        if (identity is None or "SystemAssigned" not in identity.get('type')):
            # assign system identity for spring-cloud
            logger.warning('Enabling Container App System Identity...')
            run_cli_cmd(
                'az containerapp identity assign --ids {} --system-assigned'.format(self.source_id))
            identity = run_cli_cmd(
                'az containerapp identity show --ids {}'.format(self.source_id), 15, 5, output_is_none)

        if identity is None:
            raise CLIInternalError(
                "Unable to get system identity of Container App. Please try it later.")
        return identity.get('principalId')
