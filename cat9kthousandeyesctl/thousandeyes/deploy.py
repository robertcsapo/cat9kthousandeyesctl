"""
Orchestration of Deploy
"""
import time
import xmltodict
from .verify import Verify


class Deploy:
    """
    Parameters
    ----------
    obj : object
        Thousandeyes Class Instance
    Returns
    -------
    bool
        If successful or failed
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
        return Verify.hardware(data=data)

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
        return Verify.subscription(data=data)

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
        return Verify.version(data=data)

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
        if Verify.iox(data=data) is False:
            config = """
            <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                <iox>
                </iox>
                </native>
            </config>
            """
            if obj.device_api.config(config=config) is True:
                # Wait until IOX is ready
                time.sleep(300)
                return True
            else:
                return False
        else:
            return True

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
        return Verify.apps(data=data)

    @staticmethod
    def install(obj):
        """ Install Thousand Eyes Agent on device """
        rpc = f"""
        <app-hosting xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-rpc">
            <install>
                <appid>{obj.cfg.appid}</appid>
                <package>{obj.cfg.download_url}</package>
            </install>
        </app-hosting>
        """
        data = xmltodict.parse(obj.device_api.rpc(rpc=rpc))
        if Verify.app_status_deploy(data=data, appid=obj.cfg.appid) is True:
            max_retry = 10
            retry = 0
            while True:
                if Deploy.apps(obj) is False or retry == max_retry:
                    return True
                retry += 1
                time.sleep(15)
            return False
        else:
            return False

    @staticmethod
    def config(obj):
        """ Configure Thousand Eyes Agent on device """
        config = f"""
        <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <app-hosting-cfg-data xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-app-hosting-cfg">
            <apps operation="replace">
                <app>
                    <application-name>{obj.cfg.appid}</application-name>
                    <application-network-resource>
                        <appintf-vlan-mode>appintf-trunk</appintf-vlan-mode>
                    </application-network-resource>
                    <appintf-vlan-rules>
                        <appintf-vlan-rule>
                            <vlan-id>{obj.vlan}</vlan-id>
                            <guest-interface>0</guest-interface>
                        </appintf-vlan-rule>
                    </appintf-vlan-rules>
                    <docker-resource>true</docker-resource>
                    <run-optss>
                        <run-opts>
                            <line-index>1</line-index>
                            <line-run-opts>-e TEAGENT_ACCOUNT_TOKEN={obj.cfg.token}</line-run-opts>
                        </run-opts>
                    </run-optss>
                    <prepend-pkg-opts>true</prepend-pkg-opts>
                </app>
            </apps>
        </app-hosting-cfg-data>
        <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
            <interface>
            <AppGigabitEthernet operation="replace">
                <name>1/0/1</name>
                <description>{obj.cfg.appid}</description>
                <switchport>
                <mode xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-switch">
                <trunk xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-switch">
                </trunk>
                </mode>
                <trunk xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-switch">
                <allowed>
                    <vlan>
                        <vlans>{obj.vlan}</vlans>
                    </vlan>
                </allowed>
                </trunk>
                </switchport>
                <macro xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-switch">
                <auto>
                <processing>false</processing>
                </auto>
                </macro>
            </AppGigabitEthernet>
            </interface>
        </native>
        </config>
        """
        return obj.device_api.config(config=config)

    @staticmethod
    def activate(obj):
        """ Activate Thousand Eyes Agent on device """
        rpc = f"""
        <app-hosting xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-rpc">
            <activate>
                <appid>{obj.cfg.appid}</appid>
            </activate>
        </app-hosting>
        """
        data = xmltodict.parse(obj.device_api.rpc(rpc=rpc))
        return Verify.app_status_deploy(data=data, appid=obj.cfg.appid)

    @staticmethod
    def start(obj):
        """ Start Thousand Eyes Agent on device """
        rpc = f"""
        <app-hosting xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-rpc">
            <start>
                <appid>{obj.cfg.appid}</appid>
            </start>
        </app-hosting>
        """
        data = xmltodict.parse(obj.device_api.rpc(rpc=rpc))
        return Verify.app_status_deploy(data=data, appid=obj.cfg.appid)
