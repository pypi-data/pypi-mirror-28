# Copyright (c) 2013 EMC Corporation
# All Rights Reserved
#
# This software contains the intellectual property of EMC Corporation
# or is licensed to EMC Corporation from third parties.  Use of this
# software and the intellectual property contained therein is expressly
# limited to the terms and conditions of the License Agreement under which
# it is provided by or on behalf of EMC.
import common
from common import SOSError


class ControlService(object):

    # URIs
    URI_CONTROL_CLUSTER_POWEROFF = '/control/cluster/poweroff'
    URI_CONTROL_NODE_REBOOT = '/control/node/reboot?node_id={0}'
    URI_CONTROL_SERVICE_RESTART = \
        '/control/service/restart?node_id={0}&name={1}'

    def __init__(self, ipAddr, port):
        '''
        Constructor: takes IP address and port of the ECS instance.
        These are needed to make http requests for REST API
        '''
        self.__ipAddr = ipAddr
        self.__port = port

    def rebootNode(self, nodeId):
        #START - rebootNode
        (s, h) = common.service_json_request(
            self.__ipAddr, self.__port,
            "POST",
            ControlService.URI_CONTROL_NODE_REBOOT.format(nodeId),
            None)
        if(not s):
            return None

        o = common.json_decode(s)
        print("response : " + o)
        return o
        #END - rebootNode

    def clusterPoweroff(self):
        #START - clusterPoweroff
        (s, h) = common.service_json_request(
            self.__ipAddr, self.__port,
            "POST",
            ControlService.URI_CONTROL_CLUSTER_POWEROFF,
            None)
        if(not s):
            return None

        o = common.json_decode(s)
        return o
        #END - clusterPoweroff

    def restartService(self, nodeId, serviceName):
        #START - restartService
        (s, h) = common.service_json_request(
            self.__ipAddr, self.__port,
            "POST",
            ControlService.URI_CONTROL_SERVICE_RESTART.format(
                nodeId, serviceName), None)
        if(not s):
            return None

        o = common.json_decode(s)
        return o
        #END - restartService


class Backup(object):

    URI_BACKUP_SET = "/backupset/backup?tag={0}"
    URI_BACKUP_SET_LIST = "/backupset/"
    URI_BACKUP_SET_DOWNLOAD = "/backupset/download?tag={0}"

    def __init__(self, ipAddr, port):
        '''
        Constructor: takes IP address and port of the ECS instance.
        These are needed to make http requests for REST API
        '''
        self.__ipAddr = ipAddr
        self.__port = port

    def create(self, name, force=False):

        request_uri = Backup.URI_BACKUP_SET.format(name)

        if(force is True):
            request_uri += '&force=true'

        (s, h) = common.service_json_request(
            self.__ipAddr, self.__port,
            "POST",
            request_uri, None)
        if(not s):
            return None

        o = common.json_decode(s)
        return o

    def delete(self, name):
        (s, h) = common.service_json_request(
            self.__ipAddr, self.__port,
            "DELETE",
            Backup.URI_BACKUP_SET.format(
            name), None)
        if(not s):
            return None

        o = common.json_decode(s)
        return o

    def list_backupsets(self):
        (s, h) = common.service_json_request(
            self.__ipAddr, self.__port,
            "GET",
            Backup.URI_BACKUP_SET_LIST, None)
        if(not s):
            return []
        o = common.json_decode(s)
        if (not o):
            return []
        if ('backupsets_info' in o
            and o['backupsets_info'] is not None
            and 'backupset' in o['backupsets_info']):
            result = o['backupsets_info']['backupset']
            if(result is None):
                return []
            elif isinstance(result, list):
                return result
            else:
                return [result]
        else:
            return []

    def download(self, name, filepath):

        if(filepath.endswith(".zip") is False):
            filepath += ".zip"

        (s, h) = common.service_json_request(
            self.__ipAddr, self.__port,
            "GET",
            Backup.URI_BACKUP_SET_DOWNLOAD.format(
            name), None,
                None, False, "application/octet-stream", filepath)
        if(not s):
            return None

        o = common.json_decode(s)
        return o

# START Parser definitions

'''
Parser for the restart-service command
'''


def restart_service_parser(subcommand_parsers, common_parser):
    # restart-service command parser
    restart_service_parser = subcommand_parsers.add_parser(
        'restart-service',
        description='ECS restart-service CLI usage',
        parents=[common_parser],
        conflict_handler='resolve',
        help='Restarts a service')

    mandatory_args = restart_service_parser.add_argument_group(
        'mandatory arguments')
    mandatory_args.add_argument(
        '-id', '-nodeid',
        help='Id of the node from which the service to be restarted',
        metavar='<nodeid>',
        dest='nodeid',
        required=True)
    mandatory_args.add_argument('-svc', '-servicename ',
                                dest='servicename',
                                metavar='<servicename>',
                                help='Name of the service to be restarted',
                                required=True)

    restart_service_parser.set_defaults(func=restart_service)


def restart_service(args):
    nodeId = args.nodeid
    serviceName = args.servicename

    try:
        response = common.ask_continue(
            "restart service:" +
            serviceName +
            " in node: " +
            nodeId)
        if(str(response) == "y"):
            contrlSvcObj = ControlService(args.ip, args.port)
            contrlSvcObj.restartService(nodeId, serviceName)
    except SOSError as e:
        common.format_err_msg_and_raise(
            "restart-service",
            serviceName +
            " in node: " +
            nodeId,
            e.err_text,
            e.err_code)


'''
Parser for the reboot node
'''


