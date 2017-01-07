from db import data

class HostToUser(object):
    def __init__(self):
        '''获取user,password,type'''
        self.user_obj = data.Operation_db()
        self.username_dic = self.user_obj.check_host_data()

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
        self.username_dic = self.user_obj.check_host_data()
        print(self.username_dic)
        print('\033[31;1m当前主机&&用户如下\033[0m'.center(30, '*'))
        for item in self.username_dic:
            print('主机:%s  用户:%s' % (item,self.username_dic[item]['用户']))

    def add(self):
        while True:
            self.user_obj = data.Operation_db()

            self.username_dic = self.user_obj.check_host_data()
            hostname = input('选择主机名字(q退出):').strip()
            if hostname == 'q':break
            if hostname not in self.username_dic.keys():
                print('主机不存在')
                break
            user = input('选择用户:').strip()
            if user in self.username_dic[hostname]['用户']:
                print('用户已有权限')
            else:
                obj = data.Operation_db()
                obj.add_host_user(hostname,user)
                print('授权成功')
    def remove(self):
        while True:
            self.user_obj = data.Operation_db()
            self.username_dic = self.user_obj.check_host_data()
            host = input('输入主机(q退出):').strip()
            if host == 'q':break
            if host not in self.username_dic.keys():
                print('主机不存在')
                break
            user = input('输入删除的用户').strip()
            if user not in self.username_dic[host]['用户']:
                print('用户无机器权限')
            else:
                obj = data.Operation_db()
                obj.remove_host_user(host,user)
                print('\033[31;1m删除成功\033[0m')

    def change(self):
        pass