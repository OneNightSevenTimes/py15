import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from conf import settings
from db import data
from core import auth
from core import manage_user_type
from core import manage_user
from core import manage_host_list
from core import manage_host_to_user

msg = '''
    1.用户类型管理
    2.用户管理
    3.主机表管理
    4.分配主机
    5.退出
'''
menu = {
    '1':manage_user_type.type,
    '2':manage_user.HostManage,
    '3':manage_host_list.host,
    '4':manage_host_to_user.HostToUser

}


def main():
    obj_login = auth.auth()
    status = obj_login.main()#是否登录成功
    if status:
        while True:
            print(msg)
            user_choice = input('请选择:').strip()
            obj = menu[user_choice]()
            obj.run()

if __name__ == '__main__':
    main()
