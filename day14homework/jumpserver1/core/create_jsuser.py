import paramiko
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from db import module
from core import main
def create_jumpserver_user():
    while True:
        username = input('请输入超级管理员用户：').strip()
        if len(username) == 0:continue
        password = input('请输入密码：').strip()
        if len(password) == 0:continue
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname='192.168.147.147', port=22, username=username, password=password)
            while True:
                register_name = input('创建用户名（q退出）：').strip()
                if register_name == 'q':exit()
                if not module.user_exist(register_name):#判断用户是否已经存在

                    register_password = input('密码：').strip()
                    #在堡垒机上创建用户、密码、改.bashrc
                    stdin, stdout, stderr = ssh.exec_command('useradd %s'%register_name)
                    command = 'echo %s | passwd --stdin %s'%(register_password,register_name)
                    stdin, stdout, stderr = ssh.exec_command('%s'%command)
                    stdin, stdout, stderr = ssh.exec_command('echo /usr/bin/python3 /data/jumpserver1/bin/start.py >> /home/%s/.bashrc'%register_name)
                    stdin, stdout, stderr = ssh.exec_command('echo exit >> /home/%s/.bashrc'%register_name)
                    #写入数据库堡垒机用户表中
                    module.register(register_name,register_password)
                else:
                    print('用户存在了')


            result = stderr.read()
            print(result.decode())
            ssh.close()
        except paramiko.ssh_exception.AuthenticationException as e:
            print('认证失败')
if __name__=="__main__":
    create_jumpserver_user()