import optparse
import paramiko
import configparser
from multiprocessing import Pool,Lock,Process
import sys
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
class Remote_control(object):
    def __init__(self):
        parser = optparse.OptionParser()

        parser.add_option('-s', '--server', dest='host', help='the ip you want to ssh')
        parser.add_option('-g', '--group', dest='group', help='the group you want to ssh')
        parser.add_option('-c', '--command', dest='command', help='the command you want to dis')
        parser.add_option('-a', '--action', dest='action', help='the action you want to do')

        self.options, self.args = parser.parse_args()
        # print(self.options,self.args)
        if self.verify_args(self.options, self.args):
            #去数据库中获取用户用户名、密码等信息
            info = self.get_info(self.options,self.args)
            #if hasattr(self,'%s'%self.options.command):#这里options不是字典，只能通过这种方式取值

                #func = getattr(self,'_%s'%self.options.command)
                #func(info)
            if self.options.command:
                command = self.options.command
                type = 'cmd'
            else:
                command = self.options.action
                type = 'action'
            self.make_process(info,command,type)


    def verify_args(self,options,args):
        '''check argv user input'''
        if options.host is None and options.group is None:
            exit('Err:host or group should be choosen')
        if options.command is None and options.action is None:
            exit('Err:command or action should be choosen')
        return True

    def get_info(self,options,args):
        '''get information from db'''
        config = configparser.ConfigParser()
        config.read('%s/db/info.ini'%BASE_DIR)
        host_all = []
        if options.host:
            host = options.host.split(',')
            for i in host:
                host_all.append(i)
        if options.group:#如果用户输入组存在
            host_group = options.group.split(',')#用户输入的所有组
            for host in config.sections():
                if config[host]['group'] in host_group:
                    host_all.append(host)
        host_only = set(host_all)#唯一的主机名
        info_dic = {}
        for host in host_only:
            ip = config[host]['ip']
            user = config[host]['user']
            password = config[host]['password']
            port = config[host]['port']

            info_dic[host]={'ip':ip,'user':user,'password':password,'port':port}
        return info_dic

    def cmd(self,info,command):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname='%s'%info['ip'], port=int(info['port']),\
                    username='%s'%info['user'], password='%s'%info['password'])
        stdin, stdout, stderr = ssh.exec_command(command)
        result = stdout.read()
        hostname = info['ip']
        print(hostname.center(50,'-'))
        print(result.decode())
        ssh.close()

    def action(self,info,command):
        print(command)
        transport = paramiko.Transport((info['ip'], int(info['port'])))
        transport.connect(username=info['user'], password=info['password'])
        sftp = paramiko.SFTPClient.from_transport(transport)
        file = command.split(' ')
        sftp.put('%s/db/%s'%(BASE_DIR,file[1]),file[2])

    def make_process(self,info,command,type):
        lock = Lock()#进程共享屏幕
        pool = Pool(processes=4)

        for i in info.keys():
            if type == 'cmd':
                pool.apply_async(func=self.cmd, args=(info['%s'%i],command))
            if type == 'action':
                pool.apply_async(func=self.action, args=(info['%s'%i],command))



        pool.close()
        pool.join()


if __name__ == '__main__':
    c = Remote_control()