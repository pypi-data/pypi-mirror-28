import logging
import paramiko
import re
import atexit
from collections import namedtuple
from actappliance.connections.connection import ApplianceConnection


ssh_out = namedtuple('ssh_output', ['out', 'err', 'status'])


class ApplianceSsh(ApplianceConnection):
    def __init__(self, system, connect_args, call_timeout=6 * 60 * 60):
        super(ApplianceSsh, self).__init__()
        self.logger = logging.getLogger(__name__)

        self.system = system
        self.connect_args = connect_args if connect_args is not None else {}
        self.timeout = call_timeout
        # SSH delimiter to use during uds commands
        self.SSH_DELIM = '|MiLeD|'

        # set in method 'connect'
        self.ssh_client = None

    def connect(self):
        """
        Connect to an appliance, disable timeouts and return the ssh object.
        :return: paramiko ssh object
        """
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(self.system, **self.connect_args)
        except paramiko.SSHException:
            self.logger.exception("Failed to connect to {}".format(self.system))
            raise
        _, out, _ = ssh.exec_command("unset TMOUT")
        rc = out.channel.recv_exit_status()
        if rc != 0:
            raise RuntimeError("Return code of 'unset TMOUT was {}.".format(rc))
        self.ssh_client = ssh

        # Close this connection after execution
        atexit.register(self.disconnect)

    def disconnect(self):
        try:
            self.ssh_client.close()
        except (AttributeError, NameError):
            logging.debug("No ssh client to close.")
        self.ssh_client = None

    def prep_cmd(self, operation, **update_cmds):
        """
        :return: ActCmd object with ssh_command attribute
        """
        prepared_command = self.ActCmd(operation, **update_cmds)
        prepared_command.ssh_command = self.params_to_cli(operation, **update_cmds)
        return prepared_command

    def call(self, command_obj):
        """
        Use when you explicitly want to connect over ssh and send raw ssh commands.

        This houses the functionality unlike rest method because I want to avoid passing around the client to retain
        channels.

        :param command_obj: Instance of ActCmd object
        :return: stdout, stderr, exit status
        """
        if not self.ssh_client:
            self.connect()

        stdin_chan, stdout_chan, stderr_chan = self.ssh_client.exec_command(command_obj.ssh_command)
        stdin_chan.close()

        # Wait for exit_status
        exit_status = stdout_chan.channel.recv_exit_status()

        # get output from channelfiles
        stdout = stdout_chan.readlines()
        stderr = stderr_chan.readlines()
        self.logger.debug('stderr: \n{}'.format(stderr))
        self.logger.debug("exit status: {}".format(exit_status))
        command_obj.call_result = ssh_out(out=stdout, err=stderr, status=exit_status)

    def post_cmd(self, command_obj):
        command_obj.result = self.convert_ssh_output(command_obj.call_result.out, command_obj.call_result.err)
        return super(ApplianceSsh, self).post_cmd(command_obj)

    def raw(self, ssh_command, statuses=None):
        """
        Send an ssh command with the only processing being newline stripping.

        Threaded timeouts still apply to `raw`. If you need absolute individual control use method `call`.

        :param ssh_command: command to send
        :param statuses: list of acceptable exit statuses
        :return: namedtuple ssh_output
        """
        c = self.ActCmd(ssh_command)
        self.timeout_call(c)
        # Grab the unprocessed call_result before it reaches post_cmd_handler
        assert c.call_result
        out = [line.rstrip('\n') for line in c.call_result.out]
        err = [line.rstrip('\n') for line in c.call_result.err]
        # c.call_result.status -> <ssh/rest encapsulation object>.<named tuple>.<ssh exit status>
        output = ssh_out(out=out, err=err, status=c.call_result.status)

        if statuses and output.status not in statuses:
            self.logger.debug("Failed stdout:\n{}\nFailed stderr:\n{}".format(output.out, output.err))
            raise RuntimeError("Exit status of command {} was {}; only {} accepted.".format(
                ssh_command, output.status, ','.join(str(s) for s in statuses))
            )

        return output

    def params_to_cli(self, operation, **update_cmds):
        """
        Takes a functional cli operation and appends rest like inputs.

        ex.
          self.cmd('udsinfo lshost', filtervalue='ostype=Linux')
        returns:
          "/act/bin/udsinfo lshost -filtervalue 'ostype=Linux'"
        :param operation: A functional cli operation
        :param update_cmds:
        :return:
        """
        cli_command = operation.partition(' ')[0]
        if 'udsinfo' in cli_command:
            cli_command = '/act/bin/udsinfo'
        elif 'udstask' in cli_command:
            cli_command = '/act/bin/udstask'
        elif 'sainfo' in cli_command:
            cli_command = '/act/bin/sainfo'
        else:
            raise ValueError("Actifio appliance doesn't support command {}, accepted values "
                             "(udsinfo, udstask, sainfo)".format(cli_command))
        body = operation.partition(' ')[2]

        # add parameters to body
        for k, v in update_cmds.items():
            # don't pass None params
            if v is not None:
                parameter = "-{}".format(k)
                # handle parameterless switches
                if v is True:
                    value = ''
                else:
                    value = " '{}'".format(v)
                option = "{}{}".format(parameter, value)
                body += ' {}'.format(option)
        if 'udsinfo' in cli_command and body.startswith(('ls', 'list')):
            body += " -delim '{}'".format(self.SSH_DELIM)
        full_operation = "{} {}".format(cli_command, body)
        return full_operation

    def convert_ssh_output(self, stdout, stderr):
        self.logger.debug('Parsing stdout: {}'.format(stdout))
        rest_like_result = {}
        # First format stderr
        if stderr:
            error_code = re.match("(?:ACTERR-)(\d+)", stderr[0]).group(1)
            error_message = re.match("(?:ACTERR-\d+ )(.+)", stderr[0]).group(1)
            rest_like_result['errorcode'] = error_code
            rest_like_result['errormessage'] = error_message
        # Now format stdout
        try:
            # Handle udsinfo commands that start with ls
            if self.SSH_DELIM in stdout[0]:
                self.logger.info('Ssh operation contains delim, grabbing header.')
                headers = stdout[0].split(self.SSH_DELIM)
                values = [row.split(self.SSH_DELIM) for row in stdout[1:]]
                # Make the result list like JSON response
                result_list = []
                for row in values:
                    result_list.append(dict(zip(headers, row)))
                rest_like_result['result'] = result_list
            else:
                # Handle all other udsinfo commands
                # only return a list if there is more than one item, else return a string (see exception)
                if stdout[1]:
                    rest_like_result = {'result': stdout}
                # TODO Handle commands that match "udsinfo -h | egrep -v '^\s*ls'"
        except IndexError:
            try:
                # return single item response as a string
                rest_like_result['result'] = stdout[0]
            except IndexError:
                # return "[]" if stdout was empty, matching standard rest response
                rest_like_result['result'] = stdout
        self.logger.debug("Converted cli result: {}".format(rest_like_result))
        return rest_like_result
