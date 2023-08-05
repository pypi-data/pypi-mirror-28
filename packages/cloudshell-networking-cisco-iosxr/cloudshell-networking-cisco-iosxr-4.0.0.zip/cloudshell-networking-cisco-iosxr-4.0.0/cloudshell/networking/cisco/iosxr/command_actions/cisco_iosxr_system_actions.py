import re
from cloudshell.cli.command_template.command_template_executor import CommandTemplateExecutor
from cloudshell.networking.cisco.command_actions.system_actions import SystemActions
from cloudshell.networking.cisco.iosxr.command_templates.cisco_ios_xr_cmd_templates import COMMIT_REPlACE, LOAD, COMMIT


class CiscoIOSXRSystemActions(SystemActions):
    def __init__(self, cli_service, logger):
        super(CiscoIOSXRSystemActions, self).__init__(cli_service, logger)

    def load(self, source_file, vrf=None, action_map=None, error_map=None):
        load_cmd = CommandTemplateExecutor(self._cli_service, LOAD, action_map=action_map, error_map=error_map)
        if vrf:
            load_result = load_cmd.execute_command(source_file=source_file, vrf=vrf)
        else:
            load_result = load_cmd.execute_command(source_file=source_file)

        match_success = re.search(r"[\[\(][1-9][0-9]*[\)\]].*bytes", load_result, re.IGNORECASE | re.MULTILINE)
        if not match_success:
            error_str = "Failed to restore configuration, please check logs"
            match_error = re.search(r" Can't assign requested address|[Ee]rror:.*\n|%.*$",
                                    load_result, re.IGNORECASE | re.MULTILINE)

            if match_error:
                error_str = 'load error: ' + match_error.group()

            raise Exception('validate_load_success', error_str)

        return load_result

    def replace_config(self, action_map=None, error_map=None):
        commit_result = CommandTemplateExecutor(self._cli_service, COMMIT_REPlACE).execute_command(
            action_map=action_map, error_map=error_map)

        error_match_commit = re.search(r'(ERROR|[Ee]rror).*\n', commit_result)

        if error_match_commit:
            error_str = error_match_commit.group()
            raise Exception('validate_replace_config_success', 'load error: ' + error_str)
        return commit_result

    def commit(self, action_map=None, error_map=None):
        CommandTemplateExecutor(self._cli_service, COMMIT).execute_command(action_map=action_map, error_map=error_map)

