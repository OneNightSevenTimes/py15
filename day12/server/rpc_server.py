import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from conf import setting
import pika
import subprocess
import paramiko
class Rpc_server(object):
    def __init__(self,user,password,host_ip):
        credentials = pika.PlainCredentials(user,password)
        connection = pika.BlockingConnection(pika.ConnectionParameters
                                         (host=host_ip,credentials=credentials))
        self.channel = connection.channel()
        self.channel.queue_declare(queue='rpc_queue6')

    # def SSHRPCServer(self,cmd):
    #     print("recv cmd:",cmd)
    #     cmd_obj = subprocess.Popen(cmd.decode(),shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    #
    #     result = cmd_obj.stdout.read() or cmd_obj.stderr.read()
    #     return result
    def SSHRPCServer(self,body):
        #info = {'ip':'192.168.147.147','port':22,'user':'root','password':'centos'}
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())


        print(body)
        total = eval(body)
        command = total['cmd']
        total.pop('cmd')
        for key in total:
            info = total[key]


            print(" [.] fib(%s)" % body)

            ssh.connect(hostname='%s'%info['ip'], port=22,\
                        username='%s'%info['user'], password='%s'%info['password'])
            stdin, stdout, stderr = ssh.exec_command(command)
            result = stdout.read()
            hostname = info['ip']
        #print(hostname.center(50,'-'))
        #print(result.decode())
        #ssh.close()
            return result

    def on_request(self,ch, method, props,body):
        response = self.SSHRPCServer(body)

        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(correlation_id= \
                                                             props.correlation_id),
                         body=response)
Server = Rpc_server(setting.user,setting.password,setting.mq_ip)

Server.channel.basic_consume(Server.on_request, queue='rpc_queue6')
print(" [x] Awaiting RPC requests")
Server.channel.start_consuming()