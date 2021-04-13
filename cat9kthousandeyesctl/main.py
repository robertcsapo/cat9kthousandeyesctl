#!/usr/bin/env python
"""cat9kthousandeyesctl Console Script.

Copyright (c) 2021 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.

"""
import logging
import sys
import click
from rich.console import Console
from .thousandeyes import Thousandeyes
from . import Metadata


@click.group()
@click.version_option(Metadata.version)
@click.option("--debug", is_flag=True, help="Enable logging")
@click.pass_context
def cli(ctx, debug):
    """
    Manage Thousand Eyes Agent on Catalyst 9000
    """
    ctx.ensure_object(dict)
    ctx.obj["debug"] = debug
    pass


@cli.command()
@click.pass_context
def interactive(ctx):
    """
    Interactive TTY mode
    """
    if ctx.obj["debug"] is True:
        enable_debug()
    print("Interactive mode")
    config = {}
    __hosts = click.prompt("Hosts", type=str).replace(" ", "")
    config["hosts"] = __hosts.split(",")
    config["username"] = click.prompt("Username", type=str)
    config["password"] = click.prompt("Password", type=str, hide_input=True)
    config["port"] = click.prompt("Port", default=830, type=int)
    config["timeout"] = click.prompt("Timeout", default=300, type=int)
    config["vlan"] = click.prompt("VLAN", type=int)
    config["token"] = click.prompt("Thousand Eyes Token", type=str)
    config["download_url"] = click.prompt(
        "Download URL",
        default="https://downloads.thousandeyes.com/enterprise-agent/thousandeyes-enterprise-agent-3.0.cat9k.tar",
    )
    config["appid"] = click.prompt("AppId", default="thousandeyes_enterprise_agent")
    cfg = Thousandeyes.Configs.interactive(config=config)
    mode = click.prompt("Deploy or Undeploy?", type=str, default="deploy")
    proccess = Thousandeyes(cfg)
    for host in cfg.hosts:
        if "undeploy" in mode.lower():
            disable_iox = click.confirm(
                "Disable IOX?", default=False, show_default=True
            )
            proccess.undeploy(host=host, disable_iox=disable_iox)
        if "deploy" in mode.lower():
            proccess.deploy(host=host, vlan=cfg.vlan)


@cli.command()
@click.option("--config", "-c", required=True, type=str, help="Config")
@click.pass_context
def deploy(ctx, config):
    """
    Deploy Thousand Eyes Agent
    """
    if ctx.obj["debug"] is True:
        enable_debug()
    print("Deploying Thousand Eyes Agents")
    cfg = Thousandeyes.Configs.load(config=config)
    proccess = Thousandeyes(cfg)

    for host, override in cfg.hosts.items():
        if isinstance(override, dict):
            if "vlan" in override:
                try:
                    proccess.deploy(host=host, vlan=override["vlan"])
                except Exception as error_msg:
                    print(f"Can't connect to {host} - {error_msg}")
                    pass
        else:
            try:
                proccess.deploy(host=host, vlan=cfg.vlan)
            except Exception as error_msg:
                print(f"Can't connect to {host} - {error_msg}")
                pass


@cli.command()
@click.option("--config", "-c", required=True, type=str, help="Config")
@click.pass_context
def status(ctx, config):
    """
    Status of Application Hosting on the devices
    """
    if ctx.obj["debug"] is True:
        enable_debug()
    print("Collecting status of Thousand Eyes Agents")
    cfg = Thousandeyes.Configs.load(config=config)
    proccess = Thousandeyes(cfg)
    data = {}

    for host in cfg.hosts:
        try:
            data[host] = proccess.status(host=host)
        except Exception as error_msg:
            print(f"Can't connect to {host} - {error_msg}")
            pass

    """ Print table with the results """
    console = Console()
    console.print(proccess.table(data))


@cli.command()
@click.option("--config", "-c", required=True, type=str, help="Config")
@click.option("--disable-iox", is_flag=True, help="Disable IOX")
@click.pass_context
def undeploy(ctx, config, disable_iox):
    """
    Remove Thousand Eyes Agent
    """
    if ctx.obj["debug"] is True:
        enable_debug()
    print("Undeploying Thousand Eyes Agents")
    cfg = Thousandeyes.Configs.load(config=config)
    proccess = Thousandeyes(cfg)
    for host in cfg.hosts:
        try:
            proccess.undeploy(host=host, disable_iox=disable_iox)
        except Exception as error_msg:
            print(f"Can't connect to {host} - {error_msg}")
            pass


def enable_debug():
    """
    Enable debugging of Netconf backend
    """
    print("Debug enabled")
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s: %(message)s",
        stream=sys.stdout,
    )


if __name__ == "__main__":
    cli()
