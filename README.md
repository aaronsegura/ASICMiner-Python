ASICMiner-Python
================

Python class and scripts for interrogating and configuring Bitfountain ASICMiner Blades (v2)

blade.py
--------

Python class file for ASICMiner blades.  See bm.py for example usage.


bm.py
-----

THE BLADEMANGLER

Configuration utility for ASICMiner blades.  Requires blade.py.


    $ python ./bm.py  -h
    usage: bm.py [-h] [-S | -U | -v] [--address <address>] [--netmask <netmask>]
                [--gw <address>] [--pdns <host>] [--sdns <host>]
                [--phost <host:port>] [--puser <user:pass>] [--shost <host:port>]
                [--suser <user:pass>] [--webport <port>]
                host:port [host:port ...]
    
    Tool to manipulate BitFountain ASICMINER v2 Blades
    
    positional arguments:
      host:port            Target Blade IPs
    
    optional arguments:
      -h, --help           show this help message and exit
      -S                   Switch Servers
      -U                   Update Configuration
      -v                   Display all details about blade(s)
    
      Update Flags:
    
      --address <address>  IP Address
      --netmask <netmask>  Netmask
      --gw <address>       Gateway
      --pdns <host>        Primary DNS Server
      --sdns <host>        Secondary DNS Server
      --phost <host:port>  Primary Mining Server
      --puser <user:pass>  Primary Server Credentials
      --shost <host:port>  Secondary Mining Server
      --suser <user:pass>  Secondary Server Credentials
      --webport <port>     Web UI Listening Port

If passed with no command line options, a short one-line summary is given showing the current server and hashrate:

    $ python ./bm.py 192.168.1.200:8000
    [192.168.1.200:8000] 172.16.0.2:8332 @ 11006 MH/s


You may also pass multiple blades on the same cmdline:

    $ python ./bm.py 192.168.1.200:8000 192.168.1.201:8000 192.168.1.202:8000
    [192.168.1.200:8000] 172.16.0.2:8332 @ 10738 MH/s
    [192.168.1.201:8000] 172.16.0.2:8332 @ 11040 MH/s
    [192.168.1.202:8000] 172.16.0.2:8332 @ 10492 MH/s

This also works for bulk updates:

    $ python ./bm.py -U --phost 172.16.0.2:8332 --puser user:pass 192.168.1.200:8000 192.168.1.201:8000 ...


cacti/get_ASICMiner.py
----------------

Script used in conjunction with cacti/cacti_host_template_asicminer_blade.xml

Put this script in your cacti scripts directory and make it executable.  Then import the .xml template file via the cacti web interface.

http://www.cacti.net/

