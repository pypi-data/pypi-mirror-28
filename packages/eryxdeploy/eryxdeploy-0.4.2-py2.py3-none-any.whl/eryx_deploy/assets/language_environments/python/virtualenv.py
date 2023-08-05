import os

from eryx_deploy.assets.abs_executable_environment import ExecutableEnvironment


class Virtualenv(ExecutableEnvironment):
    def __init__(self, host_machine, name, path=None):
        self._host_machine = host_machine
        self._name = name

        if path:
            self._path = path
        else:
            self._path = os.path.join(self._host_machine.project_path(), self._name)

    def first_time_setup(self):
        self._install_tool()
        self._create_env()

    def run(self, command, on_fail_msg=None):
        with self._host_machine.cd_project():
            with self._host_machine.prefix('source %s/bin/activate' % self._path):
                return self._host_machine.run(command, on_fail_msg=on_fail_msg)

    # private

    def _install_tool(self):
        self._host_machine.run('sudo -H pip install virtualenv')

    def _create_env(self):
        if not self._host_machine.path_exists(self._path):
            self._host_machine.run('virtualenv %s' % self._path)
