"""
Orchestration of Status
"""
import time
import xmltodict
from .verify import Verify
from .configs import Supported


class Status:
    """
    Parameters
    ----------
    obj : object
        Thousandeyes Class Instance
    Returns
    -------
    dict
        With data and status
    """

    @staticmethod
    def hardware(obj):
        """ Check hardware on device """
        __filter = """
        <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
            <device-hardware-data xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-device-hardware-oper">
            <device-hardware>
                <device-inventory>
                <part-number>
                </part-number>
                </device-inventory>
            </device-hardware>
            </device-hardware-data>
        </filter>
        """
        data = xmltodict.parse(obj.device_api.get(filter=__filter))
        for pid in data["data"]["device-hardware-data"]["device-hardware"][
            "device-inventory"
        ]:
            for h in Supported.hardware:
                if h in str(pid["part-number"]):
                    return pid["part-number"]
        return None

    @staticmethod
    def subscription(obj):
        """ Check version on devicee """
        __filter = """
        <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
            <licensing xmlns="http://cisco.com/ns/yang/cisco-smart-license">
            <state>
            <state-info>
            <udi>
                <pid>
                </pid>
            </udi>
            <usage>
                <license-name>
                </license-name>
            </usage>
            </state-info>
            </state>
            </licensing>
        </filter>
        """
        data = xmltodict.parse(obj.device_api.get(filter=__filter))
        for sub in data["data"]["licensing"]["state"]["state-info"]["usage"]:
            for s in Supported.subscriptions:
                if s in str(sub["license-name"]):
                    return str(sub["license-name"])
        return None

    @staticmethod
    def version(obj):
        """ Check version on devicee """
        __filter = """
        <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
            <install-oper-data xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-install-oper">
            <install-location-information>
            <install-version-state-info>
            <version>
            </version>
            </install-version-state-info>
            </install-location-information>
            </install-oper-data>
        </filter>
        """
        data = xmltodict.parse(obj.device_api.get(filter=__filter))
        try:
            return data["data"]["install-oper-data"]["install-location-information"][
                "install-version-state-info"
            ]["version"][:8]
        except Exception:
            return None

    @staticmethod
    def iox(obj):
        """ Check IOX sevice on device """
        __filter = """
        <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
            <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
            <iox>
            </iox>
            </native>
        </filter>
        """
        data = xmltodict.parse(obj.device_api.get(filter=__filter))
        return Verify.iox(data=data)

    @staticmethod
    def apps(obj):
        """ Check existing apps hosted on device """
        __filter = """
        <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
            <app-hosting-oper-data xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-app-hosting-oper">
            <app>
            </app>
            </app-hosting-oper-data>
        </filter>
        """
        data = xmltodict.parse(obj.device_api.get(filter=__filter))
        if "app-hosting-oper-data" in data["data"]:
            return data["data"]["app-hosting-oper-data"]["app"]["name"]
        return False
