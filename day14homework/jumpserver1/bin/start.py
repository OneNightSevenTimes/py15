import sys
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from core import main
from db import module
from core import ssh
if __name__ == '__main__':
    msg = '''
    ###    欢迎使用跳板机系统   ###
        1.当前用户的主机列表

    '''
    menu = {
        '1':module.list_host,

    }
    while True:
        print('\033[32;1m%s\033[0m'%msg)
        choice = input('\033[32;1mOpt,IP,hostname or ID>:\033[0m').strip()
        if len(choice) == 0:continue
        if choice not in menu:continue
        username = os.environ['USER']
        menu[choice](username)
        choice = input('\033[32;1mOpt,IP,hostname or ID>:\033[0m').strip()#主机ip
        username = input('\033[32;1m选择用户:\033[0m').strip()#主机用户
        password = module.get_passwd(username,choice)
        ssh.connect(choice,username)



