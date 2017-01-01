import threading
import optparse
import os
import sys
import random
import time
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
from db import get_data
from core import rpc_client
class Choose(object):
    def __init__(self):
        self.info = {}
    def check_task(self,user_input):
        task_id = user_input.split()[1]
        task_id = int(task_id)
        uuid = self.info[task_id][3]
        queue_name = self.info[task_id][2]
        client = rpc_client.SSHRpcClient()
        response = client.get_response(queue_name,uuid)
        print(response.decode())
    def check_all(self,*args):
        for key in self.info:
            print('task_id:[%s] ip:[%s] cmd:[%s]'%(key,self.info[key][0],self.info[key][1]))

    def run_task(self,user_input):
        host_all = []
        command = user_input.split()[4]
        if user_input.split()[1]=='-h':
            host = user_input.split()[2].split(',')
            for i in host:
                host_all.append(i)
            #print(host_all)
        #if user_input.split()[1]=='-g':
            info = get_data.info(host_all)
            info['cmd'] = command
            for host in host_all:
                task_id = random.randint(10000, 99999)
                client = rpc_client.SSHRpcClient()
                response = client.call(info)#response存放的是queue_name,uuid,用来根据task_id取结果
                #print(response.decode("gbk"))
                self.info[task_id] = [host,command,response[0],response[1]]



    def handle(self,str,user_input):
        getattr(self,str)(user_input)
    def start(self):
        while True:
            time.sleep(1)
            user_input = input('please input:').strip()

            cmd = user_input.split()[0]
            if not cmd:continue

            t = threading.Thread(target=self.handle,args=(cmd,user_input))
            t.start()

c = Choose()
c.start()
