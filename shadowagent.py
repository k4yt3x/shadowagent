#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
   ____   __            __                ___                     __
  / __/  / /  ___ _ ___/ / ___  _    __  / _ |  ___ _ ___   ___  / /_
 _\ \   / _ \/ _ `// _  / / _ \| |/|/ / / __ | / _ `// -_) / _ \/ __/
/___/  /_//_/\_,_/ \_,_/  \___/|__,__/ /_/ |_| \_, / \__/ /_//_/\__/
                                              /___/


Name: ShadowAgent
Author: K4YT3X
Description: ShadowAgent stands for "Silkroad Controller". It is essentially a
shadowsocks client for now. However, in the future, it is expected to become a
client for shadowgate

Date of Creation: July 27,2017
Last Modified: March 13,2018

Licensed under the GNU General Public License Version 3 (GNU GPL v3),
    available at: https://www.gnu.org/licenses/gpl-3.0.txt

(C) 2017 - 2018 K4YT3X
"""

import argparse
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

CONFPATH = '/etc/shadowagent.conf'
if os.getuid() == 0:
    PIDF = '/var/run/shadowsocks.pid'
    LOGF = '/var/log/shadowsocks.log'
else:
    PIDF = '/tmp/shadowsocks.pid'
    LOGF = '/tmp/shadowsocks.log'
VERSION = '1.2'


# -------------------------------- Classses --------------------------------

class silkroad:

    def start():
        avalon.info('Starting silkroad VPN')
        if not silkroad.is_running():
            os.system('/usr/bin/env sslocal -s {} -p {} -k {} -b 127.0.0.1 -l {} -m {} --pid-file={} --log-file={} -d start'.format(
                server_addr, server_port, server_pswd, local_port, encryption_method, PIDF, LOGF))
        else:
            avalon.error(avalon.FM.RBD + 'Silkroad VPN is ' + avalon.FM.BD + 'already running')

    def stop():
        avalon.info('Shutting VPN down')
        if not os.path.isfile(PIDF):
            avalon.error(avalon.FM.RBD + 'Silkroad VPN is ' + avalon.FM.BD + 'NOT STARTED')
        with open(PIDF, 'r') as pidf:
            for line in pidf:
                if psutil.pid_exists(int(line)):
                    avalon.dbgInfo('Killing PID ' + line)
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


def process_args():
    parser = argparse.ArgumentParser()
    control_group = parser.add_argument_group('Controls')
    control_group.add_argument("--start", help="Start connection to a server", action="store_true", default=False)
    control_group.add_argument("--stop", help="Stop currently running sessions", action="store_true", default=False)
    control_group.add_argument("--status", help="Check ShadowAgent status", action="store_true", default=False)
    control_group.add_argument("-s", help="Start a server by index", action="store", default=False)
    inst_group = parser.add_argument_group('Installation')
    inst_group.add_argument("--install", help="Install ShadowAgent to system", action="store_true", default=False)
    inst_group.add_argument("--uninstall", help="Uninstall ShadowAgent from system", action="store_true", default=False)
    inst_group.add_argument("--reconfigure", help="Reconfigure servers", action="store_true", default=False)
    etc = parser.add_argument_group('Extra')
    etc.add_argument("--version", help="Show SCUTUM version and exit", action="store_true", default=False)
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    return parser.parse_args()


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
    print(avalon.FG.Y + 'sa              ' + avalon.FM.BD + '# Print Help' + avalon.FM.RST)
    print(avalon.FG.Y + 'sa start        ' + avalon.FM.BD + '# Start VPN' + avalon.FM.RST)
    print(avalon.FG.Y + 'sa stop         ' + avalon.FM.BD + '# Stop VPN' + avalon.FM.RST)
    print(avalon.FG.Y + 'sa status       ' + avalon.FM.BD + '# Check VPN status' + avalon.FM.RST)
    print(avalon.FG.Y + 'sa reconfigure  ' + avalon.FM.BD + '# Reconfigure ShadowAgent' + avalon.FM.RST)
    print(avalon.FG.Y + 'sa install      ' + avalon.FM.BD + '# Install ShadowAgent' + avalon.FM.RST)


def print_logo():
    print('     ____   __            __                ___                     __')
    print('    / __/  / /  ___ _ ___/ / ___  _    __  / _ |  ___ _ ___   ___  / /_')
    print('   _\ \   / _ \/ _ `// _  / / _ \| |/|/ / / __ | / _ `// -_) / _ \/ __/')
    print('  /___/  /_//_/\_,_/ \_,_/  \___/|__,__/ /_/ |_| \_, / \__/ /_//_/\__/')
    print('                                                /___/')
    spaces = ((70 - len('Silkroad VPN Controller ' + VERSION)) // 2) * ' '
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


def select_server(serverid=False):
    """
        List all servers and let the use choose
    """
    id = 0
    servers_numerical = []
    print(avalon.FM.BD + '\n[SERVERS]\n' + avalon.FM.RST)
    for server in servers:
        servers_numerical.append(server)
    for server in servers:
        print(avalon.FG.Y + str(id) + ': ' + avalon.FM.RST + server)
        id += 1
    print('')
    if serverid is False:
        while True:
            serverid = avalon.gets('Select Server #: ')
            try:
                return servers_numerical[int(serverid)]
                break
            except IndexError:
                avalon.error('Selected Server not found!')
    else:
        return servers_numerical[int(serverid)]


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

servers = parse_config()
args = process_args()

os.system('clear')
print('\n\n')
print_logo()

if args.version:  # prints program legal / dev / version info
    print("Current Version: " + VERSION)
    print("Author: K4YT3X")
    print("License: GNU GPL v3")
    print("Github Page: https://github.com/K4YT3X/shadowagent")
    print("Contact: k4yt3x@protonmail.com")
    print()
    exit(0)


if args.start or args.s:
    server_name = select_server(args.s)
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
    if int(local_port) < 1025 and os.getuid() != 0:
        avalon.error('This application must be run as root to bind on port {}'.format(local_port))
        exit(1)
    silkroad.start()
    avalon.info('OK')
elif args.stop:
    silkroad.stop()
    avalon.info('OK')
elif args.status:
    if silkroad.is_running():
        print(avalon.FM.BD + '[+] Silkroad: ' + avalon.FG.G + 'RUNNING' + avalon.FM.RST)
    else:
        print(avalon.FM.BD + '[+] Silkroad: ' + avalon.FG.R + 'STOPPED' + avalon.FM.RST)
    exit(0)
elif args.install:
    avalon.info('Installing ShadowAgent')
    os.system('cp ' + os.path.abspath(__file__) + ' /usr/bin/sa')  # os.rename throws an error when /tmp is in a separate partition
    os.system('chown root: /usr/bin/sa')
    os.system('chmod 755 /usr/bin/sa')
    avalon.info('Installation Complete!')
    avalon.info('Now you can use "sa" command to start ShadowAgent')
    if os.path.isfile(CONFPATH):
        if avalon.ask('Config file already exists. Overwrite?', False):
            setup_wizard()
        else:
            exit(0)
    else:
        setup_wizard()
elif args.reconfigure:
    avalon.warning('Reconfiguring will purge all settings!')
    if avalon.ask('Are you sure that you want to reconfigure silkroad VPN client?', False):
        print('\nAlright then ~\n')
        setup_wizard()
    else:
        avalon.warning('Aborting reconfiguration')
        exit(0)
