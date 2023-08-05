"""
ddupdate plugin updating data on freedns.io.

See: ddupdate(8)
See: https://freedns.io/api

FIXME: Add ipv6 support
"""

from ddupdate.ddplugin import UpdatePlugin, get_netrc_auth, get_response


class FreednsIoPlugin(UpdatePlugin):
    """
    Updates DNS data for host on freedns.io.

    As usual, any host updated must first be defined in the web UI.
    Providing an ip address is optional but supported; the
    ip-disabled plugin can be used.

    The service offers more functionality not exposed here: ipv6
    addresses, TXT and MX records, etc. See https://freedns.io/api
    It should be straight-forward to add options supporting this.

    netrc: Use a line like
        machine freedns.io login <username> password <password>

    Options:
        None
    """

    _name = 'freedns.io'
    _oneliner = 'Updates on https://freedns.io'
    _url = 'https://freedns.io/request'

    def register(self, log, hostname, ip, options):
        """Implement UpdatePlugin.register."""
        user, password = get_netrc_auth('freedns.io')
        data = {
            'username': user,
            'password': password,
            'host': hostname.split('.freedns.io')[0],
            'record': 'A'
        }
        if ip:
            data['value'] = ip.v4
        html = get_response(log, self._url, self._socket_to, data=data)
        log.info("Server reply: " + html)
