"""
Orchestration of Thousand Eyes agents on Catalyst 9000
"""
from rich.table import Table
from .progressbar import Progressbar
from .netconf import Netconf
from .configs import Configs
from .deploy import Deploy
from .status import Status
from .undeploy import Undeploy


class Thousandeyes:
    """ Class for Deploy and Undeploy """

    class Configs(Configs):
        """ Load config """

        pass

    def __init__(self, cfg):
        """ Stages with description of tasks """
        self.stages = {
            "deploy": [
                "check hardware",
                "check subscription",
                "check ios-xe version",
                "check iox",
                "check existing apps",
                f"install {cfg.appid}",
                f"config {cfg.appid}",
                f"activate {cfg.appid}",
                f"start {cfg.appid}",
            ],
            "status": [
                "check hardware",
                "check subscription",
                "check ios-xe version",
                "check iox",
                "check existing apps",
            ],
            "undeploy": [
                f"stop {cfg.appid}",
                f"deactivate {cfg.appid}",
                f"uninstall {cfg.appid}",
                f"remove config {cfg.appid}",
                "disable iox",
            ],
        }
        self.cfg = cfg

    def deploy(self, host, vlan):
        """
        Parameters
        ----------
        host : str
            Catalyst 9000 host
        vlan: int
            Thousand Eyes Agent VLAN
        Returns
        -------
        bool
            If successful or failed
        """

        self.device_api = Netconf(
            host=host,
            username=self.cfg.username,
            password=self.cfg.password,
            port=self.cfg.port,
            timeout=self.cfg.timeout,
        )
        self.host = host
        self.vlan = vlan
        self.mode = "deploy"

        pbar = Progressbar(host=host)
        with pbar.progress:
            for stage in pbar.progress.track(self.stages[self.mode]):
                pbar.update(stage=stage)

                if "hardware" in stage:
                    # Stage 0
                    if Deploy.hardware(self) is not True:
                        pbar.update(
                            error=True, msg="Non-supported Cisco Catalyst Hardware"
                        )
                        return False

                if "subscription" in stage:
                    # Stage 1
                    if Deploy.subscription(self) is not True:
                        pbar.update(
                            error=True, msg="Non-supported Cisco DNA Subscription"
                        )
                        return False

                if "ios-xe" in stage:
                    # Stage 2
                    if Deploy.version(self) is not True:
                        pbar.update(error=True, msg="Non-supported IOS-XE version")
                        return False

                if "iox" in stage:
                    # Stage 3
                    if Deploy.iox(self) is not True:
                        pbar.update(
                            error=True, msg="Couldn't enable IOX (container support)"
                        )
                        return False

                if "apps" in stage:
                    # Stage 4
                    if Deploy.apps(self) is not True:
                        pbar.update(
                            error=True,
                            msg="There's an app already configured",
                        )
                        return False

                if "install" in stage:
                    # Stage 5
                    if Deploy.install(self) is not True:
                        pbar.update(
                            error=True, msg=f"Couldn't install {self.cfg.appid}"
                        )
                        return False

                if "config" in stage:
                    # Stage 6
                    if Deploy.config(self) is not True:
                        pbar.update(
                            error=True,
                            msg="Couldn't configure Application Hosting on IOS-XE",
                        )
                        return False

                if "activate" in stage:
                    # Stage 7
                    if Deploy.activate(self) is not True:
                        pbar.update(
                            error=True, msg=f"Couldn't activate {self.cfg.appid}"
                        )
                        return False

                if "start" in stage:
                    # Stage 8
                    if Deploy.start(self) is not True:
                        pbar.update(error=True, msg=f"Couldn't start {self.cfg.appid}")
                        return False

                # Stage 9
                pbar.update(success=True, msg="Thousand Eyes Agent Deployed")

        return True

    def status(self, host):
        """
        Parameters
        ----------
        host : str
            Catalyst 9000 host
        Returns
        -------
        dict
            Data about the host
        """

        self.device_api = Netconf(
            host=host,
            username=self.cfg.username,
            password=self.cfg.password,
            port=self.cfg.port,
            timeout=self.cfg.timeout,
        )
        self.host = host
        self.mode = "status"
        data = {}

        pbar = Progressbar(host=host)
        with pbar.progress:
            for stage in pbar.progress.track(self.stages[self.mode]):
                pbar.update(stage=stage)

                if "hardware" in stage:
                    data["hardware"] = Status.hardware(self)
                    if data["hardware"] is None:
                        data["hardware"] = "Non-supported"

                if "subscription" in stage:
                    data["subscription"] = Status.subscription(self)
                    if data["subscription"] is None:
                        data["subscription"] = "Unknown"

                if "ios-xe" in stage:
                    data["version"] = Status.version(self)
                    if data["version"] is None:
                        data["version"] = "Non-supported"

                if "iox" in stage:
                    data["iox"] = Status.iox(self)

                if "apps" in stage:
                    data["apps"] = Status.apps(self)

                pbar.update(success=True, msg="Status Completed")

        return data

    def undeploy(self, host, disable_iox):
        """
        Parameters
        ----------
        host : str
            Catalyst 9000 host
        Returns
        -------
        bool
            If successful or failed
        """

        self.device_api = Netconf(
            host=host,
            username=self.cfg.username,
            password=self.cfg.password,
            port=self.cfg.port,
            timeout=self.cfg.timeout,
        )
        self.host = host
        self.mode = "undeploy"

        pbar = Progressbar(host=host)
        with pbar.progress:
            for stage in pbar.progress.track(self.stages[self.mode]):
                pbar.update(stage=stage)

                if "stop" in stage:
                    # Stage 0
                    if Undeploy.stop(self) is not True:
                        pbar.update(error=True, msg=f"Couldn't stop {self.cfg.appid}")
                        return False
                if "deactivate" in stage:
                    # Stage 1
                    if Undeploy.deactivate(self) is not True:
                        pbar.update(
                            error=True, msg=f"Couldn't deactivate {self.cfg.appid}"
                        )
                        return False

                if "uninstall" in stage:
                    # Stage 2
                    if Undeploy.uninstall(self) is not True:
                        pbar.update(
                            error=True, msg=f"Couldn't uninstall {self.cfg.appid}"
                        )
                        return False

                if "config" in stage:
                    # Stage 3
                    if Undeploy.config(self) is not True:
                        pbar.update(
                            error=True,
                            msg="Couldn't remove configure for Application Hosting on IOS-XE",
                        )
                        return False

                if "disable" in stage:
                    # Stage 4
                    if disable_iox is True:
                        if Undeploy.iox(self) is not True:
                            pbar.update(
                                error=True,
                                msg="Couldn't disable IOX (container support)",
                            )
                            return False

                # Stage 5
                pbar.update(success=True, msg="Thousand Eyes Agent Undeployed")

        return True

    def table(self, data):
        """ Display Table for Status results """
        table = Table(title="\nStatus Thousand Eyes Agents")
        table.add_column("Host")

        for host in data.keys():
            for k in data[host].keys():
                table.add_column(k.capitalize())
            break

        for host in data:
            v = [str(v) for v in data[host].values()]
            table.add_row(host, v[0], v[1], v[2], v[3], v[4])

        return table
