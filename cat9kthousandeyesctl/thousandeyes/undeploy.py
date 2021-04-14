"""
Orchestration of Undeploy
"""
import xmltodict
from .verify import Verify


class Undeploy:
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
    def stop(obj):
        """ Stop Thousand Eyes Agent on device """
        rpc = f"""
        <app-hosting xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-rpc">
            <stop>
                <appid>{obj.cfg.appid}</appid>
            </stop>
        </app-hosting>
        """
        data = xmltodict.parse(obj.device_api.rpc(rpc=rpc))
        return Verify.app_status_undeploy(data=data, appid=obj.cfg.appid)

    @staticmethod
    def deactivate(obj):
        """ Deactivate Thousand Eyes Agent on device """
        rpc = f"""
        <app-hosting xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-rpc">
            <deactivate>
                <appid>{obj.cfg.appid}</appid>
            </deactivate>
        </app-hosting>
        """
        data = xmltodict.parse(obj.device_api.rpc(rpc=rpc))
        return Verify.app_status_undeploy(data=data, appid=obj.cfg.appid)

    @staticmethod
    def uninstall(obj):
        """ Uninstall Thousand Eyes Agent on device """
        rpc = f"""
        <app-hosting xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-rpc">
            <uninstall>
                <appid>{obj.cfg.appid}</appid>
            </uninstall>
        </app-hosting>
        """
        data = xmltodict.parse(obj.device_api.rpc(rpc=rpc))
        return Verify.app_status_undeploy(data=data, appid=obj.cfg.appid)

    @staticmethod
    def config(obj):
        """ Removing Application Hosting config on device """
        config = f"""
        <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <app-hosting-cfg-data xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-app-hosting-cfg">
            <apps operation="delete">
                <app>
                    <application-name>{obj.cfg.appid}</application-name>
                    <application-network-resource>
                        <appintf-vlan-mode>appintf-trunk</appintf-vlan-mode>
                    </application-network-resource>
                    <appintf-vlan-rules>
                        <appintf-vlan-rule>
                            <vlan-id>{obj.cfg.vlan}</vlan-id>
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
            <AppGigabitEthernet>
                <name>1/0/1</name>
            </AppGigabitEthernet>
            </interface>
        </native>
        </config>
        """
        return obj.device_api.config(config=config)

    @staticmethod
    def iox(obj):
        """ Disable IOX Service on device """
        config = """
            <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                <iox operation="delete">
                </iox>
                </native>
            </config>
            """
        return obj.device_api.config(config=config)
