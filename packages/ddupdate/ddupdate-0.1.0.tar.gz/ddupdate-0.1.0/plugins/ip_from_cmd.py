"""
ddupdate plugin supporting getting ip address from a command.

See: ddupdate(8)

"""

import re
import subprocess

from ddupdate.ddplugin import IpPlugin, IpLookupError, dict_of_opts


class IpV4FromCmdPlugin(IpPlugin):
    """
    Use ip4 address obtained from a command.

    The command is invoked without parameters, and should return a single
    ip address on stdout. Anything which is not parsed as an ipv4 address
    is treated as an error message.

    Note that when invoked in a systemd context, the environment
    for the command is more or less empty.

    The command invoked is specified in the cmd option

    Options:
        cmd=command

    netrc:
        Nothing
    """

    _name = 'ipv4-from-command'
    _oneliner = 'Obtain address from a command'

    def get_ip(self, log, options):
        """Implement IpPlugin.get_ip()."""
        opts = dict_of_opts(options)
        if 'cmd' not in opts:
            raise IpLookupError("Required option cmd= missing, giving up.")
        cmd = opts['cmd']
        log.debug("Running: %s", cmd)
        result = subprocess.getoutput(cmd).strip()
        log.debug("result: %s", result)
        pat = re.compile(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
        if not pat.fullmatch(result):
            raise IpLookupError("Bad result from ip cmmand: " + result)
        return result
