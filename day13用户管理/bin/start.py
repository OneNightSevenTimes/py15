import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from conf import settings
from db import data
from core import auth
from core import manage_user_type

msg = '''
    1.用户类型管理
    2.用户管理
    3.主机表管理
    4.分配主机
    5.退出
'''
menu = {
    '1':manage_user_type.type
}

def get_data():
    '''获取user,password,type'''
    user_obj = data.Operation_db()
    username_dic = user_obj.check_data()
    return username_dic

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
