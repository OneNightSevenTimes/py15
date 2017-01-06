import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from conf import settings
from db import data
from core import auth

msg = '''
    1.用户类型管理
    2.用户管理
    3.主机表管理
    4.分配主机
    5.退出
'''
menu = {
    '1':data.Operation_db
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
            obj = menu[user_choice]()#Operation_db
            choose(obj)

def choose(obj):
    while True:
        dic = obj.check_data()
        print(dic)
        change_user = input('输入需要修改类型的用户(q退出):').strip()
        username_dic = get_data()
        if change_user in username_dic.keys():
            change_type = input('输入需要之后的类型：').strip()
        elif change_user == 'q':
            break
        else:
            print('修改用户不存在')
            break
        obj.change_type(change_user, change_type)



if __name__ == '__main__':
    main()