def reboot_node_parser(subcommand_parsers, common_parser):
    # create command parser
    reboot_node_parser = subcommand_parsers.add_parser(
        'reboot-node',
        description='ECS reboot-node CLI usage',
        parents=[common_parser],
        conflict_handler='resolve',
        help='Reboots the node')

    mandatory_args = reboot_node_parser.add_argument_group(
        'mandatory arguments')
    mandatory_args.add_argument('-id', '-nodeid',
                                help='Id of the node to be rebooted',
                                metavar='<nodeid>',
                                dest='nodeid',
                                required=True)

    reboot_node_parser.set_defaults(func=reboot_node)


def reboot_node(args):
    nodeId = args.nodeid

    try:
        response = common.ask_continue("reboot node:" + nodeId)
        if(str(response) == "y"):
            contrlSvcObj = ControlService(args.ip, args.port)
            contrlSvcObj.rebootNode(nodeId)
    except SOSError as e:
        common.format_err_msg_and_raise(
            "reboot-node",
            nodeId,
            e.err_text,
            e.err_code)


'''
Parser for the cluster poweroff
'''


def cluster_poweroff_parser(subcommand_parsers, common_parser):
    # create command parser
    cluster_poweroff_parser = subcommand_parsers.add_parser(
        'cluster-poweroff',
        description='ECS cluster-poweroff CLI usage',
        parents=[common_parser],
        conflict_handler='resolve',
        help='Power off the cluster')

    cluster_poweroff_parser.set_defaults(func=cluster_poweroff)


def cluster_poweroff(args):

    try:
        response = common.ask_continue("power-off the cluster")
        if(str(response) == "y"):
            contrlSvcObj = ControlService(args.ip, args.port)
            contrlSvcObj.clusterPoweroff()
    except SOSError as e:
        common.format_err_msg_and_raise(
            "cluster-poweroff",
            "",
            e.err_text,
            e.err_code)

'''
Parser function definitions for Backup CLI
'''


def create_backup_parser(subcommand_parsers, common_parser):
    create_backup_parser = subcommand_parsers.add_parser(
        'create-backup',
        description='ECS create backup CLI usage',
        parents=[common_parser],
        conflict_handler='resolve',
        help="Creates a ECS backup set.")
    mandatory_args = create_backup_parser.add_argument_group(
        'mandatory arguments')
    mandatory_args.add_argument('-name', '-n',
                help="Name of the backup. " +
                "It must not have '_' (underscore) character",
                metavar='<backup name>',
                dest='name',
                required=True)
    create_backup_parser.add_argument('-force',
                help='Create backup forcibly',
                action='store_true',
                dest='force')
    create_backup_parser.set_defaults(func=create_backup)


def create_backup(args):

    try:
        obj = Backup(args.ip, args.port)
        res = obj.create(args.name, args.force)
    except SOSError as e:
        common.format_err_msg_and_raise(
            'create', 'backup',
            e.err_text, e.err_code)


def delete_backup_parser(subcommand_parsers, common_parser):

    delete_backup_parser = subcommand_parsers.add_parser(
        'delete-backup',
        description='ECS delete backup CLI usage',
        parents=[common_parser],
        conflict_handler='resolve',
        help="Deletes a ECS backup set")
    mandatory_args = delete_backup_parser.add_argument_group(
        'mandatory arguments')
    mandatory_args.add_argument('-name', '-n',
                help='Name of the backup',
                metavar='<backup name>',
                dest='name',
                required=True)
    delete_backup_parser.set_defaults(func=delete_backup)


def delete_backup(args):

    try:
        obj = Backup(args.ip, args.port)
        res = obj.delete(args.name)
    except SOSError as e:
        common.format_err_msg_and_raise(
            'delete', 'backup',
            e.err_text, e.err_code)


def list_backup_parser(subcommand_parsers, common_parser):

    list_backup_parser = subcommand_parsers.add_parser(
        'list-backup',
        description='ECS list backup CLI usage',
        parents=[common_parser],
        conflict_handler='resolve',
        help="List all ECS backup set")
    list_backup_parser.add_argument('-v', '-verbose',
                                dest='verbose',
                                help='List backups with details',
                                action='store_true')
    list_backup_parser.set_defaults(func=list_backup)


def list_backup(args):

    try:
        obj = Backup(args.ip, args.port)
        res = obj.list_backupsets()
        if(len(res) > 0):
            if(args.verbose is True):
                return common.format_json_object(res)
            else:
                from datetime import datetime
                from common import TableGenerator
                for item in res:
                    value = datetime.fromtimestamp(float(item['create_time'])
                                                   / 1000)
                    item['creation_time'] = value.strftime('%Y-%m-%d %H:%M:%S')
                    item['size_in_mb'] = float(float(item['size'])
                                               / (1024 * 1024))

                TableGenerator(
                        res, ['name', 'size_in_mb',
                              'creation_time']).printTable()
    except SOSError as e:
        common.format_err_msg_and_raise(
            'list', 'backup',
            e.err_text, e.err_code)


def download_backup_parser(subcommand_parsers, common_parser):

    download_backup_parser = subcommand_parsers.add_parser(
        'download-backup',
        description='ECS download backup CLI usage',
        parents=[common_parser],
        conflict_handler='resolve',
        help="Download a ECS backup set")
    mandatory_args = download_backup_parser.add_argument_group(
        'mandatory arguments')
    mandatory_args.add_argument('-name', '-n',
                                help='Name of the backup',
                                metavar='<backup name>',
                                dest='name',
                                required=True)
    mandatory_args.add_argument('-filepath', '-fp',
                                help='Download file path',
                                metavar='<filepath>',
                                dest='filepath',
                                required=True)
    download_backup_parser.set_defaults(func=download_backup)


def download_backup(args):

    try:
        obj = Backup(args.ip, args.port)
        res = obj.download(args.name, args.filepath)
    except SOSError as e:
        common.format_err_msg_and_raise(
            'download', 'backup',
            e.err_text, e.err_code)
