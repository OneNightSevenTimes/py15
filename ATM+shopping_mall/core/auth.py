import sys
import os
import json
basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def get_info(user_id,password):
    '''
    get information of user from db
    :param user_id:
    :param password:
    :return:
    '''
    db = '%s/db/accounts/user%s.json' %(basedir,user_id)
    #print(db)
    count = 0
    if os.path.isfile(db):
        with open(db,'r')as f:
            data = json.load(f)
        balance = data['balance']
        correct_pwd = data['password']
        loc = data['locked']
        #auth_login(password,correct_pwd)
        if not loc:
            while count < 3:
                if data['password'] == password:
                    return True
                else:
                    password = input('try it again').strip()
                    count+=1
                    if count == 2 and password!=data['password']:
                        print('\033[31;1mtry too much times\033[0m')
                        data['locked'] = 'True'
                        with open(db, 'w')as f:
                            json.dump(data,f)
                        break
        else:
            print('\033[31;1myour account has been locked\033[0m')
    else:
        print('\033[31;1mthe user_id is not exist,you should register\033[0m')