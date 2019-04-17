#!/usr/bin/python3
"""
Usage:
  noexpire.py -h | --help
  noexpire.py (--vcenter=<vcenter> --vcenter_pass=<vcenter_pass> --username=<username> --username_pass=<username_pass>)
 
Options:
  --vcenter=<vcenter>
  --vcenter_pass=<vcenter_pass>
  --username=<username>
  --username_pass=<username_pass>
"""
import paramiko

from pyVmomi import vim
from docopt import docopt
from getpass import getpass
from pyVim.connect import SmartConnect


def login_ssh(target, vc_local_user, vc_password, user_pass):
    cmd = "/usr/lib/vmware-vmafd/bin/dir-cli user modify --account administrator --password-never-expires --password {}".format(user_pass)
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.WarningPolicy)
    client.connect(
        hostname=target,  
        username=vc_local_user, 
        password=vc_password, 
        )
    stdin, stdout, stderr = client.exec_command('shell {}'.format(cmd))
    print(stderr.readlines())
    print(stdout.readlines())    

def main():
    opts = docopt(__doc__)
    vc = opts['--vcenter']
    vc_pass = opts['--vcenter_pass']
    user = opts['--username']
    user_pass=opts['--username_pass']

    ssh_session = login_ssh(
        target=vc,
        vc_local_user='root',
        vc_password=vc_pass,
        user_pass=user_pass
    )

if __name__ == '__main__':
    main()
