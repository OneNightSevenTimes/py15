import socketserver
import configparser
from conf import settings
import os
import hashlib

STATUS_CODE  = {
    250 : "Invalid cmd format, e.g: {'action':'get','filename':'test.cfg.py','size':344}",
    251 : "Invalid cmd ",
    252 : "Invalid auth data",
    253 : "Wrong username or password",
    254 : "Passed authentication",
    255 : "Filename doesn't provided",
    256 : "File doesn't exist on server",
    257 : "ready to send file",
    258 : "md5 verification",
    259 : "file exist on server",
    260 : "continue transfer",
    261 : "change dir success",
    262 : "dir is not exist",
    263 : "show dir",

}

import json
class FTPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        while True:
            self.data = self.request.recv(1024).strip()
            print(self.client_address[0])
            print(self.data)
           # self.request.send(b'1')
            if not self.data:
                print("client closed...")
                break
            data  = json.loads(self.data.decode())
            if data.get('action') is not None:
                print("---->",hasattr(self,"_auth"))


                if hasattr(self,"_%s"%data.get('action')):
                    func = getattr(self,"_%s"% data.get('action'))
                    func(data)
                else:
                    print("invalid cmd")
                    self.send_response(251)
            else:
                print("invalid cmd format")
                self.send_response(250)

    def send_response(self,status_code,data=None):
        '''向客户端返回数据'''
        response = {'status_code':status_code,'status_msg':STATUS_CODE[status_code]}
        if data:
            response.update( data  )
        self.request.send(json.dumps(response).encode())

    def _auth(self,*args,**kwargs):
        data = args[0]
        if data.get("username") is None or data.get("password") is None:
            self.send_response(252)

        user =self.authenticate(data.get("username"),data.get("password"))
        if user is None:
            self.send_response(253)
        else:
            print("passed authentication",user)
            self.user = user
            self.send_response(254)
    def authenticate(self,username,password):
        '''验证用户合法性，合法就返回用户数据'''

        config = configparser.ConfigParser()
        config.read(settings.ACCOUNT_FILE)
        if username in config.sections():
            _password = config[username]["Password"]
            if _password == password:
                print("pass auth..",username)
                config[username]["Username"] = username
                return config[username]

    def _put(self,*args,**kwargs):
        "client send file to server"
        data = args[0]
        print(data)
        user_home_dir = "%s/%s" %(settings.USER_HOME,self.user["Username"])
        file_abs_path = "%s/%s" %(user_home_dir,data.get('filename'))

        print(file_abs_path)
        if os.path.isfile(file_abs_path):#断点续传
            #判断server文件大小是否和client文件大小一致 seek
            file_exist_size = os.path.getsize(file_abs_path)
            file_total_size = data.get('filesize')
            print(file_exist_size,file_total_size)
            if file_exist_size == file_total_size:
                #self.request.recv(1)
                print('file exist')
                self.send_response(259)
            else:
                self.send_response(260)
                self.request.recv(1)
                self.request.send(str(file_exist_size).encode())
                file_obj = open(file_abs_path, 'ab')
                received_size = file_exist_size
                while received_size < file_total_size:
                    data = self.request.recv(4096)
                    file_obj.write(data)
                    received_size += len(data)
                file_obj.close()

        else:
            self.send_response(257)
            file_obj = open(file_abs_path,'wb')
            total_size = data.get('filesize')
            received_size = 0
            while received_size < total_size:
                data = self.request.recv(4096)
                file_obj.write(data)
                received_size += len(data)
            file_obj.close()


    def _get(self,*args,**kwargs):
        data = args[0]
        if data.get('filename') is None:
            self.send_response(255)
        user_home_dir = "%s/%s" %(settings.USER_HOME,self.user["Username"])
        file_abs_path = "%s/%s" %(user_home_dir,data.get('filename'))
        print("file abs path",file_abs_path)

        if os.path.isfile(file_abs_path):
            file_obj = open(file_abs_path,"rb")
            file_size = os.path.getsize(file_abs_path)
            self.send_response(257,data={'file_size':file_size})
            self.request.recv(1) #等待客户端确认

            if data.get('md5'):
                md5_obj = hashlib.md5()
                for line in file_obj:
                    self.request.send(line)
                    md5_obj.update(line)
                else:
                    file_obj.close()
                    md5_val = md5_obj.hexdigest()
                    self.send_response(258,{'md5':md5_val})
                    print("send file done....")
            else:
                for line in file_obj:
                    self.request.send(line)
                else:
                    file_obj.close()
                    print("send file done....")
        else:
            self.send_response(256)


    def _ls(self,*args,**kwargs):
        data = args[0]
        cmd_list = data.get('cmd_list')
        if len(cmd_list) > 1:
            dir_name = cmd_list[1]
        if len(cmd_list) == 1:
            dir_name = '%s/%s'%(settings.USER_HOME,data.get('username'))
            print(dir_name)
        contact = os.popen('dir %s'%dir_name)
        contact_tra = contact.read()
        self.send_response(261,{'contact':contact_tra})



    def _cd(self, *args, **kwargs):
        data = args[0]
        cmd_list = data.get('cmd_list')
        dir_name = cmd_list[1]
        user_home_path = '%s/%s'%(settings.USER_HOME,self.user["Username"])#用户家目录
        change_path = '%s/%s'%(user_home_path,dir_name)
        if os.path.isdir(change_path):
            self.send_response(261,{'file_path':change_path})
        else:
            self.send_response(262)





if __name__ == "__main__":
    HOST, PORT = "localhost", 9000
