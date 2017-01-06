from db import data

class type(object):
    def __init__(self):
        '''获取user,password,type'''
        self.user_obj = data.Operation_db()
        self.username_dic = self.user_obj.check_data()

    def run(self):
        while True:
            self.user_obj = data.Operation_db()
            dic = self.user_obj.check_data()
            print(dic)
            change_user = input('输入需要修改类型的用户(q退出):').strip()
            if change_user in self.username_dic.keys():
                change_type = input('输入需要之后的类型：').strip()
            elif change_user == 'q':
                break
            else:
                print('修改用户不存在')
                break
            status = self.user_obj.change_type(change_user, change_type)
            if status:
                print('修改成功')