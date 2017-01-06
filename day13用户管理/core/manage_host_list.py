from db import data

class host(object):
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
        self.username_dic = self.user_obj.check_host_data()
        print(self.username_dic)
        print('\033[31;1m当前主机列表如下\033[0m'.center(30, '*'))
        for i in self.username_dic.keys():
            print('主机:%s IP:%s 端口:%s 用户:%s' %(i,\
                                              self.username_dic[i]['IP'],\
                                              self.username_dic[i]['端口'],\
                                              self.username_dic[i]['用户']))
    def add(self):
        while True:
            self.user_obj = data.Operation_db()
            self.username_dic = self.user_obj.check_host_data()
            host = input('输入主机名(q退出):').strip()
            if host in self.username_dic.keys():
                print('主机名已存在')
                break
            if host == 'q':break
            ip = input('输入ip:').strip()
            port = input('输入端口:').strip()

            obj = data.Operation_db()
            obj.add_host(host,ip,port)

    def remove(self):
        while True:
            self.user_obj = data.Operation_db()
            self.username_dic = self.user_obj.check_host_data()
            hostname = input('输入删除主机(q退出):').strip()
            if hostname == 'q':break
            if len(hostname) == 0:continue
            if hostname not in self.username_dic.keys():
                print('主机不存在')
                break
            obj = data.Operation_db()
            obj.remove_host(hostname)

    def change(self):
        while True:
            self.user_obj = data.Operation_db()
            self.username_dic = self.user_obj.check_host_data()
            hostname = input('输入修改主机(q退出):').strip()
            if hostname == 'q':break
            if len(hostname) == 0:continue
            if hostname not in self.username_dic.keys():
                print('主机不存在')
                break
            ip = input('输入ip:').strip()
            port = input('输入端口:').strip()
            obj = data.Operation_db()
            obj.change_host(hostname,ip,port)

