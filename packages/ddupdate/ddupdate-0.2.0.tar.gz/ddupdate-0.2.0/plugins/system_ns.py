"""
ddupdate plugin updating data on system-ns.com.

See: ddupdate(8)
See: https://system-ns.com/services/dynamic

"""
import json

from ddupdate.ddplugin import UpdatePlugin, UpdateError
from ddupdate.ddplugin import get_response, get_netrc_auth


class SystemNsPlugin(UpdatePlugin):
    """
    Update a dns entry on system-ns.com.

    As usual, any host updated must first be defined in the web UI.
    Providing an ip address is optional but supported; the ip-disabled
    plugin can be used.

    Access to the service requires an API token. This is available in the
    website account.

    netrc: Use a line like
        machine  system-ns.com password <API token from website>

    Options:
        None
    """

    _name = 'system-ns.com'
    _oneliner = 'Updates on https://system-ns.com'
    _apihost = 'https://system-ns.com/api'
    _url = '{0}?type=dynamic&domain={1}&command=set&token={2}'

    def register(self, log, hostname, ip, options):
        """Implement UpdatePlugin.register()."""
        password = get_netrc_auth('system-ns.com')[1]
        url = self._url.format(self._apihost, hostname, password)
        if ip:
            url += "&ip=" + ip.v4
        html = get_response(log, url, self._socket_to)
        reply = json.loads(html)
        if reply['code'] > 2:
            raise UpdateError('Bad reply code {0}, message: {1}'.format(
                reply['code'], reply['msg']))
        log.info("Server reply: " + reply['msg'])
