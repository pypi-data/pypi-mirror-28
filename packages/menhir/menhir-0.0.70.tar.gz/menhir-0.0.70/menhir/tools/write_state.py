"""Tool that writes the project state to a file."""

import argparse
import logging

from menhir.fileutils import yaml_dumper
from menhir.tool import Tool
from menhir.tool_utils import OK, NOTHING_TO_DO, working_dir

log = logging.getLogger(__name__)


def tool():
    return WriteState()


class WriteState(Tool):

    def dir_info(tool, path, info):
        return {
            'project_recognised': False,
            'can_run': True,
        }

    def dependencies(tool, path):
        return []

    def arg_parser(tool, **kwargs):
        """Arg parser for the tool options and arguments."""
        return parser(**kwargs)

    def execute_tool(tool, path, info, args):
        """Execute the write_state tool."""
        with working_dir(path):
            log.info('Writing state in %s', path)
            if 'changed' in info:
                with open('menhir-state.yaml', 'w+') as f:
                    yaml = yaml_dumper()
                    yaml.dump({'changed': info['changed']}, f)
                    return OK

        return NOTHING_TO_DO


def parser(**kwargs):
    """Arg parser for the tool options and arguments."""
    parser = argparse.ArgumentParser(
        description="Write state.",
        **kwargs
    )
    return parser
