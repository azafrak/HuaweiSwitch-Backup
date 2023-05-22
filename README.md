# Huawei Switch Multi Devices Backup
S5700 series switch batch backup (multi-process concurrency)

### Project Features
The original of the project; https://github.com/hzh1019
Developed on the original project.

I customized the project for my own purposes. This project ensures that the configurations of the S5700 series Switches that we use within the company are recorded periodically.

Since there are so many switches, it takes time to check them all one by one. This project automates the whole process.

The program runs the following commands one after the other.

1. save config.cfg (saves current config)
2. y (confirmation given to overwrite existing file)
3. tftp 172.16.2.119 put flash:/config.cfg (this command sends the saved config file to the specified IP address via TFTP)

### Environment Requirements
1. Python3
2. TFTP Server (I am using Tftp64)
3. Switch login information

### How to use?
1. Put Switch_AutoBackup.py, switchs.txt and credentials.json in the same directory.
2. Edit the contents of the credentials.json file. Enter your telnet information.
3. Edit switchs.txt and fill in the management IP addresses of the switches that need to be backed up. One switch per line.
```
172.16.1.10
172.16.1.12
etc
```
4. Set the following command as a Windows or Linux scheduled task according to your needs.
```
python3 Switch_AutoBackup.py
or
python Switch_AutoBackup.py
```