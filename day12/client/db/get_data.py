import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)
import pymysql
from conf import setting

def info(host_ip):
    info = {}
    print(host_ip)
    for ip in host_ip:
        conn = pymysql.connect(host=setting.db_ip,port=setting.db_port,user=setting.db_user,\
                               password=setting.db_password,db=setting.db_name)
        cursor = conn.cursor()

        sql = "select hosts.hid,hosts.hname,hosts.hostip,groups.gname,\
        hosts.user,hosts.password from hosts left join groups on hosts.group_id=groups.gid \
        where hostip=%s "
        params = (ip)
        reCount = cursor.execute(sql,params)
        data = cursor.fetchall()
        print(data)
        #info[data[0][1]]['ip']=data[0][2]
        info[data[0][1]] = {'ip':data[0][2],'user':data[0][4],'password':data[0][5]}

        conn.commit()
        cursor.close()
        conn.close()
    return info