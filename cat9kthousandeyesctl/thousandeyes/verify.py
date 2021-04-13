"""
Validate data from Catalyst 9000
"""
from .configs import Supported


class Verify:
    """
    Parameters
    ----------
    data : dict (xml)
        XML data
    Returns
    -------
    bool
        If successful or failed
    """

    @staticmethod
    def hardware(data):
        """ Check hardware on device """
        try:
            data["data"]["device-hardware-data"]["device-hardware"]["device-inventory"]
        except Exception:
            raise Exception(
                "Can't determinate the Catalyst 9000 Hardware of the device"
            )

        for pid in data["data"]["device-hardware-data"]["device-hardware"][
            "device-inventory"
        ]:
            for h in Supported.hardware:
                if h in str(pid["part-number"]):
                    return True
        return False

    @staticmethod
    def subscription(data):
        """ Check DNA Subscription on device """
        try:
            data["data"]["licensing"]["state"]["state-info"]["usage"]
        except Exception:
            raise Exception("Can't determinate the DNA Subscription of the device")

        for sub in data["data"]["licensing"]["state"]["state-info"]["usage"]:
            for s in Supported.subscriptions:
                if s in str(sub["license-name"]):
                    return True
        return False

    @staticmethod
    def version(data):
        """ Check version on devicee """
        try:
            __version = data["data"]["install-oper-data"][
                "install-location-information"
            ]["install-version-state-info"]["version"]
        except Exception:
            raise Exception("Can't determinate the IOS-XE version of the device")

        for v in Supported.versions:
            if v in __version:
                return True
        return False

    @staticmethod
    def app_status_deploy(data, appid):
        """ Check deploy status """
        catch_succcess = [
            "Installing package",
            "RUNNING",
            "ACTIVATED",
        ]
        if "#text" in data["rpc-reply"]["result"]:
            if appid in data["rpc-reply"]["result"]["#text"]:
                for status in catch_succcess:
                    if status.lower() in data["rpc-reply"]["result"]["#text"].lower():
                        return True
        return False

    @staticmethod
    def app_status_undeploy(data, appid):
        """ Check undeploy status """
        catch_succcess = [
            "STOPPED",
            "DEPLOYED",
            "Uninstalling",
        ]
        if "#text" in data["rpc-reply"]["result"]:
            if appid in data["rpc-reply"]["result"]["#text"]:
                for status in catch_succcess:
                    if status.lower() in data["rpc-reply"]["result"]["#text"].lower():
                        return True
        return False

    @staticmethod
    def apps(data):
        """ Check existing apps hosted on device """
        if "app-hosting-oper-data" in data["data"]:
            # Applications already installed on Host
            return False
        return True

    @staticmethod
    def iox(data):
        """ Check IOX sevice on device """
        if "native" in data["data"]:
            for k in data["data"]["native"].keys():
                # IOX already configured on Host
                if k == "iox":
                    return True
        return False
