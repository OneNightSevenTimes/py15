import pymysql
from conf import settings
class Get_history_data(object):
    def __init__(self,host,port,user,passwd,db):
        self.conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
        self.cursor = self.conn.cursor()

    def get_itemid(self,item,file_item):
        sql = "select hosts.host,itemid from items left join hosts on items.hostid=hosts.hostid where items.key_=%s"
        params = item
        reCount = self.cursor.execute(sql, params)
        row = self.cursor.fetchall()
        f = open(file_item,'a+',encoding='utf-8')
        for i in row:
            f.write(str(i[0])+' '*8+str(i[1])+'\n')
        # self.conn.commit()
        # self.cursor.close()
        # self.conn.close()
    def get_data(self,file_item,file_data,clock_from_ago,clock_end_ago,clock_from,clock_end):
        f = open(file_item, 'r', encoding='utf-8')
        f2 = open(file_data, 'a+', encoding='utf-8')

        for line in f:
            all=line.split(' ')
            host=all[0]
            item = all[8]
            sql = "select max(round(value,4))as MAX from history where itemid=%s and clock>%s and clock<%s"
            params=(item,clock_from_ago,clock_end_ago)
            reCount = self.cursor.execute(sql, params)
            row = self.cursor.fetchone()

            sql2 = "select max(round(value,4)) from history where itemid=%s and clock>%s and clock<%s"
            params=(item,clock_from,clock_end)
            reCount2 = self.cursor.execute(sql2, params)
            row2 = self.cursor.fetchone()
            info=str(host)+' '*8+str(row[0])+' '*8+str(row2[0])+'\n'
            print(info)
            f2.write(info)
        self.conn.commit()
        self.cursor.close()
        self.conn.close()