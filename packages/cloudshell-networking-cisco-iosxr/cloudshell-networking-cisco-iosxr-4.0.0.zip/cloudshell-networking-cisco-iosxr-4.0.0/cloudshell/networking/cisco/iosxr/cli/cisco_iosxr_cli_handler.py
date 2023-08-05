#!/usr/bin/python
# -*- coding: utf-8 -*-
from cloudshell.cli.cli_service_impl import CliServiceImpl

from cloudshell.networking.cisco.cli.cisco_cli_handler import CiscoCliHandler
from cloudshell.networking.cisco.cli.cisco_command_modes import EnableCommandMode, ConfigCommandMode
from cloudshell.networking.cisco.iosxr.cli.cisco_iosxr_command_modes import CiscoIOSXRConfigCommandMode


class CiscoIOSXRCliHandler(CiscoCliHandler):
    @property
    def config_mode(self):
        return self.modes[CiscoIOSXRConfigCommandMode]

    def on_session_start(self, session, logger):
        """Send default commands to configure/clear session outputs
        :return:
        """

        cli_service = CliServiceImpl(session=session, command_mode=self.enable_mode, logger=logger)
        cli_service.send_command("terminal length 0", EnableCommandMode.PROMPT)
        cli_service.send_command("terminal width 300", EnableCommandMode.PROMPT)
        with cli_service.enter_mode(self.config_mode) as config_session:
            config_session.send_command("no logging console", ConfigCommandMode.PROMPT)