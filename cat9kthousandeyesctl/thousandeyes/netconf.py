"""
Device API using Netconf
"""
from ncclient import manager
from lxml import etree


class Netconf:
    """
    Methods
    ----------
    _connect : obj
        Establish Netconf over SSH
    get: xml
        Get config
    config: xml
        Edit config
    rpc: xml
        RPC commands
    """

    def __init__(self, host=None, port=830, timeout=600, username=None, password=None):
        """
        Parameters
        ----------
        host : str
            Device host
        port: int
            Device port
        timeout: int
            Netconf port
        username: str
            Device access
        password: str
            Device access
        """
        self.host = host
        self.port = port
        self.timeout = timeout
        self.username = username
        self.password = password

    def _connect(self):
        """
        Parameters
        ----------
        host : str
            Device host
        port: int
            Device port
        timeout: int
            Netconf port
        username: str
            Device access
        password: str
            Device access

        Returns
        -------
        obj
            Netconf connection object
        """
        return manager.connect(
            host=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
            hostkey_verify=False,
            timeout=self.timeout,
        )

    def get(self, filter=None):
        """
        Parameters
        ----------
        filter : str
            Netconf XML XPath
        Returns
        -------
        c: str
            XML
        """
        with self._connect() as m:
            c = m.get(filter).data
        return etree.tostring(c, encoding="unicode", pretty_print=True)

    def config(self, config):
        """
        Parameters
        ----------
        config : str
            Netconf XML
        Returns
        -------
        c: bool
            Successful or failed
        """
        with self._connect() as m:
            c = m.edit_config(target="running", config=config)
            if c.ok:
                return True
            else:
                print(c.error)
                return False

    def rpc(self, rpc):
        """
        Parameters
        ----------
        rpc : str
            Netconf XML RPC
        Returns
        -------
        c: str
            XML
        """
        with self._connect() as m:
            c = m.dispatch(etree.fromstring(rpc))
            return str(c)
