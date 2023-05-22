import logging
import telnetlib
import time
import datetime
from multiprocessing import Pool
import json


class TelnetClient():
    def __init__(self):
        self.tn = telnetlib.Telnet()
        self.credentials = self.load_credentials()

    # This function implements telnet login host
    def login_host(self, host_ip):
        try:
            self.tn.open(host_ip, port=23)
        except:
            logging.warning('%s network connection failed' % host_ip)
            return False

        # Wait for the login to appear and enter the user name, wait up to 10 seconds
        self.tn.read_until(b'Username: ', timeout=10)
        self.tn.write(self.credentials['username'].encode('ascii') + b'\n')
        # Wait for the Password to appear and then enter the user name, wait up to 10 seconds
        self.tn.read_until(b'Password: ', timeout=10)
        self.tn.write(self.credentials['password'].encode('ascii') + b'\n')
        # Give two seconds of latency before getting the results, this way give the server adequate response time
        time.sleep(2)
        # Get login result
        command_result = self.tn.read_very_eager().decode('ascii')
        if 'Login failed' not in command_result:
            logging.warning('%s login successful' % host_ip)
            return True
        else:
            logging.warning('%s Login failed, wrong username or password' % host_ip)
            return False

    # This function implements the command passed in and outputs its execution result
    def execute_some_command(self, command):
        # Excuting an command
        self.tn.write(command.encode('ascii') + b'\n')
        time.sleep(2)
        # get command result
        command_result = self.tn.read_very_eager().decode('ascii')
        logging.warning('command execution result:\n%s' % command_result)

    # exit telnet
    def logout_host(self):
        self.tn.write(b"quit\n")

    def load_credentials(self):
        with open('credentials.json') as f:
            data = json.load(f)
        return data


def switchbak(host_ip, command1, command2, command3, command4, command5):
    telnet_client = TelnetClient()

    # Login to the telnet using the provided host IP
    if telnet_client.login_host(host_ip):
        
        telnet_client.execute_some_command(command1)  # Execute the first command
        telnet_client.execute_some_command(command2)  # Execute the second command

        time.sleep(5) # Waits 5 seconds for the command to be executed
        telnet_client.execute_some_command(command3)  # Execute the third command

        telnet_client.execute_some_command(command4)  # Execute the fourth command
        telnet_client.execute_some_command(command5)  # Execute the fifth command

        # Logout from the telnet
        telnet_client.logout_host()


if __name__ == '__main__':
    print('It started simultaneous backup')
    start = time.time()

    p = Pool(50)
    for ip in open('switchs.txt').readlines():
        ip = ip.strip()

        ftphost = '172.16.2.119'
        filename = ip.replace('.', '-') + '-' + datetime.date.today().strftime('%Y%m%d') + '.cfg'
        command1 = 'save config.cfg'
        command2 = 'y'
        command3 = 'tftp ' + ftphost + ' put flash:/config.cfg ' + filename
        command4 = 'save'
        command5 = 'y'

        p.apply_async(switchbak, args=(ip, command1, command2, command3, command4, command5,))

    p.close()
    p.join()
    end = time.time()
    print('Backup complete, time taken: %0.2f seconds' % (end - start))
