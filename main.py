#!/usr/bin/env python3

from netmiko import ConnectHandler
import sys
import re

key = '~/.ssh/dell-admin'
hosts = [list of switch host names or ips]
domain = 'your domain'
use_domain = True
user = 'your switch user'
dev_type = 'dell_os6'
mac = sys.argv[1]
command = f'show mac address-table address {mac}'

for host in hosts:
    if use_domain == True:
        name = host
        host = f'{host}.{domain}'
    dev_cx = {
        'device_type': dev_type,
        'host': host,
        'username': user,
        'use_keys': True,
        'key_file': key
    }
    
    with ConnectHandler(**dev_cx) as cx:
        cx.send_command("enable")
        output = cx.send_command(command)
  
    for line in output.splitlines():
        if len(line):
            if line[0].isdigit():
                #print(f'{host} {line}')
                values = re.split(r' {2,}', line)
                print(f'{name.ljust(16)}{values[0].ljust(16)}\t\t{values[1].ljust(16)}\t\t{values[2].ljust(16)}\t\t{values[3].ljust(16)}')
       
    cx.disconnect()
