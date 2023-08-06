from openpyn import root
import subprocess
import sys


def check_credentials():
    try:
        serverFiles = subprocess.check_output(
            "ls /usr/share/openpyn/credentials", shell=True, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        return False
    return True


def save_credentials():
    if root.verify_running_as_root() is False:
        print("Please run as 'sudo openpyn --init' the first time. root access is",
              "needed to store credentials in /usr/share/openpyn/credentials.")
        sys.exit()
    else:
        print("Storing credentials in '/usr/share/openpyn/credentials with openvpn",
              "compatible 'auth-user-pass' file format\n")

        username = input("Enter your username for NordVPN, i.e youremail@yourmail.com: ")
        password = input("Enter the password for NordVPN: ")
        command_1 = "sudo echo " + '"%s"' % username + " > /usr/share/openpyn/credentials"
        command_2 = "sudo echo " + '"%s"' % password + " >> /usr/share/openpyn/credentials"
        try:
            # create Empty file with 600 permissions
            subprocess.call("sudo touch /usr/share/openpyn/credentials".split())
            subprocess.check_call(command_1, shell=True)
            subprocess.check_call(command_2, shell=True)
            subprocess.check_call("sudo chmod 600 /usr/share/openpyn/credentials".split())

            print("Awesome, the credentials have been saved in '/usr/share/openpyn/credentials'\n")
        except subprocess.CalledProcessError:
            print("Your OS is not letting modify /usr/share/openpyn/credentials",
                  "Please run with 'sudo' to store credentials")
            subprocess.call("sudo rm /usr/share/openpyn/credentials".split())
            sys.exit()
    return
