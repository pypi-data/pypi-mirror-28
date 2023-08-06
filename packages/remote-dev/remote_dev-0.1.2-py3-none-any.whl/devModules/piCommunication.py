"""
Class for the basic communication with the pi
used to:
1) manage files on the pi
2) run scripts on the pi
3) Create commands to be ran on the pi
"""
import subprocess


class PiCommunication:
    def __init__(self, username, pi_address):
        self.username = username
        self.pi_address = pi_address

    def run_command(self, project_folder, script):
        """
        Runs a command on the pi in the given folder
        :param project_folder: the folder to run the script in
        :param script: the s
        :return:
        """
        command = ["ssh", "{}@{}".format(self.username, self.pi_address), "cd {}".format(project_folder), "&&", script]
        subprocess.call(command)

    def scp_dir(self, dir, destination):
        """
        Secure copies a dir to the given destination
        :param dir: the directory to copy
        :param destination: the destination directory on the pi
        :return:
        """
        command = self.get_scp_dir_command(dir, destination)
        subprocess.call(command)

    def get_scp_dir_command(self, dir, destination):
        """
        Gets a command to copy the given dirs and files
        :param username:
        :param pi_address:
        :return:
        """
        dest = "{}@{}:{}".format(self.username, self.pi_address, destination)
        return ["scp", "-r", dir, dest]

    def get_login(self):
        return "{}@{}".format(self.username, self.pi_address)

    def delete_file_on_pi(self, file):
        """
        Deletes a file on the pi
        :param file:
        :return:
        """
        command = ["ssh", self.get_login(), "rm {}".format(file)]
        subprocess.call(command)

    def delete_dir_on_pi(self, dir):
        """
        Deletes a directory and all its content on the pi
        :param dir:
        :return:
        """
        command = ["ssh", self.get_login(), "rm -r -f {}".format(dir)]
        subprocess.call(command)

    def run_multiple_commands(self, commands):
        command = ["ssh", "-t", self.get_login(), commands.pop(0)]

        for c in commands:
            command += ["&&", c]
        subprocess.call(command)

    def get_cd_command(self, dir):
        """
        Gets the command to cd into the given dir
        :param dir:
        :return:
        """
        return "cd {}".format(dir)
