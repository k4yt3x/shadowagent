# ShadowAgent

## Current Version: 1.2

### Prerequisites
+ Linux
+ For other prerequisites please see DEPENDENCIES.md

<br>

### What is ShadowAgent?
ShadowAgent is a SilkRoad VPN Controller. It is currently a fully functioning Shadowsocks client.  This program is a part of the Sakura One Project, which is a project designed for modifying shadowsocks against censorship.

<br>

### Download & Install
First you'll need shadowsocks.  
You can install shadowsocks package however you want. Here's an example for installing shadowsocks with pip. root privilege is optional.
~~~~
$ pip install git+https://github.com/shadowsocks/shadowsocks.git@master
~~~~

Then clone and install shadowagent
~~~~
$ git clone https://github.com/K4YT3X/shadowagent.git && cd shadowagent/
$ sudo python3 shadowagent.py --install  # And the program is installed
~~~~
<br>

### Usage
As shown in the program help page, here are the commands
**Note that the program needs to run a setup wizard when first being used**
~~~~
usage: sa [-h] [--start] [--stop] [--status] [-s S] [--install] [--uninstall]
          [--reconfigure] [--version]

optional arguments:
  -h, --help     show this help message and exit

Controls:
  --start        Start connection to a server
  --stop         Stop currently running sessions
  --status       Check ShadowAgent status
  -s S           Start a server by index

Installation:
  --install      Install ShadowAgent to system
  --uninstall    Uninstall ShadowAgent from system
  --reconfigure  Reconfigure servers

Extra:
  --version      Show SCUTUM version and exit
~~~~