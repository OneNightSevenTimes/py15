from db import data
class auth(object):
    def __init__(self):
        '''获取user,password,type'''
        user_obj = data.Operation_db()
        self.username_dic = user_obj.check_data()

    def main(self):
        while True:
            user = input('用户名：').strip()
            if len(user) == 0: continue
            if user in self.username_dic.keys():
                while True:
                    pwd = input('请输入密码:').strip()
                    if len(pwd) == 0: continue
                    if pwd == self.username_dic[user]['password']:
                        print('login in')
                        return True
            else:
                print('用户不存在')