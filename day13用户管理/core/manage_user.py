from db import data

class HostManage(object):
    def __init__(self):
        '''获取user,password,type'''
        self.user_obj = data.Operation_db()
        self.username_dic = self.user_obj.check_data()

    def run(self):
        msg = '''
        *  check
        *  add
        *  remove
        *  change
        '''
        while True:
            print(msg)
            user_choice= input('请选择(q退出):').strip()
            if user_choice == 0:continue
            if user_choice == 'q':break
            if hasattr(self,user_choice):
                func = getattr(self,user_choice)
                func()


    def check(self):
        self.user_obj = data.Operation_db()
        self.username_dic = self.user_obj.check_data()
        print('\033[31;1m当前用户如下\033[0m'.center(30, '*'))
        for item in self.username_dic:
            print('user:%s  password:%s  type:%s' % (item,self.username_dic[item]['password'],self.username_dic[item]['type']))

    def add(self):
        while True:
            self.user_obj = data.Operation_db()
            self.username_dic = self.user_obj.check_data()
            username = input('输入新增用户名字(q退出):').strip()
            if username == 'q':break
            if username in self.username_dic.keys():
                print('用户已存在')
                break
            password = input('输入新增用户密码:').strip()
            type = int(input('用户类型(1:root 2:regular):').strip())
            extra = input('其他:').strip()
            obj = data.Operation_db()
            obj.add_user(username,password,type,extra)
    def remove(self):
        while True:
            self.user_obj = data.Operation_db()
            self.username_dic = self.user_obj.check_data()
            username = input('输入删除用户(q退出):').strip()
            if username == 'q':break
            if username not in self.username_dic.keys():
                print('用户不存在')
                break

            obj = data.Operation_db()
            obj.remove_user(username)
            print('\033[31;1m删除成功\033[0m')

    def change(self):
        pass