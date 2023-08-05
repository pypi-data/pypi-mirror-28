import os
import enum
import sys
from qtconsole.qt import QtGui
from chconsole.launch.launch_config import LaunchConfig
from chconsole.launch.launch_widget import LaunchWidget
from chconsole.storage import DefaultNames
from jupyter_core.paths import jupyter_config_dir
from chconsole import __version__
from traitlets.config.application import catch_config_error
from traitlets import Dict, CBool, UseEnum, Unicode
from jupyter_core.application import JupyterApp, base_flags, base_aliases
from traitlets.config.application import boolean_flag
from chconsole.launch import (
    Launch, start_chconsole, start_console, start_qtconsole)

__author__ = 'Manfred Minimair <manfred@minimair.org>'


_examples = """
jupyter chjoin                      # start a chconsole connected to a remote session
"""

flags = dict(base_flags)
# Flags from boolean_flog allow uses such
# as --force-username, --no-force-username
flags.update(boolean_flag(
    'gui', 'JoinApp.gui',
    "Use gui to connect to launch console."
))
flags.update(boolean_flag(
    'force-username', 'JoinApp.require_username',
    "Require entering a user name in the gui."
    "Use the pre-determined user name if none given."
))

aliases = dict(base_aliases)
new_aliases = dict(
    key='JoinApp.key',
    curie='JoinApp.curie',
    console='JoinApp.console_type'
)
aliases.update(new_aliases)


class ConsoleType(enum.Enum):
    chat = 1
    qt = 2
    text = 3


class JoinApp(JupyterApp):

    name = 'jupyter-chjoin'
    version = __version__
    description = """
        Launch Chat Console connected to a remote kernel.

        This launches a chconsole instance locally connected
        to a Python kernel running remotely.

    """
    examples = _examples

    classes = [LaunchConfig]  # additional classes with configurable options
    flags = Dict(flags)
    aliases = Dict(aliases)

    gui = CBool(True, config=True,
                help="Whether to launch through gui; only launches chat console through gui")

    require_username = CBool(True, config=True,
                             help="Whether to require input of username in gui")

    console_type = UseEnum(ConsoleType, default_value=ConsoleType.chat,
                           config=True,
                           help='type of console to use: 1 = chat, 2 = qt, 3 = text')

    key = Unicode('', config=True, help='Session identifier to connect to.')
    curie = Unicode('', config=True,
                    help='Curie consisting of ip address and Session identifier to connect to.')

    launch_config = None  # LaunchConfig

    @catch_config_error
    def initialize(self, argv=None):
        super(JoinApp, self).initialize(argv)
        if self._dispatching:
            return
        # more initialization code if needed
        self.launch_config = LaunchConfig()

    def start(self):
        super(JoinApp, self).start()
        if self.gui:
            app = QtGui.QApplication(sys.argv)
            self.widget = LaunchWidget(self.launch_config.kernel_gate,
                                       self.launch_config.gate_tunnel_user,
                                       self.require_username)
            self.widget.show()
            sys.exit(app.exec_())
        else:
            if self.curie:
                curie = self.curie
            elif self.key:
                curie = self.launch_config.kernel_gate + '/' + self.key
            else:  # no key to connect
                print('Provide --key or --curie parameter.')
                return
            launch = Launch(self.launch_config.gate_tunnel_user,
                            curie)
            if self.console_type == ConsoleType.chat:
                start_chconsole(launch)

            elif self.console_type == ConsoleType.qt:
                start_qtconsole(launch)

            else:  # self.console_type == ConsoleType.text:
                start_console(launch)


def _gen_default_config():
    """
    Generate the config file if it does not exist.
    :return: True if config file generated.
    """
    gen_config = False
    config_location = os.path.join(jupyter_config_dir(),
                                   DefaultNames.chjoin_config_file)
    if not os.path.exists(config_location):
        gen_config = True
        JoinApp.config_file = config_location
        JoinApp.generate_config = gen_config
        JoinApp.launch_instance()

    return gen_config


def main():
    if _gen_default_config():
        print('Ready to run application.')
    else:
        JoinApp.launch_instance()


if __name__ == '__main__':
    main()
