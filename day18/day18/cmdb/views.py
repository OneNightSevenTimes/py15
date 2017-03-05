from django.shortcuts import render
from django.shortcuts import redirect
import pymysql
# Create your views here.
def mysql(sql):
    conn = pymysql.connect(host='192.168.147.147',port=3306,user='root',passwd='centos',db='day18')
    cursor = conn.cursor()
    cursor.execute(sql)
    result=cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return result


def index(request):
    if request.method == 'GET':
        result = mysql('select * from host')
        DB = []
        for i in result:
            temp = {'hostname':i[1],'port':i[2],'host_ip':i[3]}
            DB.append(temp)
        return render(request, 'index.html', {'data':DB})
    if request.method == 'POST':
        h = request.POST.get('host')
        i = request.POST.get('host_ip')
        p = request.POST.get('port')
        sql = "insert into host (hostname,port,host_ip) values ('%s',%s,'%s')"%(h,p,i)
        mysql(sql)
        # return render(request,'index_bak.html')
        result = mysql('select * from host')
        DB = []
        for i in result:
            temp = {'hostname': i[1], 'host_ip': i[3], 'port': i[2]}
            DB.append(temp)

        return render(request, 'index.html', {'data': DB})
def login(request):
    if request.method == 'GET':
        return render(request,'login.html')
    elif request.method == 'POST':
        #获取用户提交的数据
        Username = request.POST.get('user')
        password = request.POST.get('pwd')
        sql = "select password from user where username='%s'"%Username
        info = mysql(sql)
        if info:
            if password == info[0][0]:
                return redirect('/index/')
            else:
                return render(request, 'login.html')
        else:
            return render(request, 'login.html')
def delete(request):
    if request.method == 'GET':
        hostname = request.GET.get('h')
        sql = "delete from host where hostname='%s'"%hostname
        mysql(sql)
        return redirect('/index/')

