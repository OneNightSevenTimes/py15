from db import data
import xlrd
import xlwt
import time
import os

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
        username_dic = self.user_obj.check_host_data()
        print(username_dic)
        print('\033[31;1m当前主机列表如下\033[0m'.center(30, '*'))
        for i in username_dic.keys():
            print('主机:%s IP:%s 端口:%s 用户:%s' %(i,\
                                              username_dic[i]['IP'],\
                                              username_dic[i]['端口'],\
                                              username_dic[i]['用户']))
        choice = input('是否导出excel(,yes导出,q退出):').strip()
        if choice == 'yes':
            location = input('输入保存文件名：')
            self.write(location,username_dic)


    def read(self,location):
        self.user_obj = data.Operation_db()
        self.username_dic = self.user_obj.check_host_data()

        data1 = xlrd.open_workbook(location)
        table = data1.sheets()[0]

        # print(table)
        nrows = table.nrows  # 行
        ncols = table.ncols  # 列
        # print(nrows)
        # print(ncols)
        for rownum in range(1, table.nrows):
            value = table.row_values(rownum)
            host = value[0]
            ip = value[1]
            port = value[2]
            obj = data.Operation_db()
            obj.add_host(host,ip,port)


    def write(self,location,content):
        f = xlwt.Workbook()
        sheet1 = f.add_sheet('hosts')
        sheet1.col(0).width = 6666
        sheet1.col(1).width = 6666
        title = ['主机', 'IP', '端口']
        for i in range(0, len(title)):
            sheet1.write(0, i, title[i])
        for index,key in enumerate(content.keys()):
            row0=[]
            row = content[key]
            value1 = row['IP']
            value2 = row['端口']
            row0.append(key)
            row0.append(value1)
            row0.append(value2)
            title = ['主机','IP','端口']

            for i in range(0, len(row0)):
                sheet1.write(index+1, i, row0[i])
        f.save('%s%s.xls' %(location,time.strftime('%Y-%m-%d')))
        print('导出成功')



    def add(self):
        while True:
            self.user_obj = data.Operation_db()
            self.username_dic = self.user_obj.check_host_data()
            # host = input('输入主机名(q退出):').strip()
            # if host in self.username_dic.keys():
            #     print('主机名已存在')
            #     break
            # if host == 'q':break
            # ip = input('输入ip:').strip()
            # port = input('输入端口:').strip()
            location = input('excel表路径(q退出):').strip()
            if location == 'q':break
            if len(location) == 0:continue
            if os.path.isfile(location):
                self.read('%s'%location)
            else:
                print('文件不存在')
                continue


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

