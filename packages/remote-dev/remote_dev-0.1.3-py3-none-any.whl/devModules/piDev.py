import time

import yaml

from devModules.filesystem import *
from devModules.piCommunication import *

"""
Class for managing the development on the pi. Used to smart copy the project dirs and run
project scripts on the pi
"""


class PiDev:
    def __init__(self, settings):
        self.project_name = settings["project_name"]
        self.username = settings["username"]
        self.dirs = settings["dirs"]
        self.exclude = settings["exclude"]
        self.root_pi = settings["root_pi"]
        self.project_dir = settings["project_dir"]
        self.pi_address = settings["pi_address"]
        self.copy_dir = settings["copy_dir"]
        self.session_file = settings["session_file"]
        self.comm = PiCommunication(self.username, self.pi_address)
        self.python_version = settings["python_version"]
        self.dependencies = settings["dependencies"]
        self.provision_commands = settings["provision_commands"]

    def run_command(self, command):
        """
        Runs a command on the pi in the project root folder
        :param command: the command to run
        :return:
        """
        self.comm.run_multiple_commands(
            [self.comm.get_cd_command(self.root_pi),
             self.comm.get_cd_command(self.project_dir),
             command])

    def run_tests(self):
        """
        Runs the tests on the pi
        :return:
        """
        self.run_command("python -m unittest discover")

    def scp_project(self):
        """
        copies the project to the pi
        :return: None
        """
        self.comm.scp_dir(self.copy_dir, self.root_pi)

    def update_session(self):
        """
        Updates the information in the session:
            1) updates the last modified time stamp
            2) updates the files that were copied
        :return:
        """
        # Get current time stamp and store in the session
        now = time.time()
        session_data = {
            "time": now,
            "files": get_included_files(self.dirs, self.exclude)
        }
        with open(self.session_file, "w") as f:
            yaml.dump(session_data, f, default_flow_style=False)

    def load_session(self):
        """
        Loads the session information
        :return:
        """
        return yaml_file_to_dict(self.session_file)

    def upload_changes(self):
        """
        Uploads the changes to the pi
        :return:
        """
        remove_if_exists(self.copy_dir)
        session = self.load_session()
        timestamp = session["time"]

        copy_with_exclusion(self.dirs, self.copy_dir, self.exclude, timestamp)

        if os.path.exists(self.copy_dir):
            self.comm.scp_dir(self.copy_dir, self.root_pi)
        files = session["files"]
        included = get_included_files(self.dirs, self.exclude)
        to_delete = files - included
        for f in to_delete:
            self.comm.delete_file_on_pi(self.project_dir + f[1:])
        self.update_session()

    def create_project(self):
        copy_with_exclusion(self.dirs, self.copy_dir, self.exclude)

    def delete_project(self):
        """
        Deletes the project on the pi
        :return:
        """
        self.comm.delete_dir_on_pi(self.project_dir)

    def create_venv(self):
        """
        Creates the virtual environment
        :return:
        """
        self.comm.run_command(self.root_pi, "virtualenv {}_venv -p {}".format(self.project_name, self.python_version))

    def install_dependencies(self):
        """
        Installs the dependencies. (Must have created a virtual environment)
        :return:
        """
        # First check if the virtual env exist

        commands = [
                       self.comm.get_cd_command(self.root_pi),
                       self.get_activate_venv_command(),
                   ] + [
                       "pip install {}".format(dep) for dep in self.dependencies
                   ]
        self.comm.run_multiple_commands(commands)

    def get_activate_venv_command(self):
        """
        Gets the command to activate the venv
        :return:
        """
        return "source {}_venv/bin/activate".format(self.project_name)

    def run_provision_commands(self):
        """
        runs the extra commands in the settings
        :return: None
        """
        self.comm.run_multiple_commands(self.provision_commands)