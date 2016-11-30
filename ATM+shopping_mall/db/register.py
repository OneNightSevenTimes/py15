#注册调用接口
import json
import os
basedir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def username(user_id,pwd,cre,bal,status = False):
    user_info = {
        'user_id':user_id,
        'password':pwd,
        'credit': cre,
        'balance':bal,
        'locked':status
    }
    user_info['limit'] = user_info['credit']

    with open('%s/db/accounts/user%s.json'%(basedir,user_info['user_id']),'w')as f:
        #json.dump(user_id,f)
        f.write(json.dumps(user_info))
        #两种方法都能字典转换成json格式
def load(user_id):
    with open('%s/db/accounts/user%s.json'%(basedir,user_id),'r') as f:
        data = json.load(f)
    return data
def dump(user_id,data):
    with open('%s/db/accounts/user%s.json'%(basedir,user_id),'w') as f:
        json.dump(data,f)