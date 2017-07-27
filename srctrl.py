#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
  ____    ____             ____   _____   ____    _
 / ___|  |  _ \           / ___| |_   _| |  _ \  | |
 \___ \  | |_) |         | |       | |   | |_) | | |
  ___) | |  _ <          | |___    | |   |  _ <  | |___
 |____/  |_| \_\  _____   \____|   |_|   |_| \_\ |_____|
                 |_____|


Name: SR_CTRL
Author: K4YT3X
Description: SR_CTRL stands for "Silkroad Controller". It is essentially a
shadowsocks client for now. However, in the future, it will become a client for
shadowgate

Date of Creation: July 27,2017
Last Modified: July 27,2017

Licensed under the GNU General Public License Version 3 (GNU GPL v3),
    available at: https://www.gnu.org/licenses/gpl-3.0.txt

(C) 2017 K4YT3X
"""

import configparser
import os
import psutil
import re
import sys

try:
    import avalon_framework as avalon
except ImportError:
    while True:
        install = input('\033[31m\033[1mAVALON Framework not installed! Install now? [Y/n] \033[0m')
        if len(install) == 0 or install[0].upper() == 'Y':
            try:
                if os.path.isfile('/usr/bin/pip3'):
                    print('Installing using method 1')
                    os.system('pip3 install avalon_framework')
                elif os.path.isfile('/usr/bin/wget'):
                    print('Installing using method 2')
                    os.system('wget -O - https://bootstrap.pypa.io/get-pip.py | python3')
                    os.system('pip3 install avalon_framework')
                else:
                    print('Installing using method 3')
                    import urllib.request
                    content = urllib.request.urlopen('https://bootstrap.pypa.io/get-pip.py')
                    with open('/tmp/get-pip.py', 'w') as getpip:
                        getpip.write(content.read().decode())
                        getpip.close()
                    os.system('python3 /tmp/get-pip.py')
                    os.system('pip3 install avalon_framework')
                    os.remove('/tmp/get-pip.py')
            except Exception as e:
                print('\033[31mInstallation failed!: ' + str(e))
                print('Please check your Internet connectivity')
                exit(0)
            print('\033[32mInstallation Succeed!\033[0m')
            print('\033[32mPlease restart the program\033[0m')
            exit(0)
        elif install[0].upper() == 'N':
            print('\033[31m\033[1mSCUTUMM requires avalon framework to run!\033[0m')
            print('\033[33mAborting..\033[0m')
            exit(0)
        else:
            print('\033[31m\033[1mInvalid Input!\033[0m')

CONFPATH = '/etc/srctrl.conf'
PIDF = '/var/run/shadowsocks.pid'
VERSION = '1.0 alpha'


# -------------------------------- Classses --------------------------------

class silkroad:

    def start():
        avalon.info('Starting silkroad VPN')
        if not silkroad.is_running():
            os.system('/usr/bin/sslocal -s ' + server_addr + ' -p ' + server_port + ' -k ' + server_pswd + ' -b 127.0.0.1 -l ' + local_port + ' -m ' + encryption_method + ' -d start')
        else:
            avalon.error(avalon.FM.RBD + 'Silkroad VPN is ' + avalon.FM.BD + 'already running')

    def stop():
        avalon.info('Shutting VPN down')
        if not os.path.isfile(PIDF):
            avalon.error(avalon.FM.RBD + 'Silkroad VPN is ' + avalon.FM.BD + 'NOT STARTED')
        with open(PIDF, 'r') as pidf:
            for line in pidf:
                if psutil.pid_exists(int(line)):
                    avalon.subLevelTimeInfo('Killing PID ' + line)
                    os.system('kill -9 ' + line)
                    return 0
                else:
                    avalon.error(avalon.FM.RBD + 'Silkroad VPN is ' + avalon.FM.BD + 'NOT RUNNING')

    def is_running():
        if os.path.isfile(PIDF):
            with open(PIDF, 'r') as pidf:
                for line in pidf:
                    if psutil.pid_exists(int(line)):
                        return True
        return False


# -------------------------------- Functions --------------------------------


def validIP(s):
    a = s.split('.')
    if len(a) != 4:
        return False
    for x in a:
        if not x.isdigit():
            return False
        i = int(x)
        if i < 0 or i > 255:
            return False
    return True


def validDomain(hostname):
    if len(hostname) > 255:
        return False
    if hostname[-1] == ".":
        hostname = hostname[:-1]  # strip exactly one dot from the right, if present
    allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
    return all(allowed.match(x) for x in hostname.split("."))


def print_help():
    print(avalon.FM.BD + '[USAGE]\n' + avalon.FM.RST)
    print(avalon.FG.Y + 'srctrl              ' + avalon.FM.BD + '# Print Help' + avalon.FM.RST)
    print(avalon.FG.Y + 'srctrl start        ' + avalon.FM.BD + '# Start VPN' + avalon.FM.RST)
    print(avalon.FG.Y + 'srctrl stop         ' + avalon.FM.BD + '# Stop VPN' + avalon.FM.RST)
    print(avalon.FG.Y + 'srctrl status       ' + avalon.FM.BD + '# Check VPN status' + avalon.FM.RST)
    print(avalon.FG.Y + 'srctrl reconfigure  ' + avalon.FM.BD + '# Reconfigure SRCTRL' + avalon.FM.RST)


def print_logo():
    print(avalon.FM.BD + avalon.FG.B + '  ____    ____  ' + avalon.FM.RST + '           ____   _____   ____    _')
    print(avalon.FM.BD + avalon.FG.B + ' / ___|  |  _ \\ ' + avalon.FM.RST + '          / ___| |_   _| |  _ \\  | |')
    print(avalon.FM.BD + avalon.FG.B + ' \\___ \\  | |_) |' + avalon.FM.RST + '         | |       | |   | |_) | | |')
    print(avalon.FM.BD + avalon.FG.B + '  ___) | |  _ < ' + avalon.FM.RST + '         | |___    | |   |  _ <  | |___')
    print(avalon.FM.BD + avalon.FG.B + ' |____/  |_| \\_\\' + avalon.FM.RST + '  _____   \\____|   |_|   |_| \\_\\ |_____|')
    print(avalon.FM.BD + avalon.FG.B + '                ' + avalon.FM.RST + ' |_____|')
    spaces = ((56 - len('Silkroad VPN Controller ' + VERSION)) // 2) * ' '
    print(avalon.FM.BD + '\n' + spaces + 'Silkroad VPN Controller ' + VERSION + '\n' + avalon.FM.RST)


def setup_wizard():
    avalon.info('Setup Wizard Started')
    config = configparser.ConfigParser()
    config['SERVERS'] = {}
    config['PORTS'] = {}
    config['LOCALPORTS'] = {}
    config['PASSWORDS'] = {}
    config['ENCRYPTIONS'] = {}
    while True:
        while True:
            server_name = avalon.gets('Server Name: ')
            if server_name == '':
                    avalon.error('Invalid Input!')
            else:
                break
        while True:
            server_addr = avalon.gets('Server Address: ')
            if validIP(server_addr) or validDomain(server_addr):
                break
            else:
                avalon.error('Invalid Input! IP addresses or domains only!')
        while True:
            server_port = avalon.gets('Server Port [1080]: ')
            if server_port.isdigit():
                if not (int(float(server_port)) > 65535 or int(float(server_port)) < 1):
                    break
            elif server_port == '':
                server_port = '1080'
                break
            else:
                avalon.error('Invalid Input! Not a port number!')
        while True:
            local_port = avalon.gets('Local Port [1080]: ')
            if local_port.isdigit():
                if not (int(float(local_port)) > 65535 or int(float(local_port)) < 1):
                    break
            elif local_port == '':
                local_port = '1080'
                break
            else:
                avalon.error('Invalid Input! Not a port number!')
        while True:
            encryption_method = avalon.gets('Encryption Method: ')
            if encryption_method == '':
                    avalon.error('Invalid Input!')
            else:
                break
        while True:
            server_pswd = avalon.gets('Server Password: ')
            if server_pswd == '':
                    avalon.error('Invalid Input!')
            else:
                break
        config['SERVERS'][server_name] = server_addr
        config['PORTS'][server_name] = server_port
        config['LOCALPORTS'][server_name] = local_port
        config['PASSWORDS'][server_name] = server_pswd
        config['ENCRYPTIONS'][server_name] = encryption_method
        if avalon.ask('Add another server?'):
            pass
        else:
            break
    avalon.info('Set-up Completed!')
    avalon.info('Writing configuration file to ' + CONFPATH)
    with open(CONFPATH, 'w') as configfile:
        config.write(configfile)  # Writes configurations
    avalon.info('Writing success!')
    avalon.info('Please relaunch application')
    exit(0)


def select_server():
    """
        List all servers and let the use choose
    """
    id = 0
    servers_numerical = []
    print(avalon.FM.BD + '\n[SERVERS]\n' + avalon.FM.RST)
    for server in servers:
        servers_numerical.append(server)
    for server in servers:
        print(avalon.FG.Y + str(id) + ': ' + avalon.FM.RST + servers[server])
        id += 1
    print('')
    while True:
        serverid = avalon.gets('Select Server #: ')
        try:
            return servers_numerical[int(serverid)]
            break
        except IndexError:
            avalon.error('Selected Server not found!')


def parse_config():
    """
        Reads all configuration files
    """
    if not os.path.isfile(CONFPATH):
        avalon.warning('Config File Not Found!')
        if avalon.ask('Start Set-up Wizard?', True):
            setup_wizard()
        else:
            avalon.error('No configuration file found!')
            avalon.error('Please initialize the config file!')
            exit(0)
    else:
        config = configparser.ConfigParser()
        config.read(CONFPATH)
        config.sections()
        servers = config['SERVERS']
        return servers


# -------------------------------- Procedural --------------------------------

print_logo()

if os.getuid() != 0:
    avalon.error('This application must be run as root!')
    exit(0)

servers = parse_config()

try:
    if sys.argv[1].upper() == 'START':
        server_name = select_server()
        config = configparser.ConfigParser()
        config.read(CONFPATH)
        config.sections()
        servers = config['SERVERS']
        ports = config['PORTS']
        localports = config['LOCALPORTS']
        passwords = config['PASSWORDS']
        encryptions = config['ENCRYPTIONS']
        server_port = ports[server_name]
        local_port = localports[server_name]
        server_addr = servers[server_name]
        server_pswd = passwords[server_name]
        encryption_method = encryptions[server_name]
        silkroad.start()
        avalon.info('OK')
    elif sys.argv[1].upper() == 'STOP':
        silkroad.stop()
        avalon.info('OK')
    elif sys.argv[1].upper() == 'STATUS':
        if silkroad.is_running():
            print(avalon.FM.BD + '[+] Silkroad: ' + avalon.FG.G + 'RUNNING' + avalon.FM.RST)
        else:
            print(avalon.FM.BD + '[+] Silkroad: ' + avalon.FG.R + 'STOPPED' + avalon.FM.RST)
        exit(0)
    elif sys.argv[1].upper() == 'INSTALL':
        avalon.info('Installing SR_CTRL')
        os.system('cp ' + os.path.abspath(__file__) + ' /usr/bin/srctrl')  # os.rename throws an error when /tmp is in a separate partition
        os.system('chown root: /usr/bin/srctrl')
        os.system('chmod 755 /usr/bin/srctrl')
        avalon.info('Installation Complete!')
        avalon.info('Now you can use "srctrl" command to start SR_CTRL')
        if os.path.isfile(CONFPATH):
            if avalon.ask('Config file already exists. Overwrite?', False):
                setup_wizard()
            else:
                exit(0)
        else:
            setup_wizard()
    elif sys.argv[1].upper() == 'RECONFIGURE':
        avalon.warning('Reconfiguring will purge all settings!')
        if avalon.ask('Are you sure that you want to reconfigure silkroad VPN client?', False):
            print('\nAlright then ~\n')
            setup_wizard()
        else:
            avalon.warning('Aborting reconfiguration')
            exit(0)
    else:
        avalon.error('Unrecognized Option: ' + sys.argv[1] + '\n')
        print_help()
except IndexError:
    print_help()
    exit(0)
except Exception as e:
    avalon.error(str(e))
    exit(1)
