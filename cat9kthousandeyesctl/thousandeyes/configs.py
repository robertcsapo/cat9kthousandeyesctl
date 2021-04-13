"""
Configuration
"""
from dataclasses import dataclass, fields
import yaml


@dataclass(frozen=True)
class Config:
    """ Config for Thousand Eyes Agent """

    hosts: list
    username: str
    password: str
    port: int
    timeout: int
    download_url: str
    appid: str
    vlan: int
    token: str


class Supported:
    """ Supported Catalyst 9000 devices """

    hardware = ["C9300", "C9400"]
    subscriptions = ["dna-advantage"]
    versions = [
        "17.03.03",
        "17.04.",
        "17.05.",
    ]


class Configs:
    """
    Parameters
    ----------
    config : file
        YAML config
    Returns
    -------
    dataclass: Config
        Config for Thousand Eyes Agent
    """

    @classmethod
    def load(cls, config):
        """
        Load config from YAML
        ---
        Returns
        dataclass: Config
        """
        try:
            with open(config, "r") as file:
                cfg_dict = yaml.load(file, Loader=yaml.FullLoader)
        except Exception as error_msg:
            raise Exception(f"Can't read config file - {error_msg}")
        return cls.__validate(cfg_dict)

    @classmethod
    def interactive(cls, config):
        """
        Load config from prompt (input)
        ---
        Returns
        dataclass: Config
        """
        return cls.__validate(config)

    @classmethod
    def __validate(cls, cfg_dict):
        """
        Create instance from dataclass
        ---
        Returns
        dataclass: Config
        """

        cfg = Config(
            hosts=cfg_dict["hosts"],
            username=cfg_dict["username"],
            password=cfg_dict["password"],
            port=cfg_dict["port"],
            timeout=cfg_dict["timeout"],
            download_url=cfg_dict["download_url"],
            appid=cfg_dict["appid"],
            vlan=cfg_dict["vlan"],
            token=cfg_dict["token"],
        )

        return cfg
