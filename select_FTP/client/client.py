
import socket
import os,sys
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class selectFtpClient:
    def __init__(self):
        self.args=sys.argv
        if len(self.args)>1:
            self.port=(self.args[1],int(self.args[2]))
        else:
            self.port=("127.0.0.1",8885)
        self.create_socket()
        self.command_fanout()

    def create_socket(self):
        try:
            self.sk = socket.socket()
            self.sk.connect(self.port)
            print('连接FTP服务器成功!')
        except Exception as e:
            print("error: ",e)

    def command_fanout(self):
        while True:
            cmd = input('>>>').strip()
            if cmd == 'exit()':
                break
            cmd,file = cmd.split()
            if hasattr(self, cmd):
                func = getattr(self, cmd)
                func(cmd,file)
            else:
                print('调用错误!')

    def put(self,cmd,file):

        if os.path.isfile(file):
            fileName= os.path.basename(file)
            fileSize = os.path.getsize(file)
            fileInfo ='%s|%s|%s'%(cmd,fileName,fileSize)
            self.sk.send(bytes(fileInfo, encoding='utf8'))
            recvStatus = self.sk.recv(1024)
            print('recvStatus', recvStatus)
            hasSend = 0
            if str(recvStatus, encoding='utf8') == "OK":
                with open(file, 'rb') as f:
                    while fileSize > hasSend :
                        contant = f.read(1024)
                        recv_size = len(contant)
                        self.sk.send(contant)
                        hasSend += recv_size
                        s=str(int(hasSend/fileSize*100))+"%"
                        print("正在上传文件："+fileName+"   已经上传："+s)
                print('%s文件上传完毕' % (fileName,))
        else:
            print('文件不存在')

    def get(self, cmd,file):
        info = '%s|%s|%s'%(cmd,file,'0')
        self.sk.send(bytes(info, encoding='utf8'))

        fileInfo = self.sk.recv(1024)
        print(fileInfo.decode("utf8"))
        fileStatus, fileSize = str(fileInfo, encoding='utf8').split('|')
        fileSize=int(fileSize)
        print('file_status: ', fileStatus, fileSize)
        if fileStatus == 'YES':
            #******------注意:下面这句与server的一发一收是必须有的,否则没有办法再次激活server的read方法-----******
            self.sk.send(bytes("second_active", encoding='utf8'))
            path = os.path.join(BASE_DIR,file)
            hasReceived = 0
            with open(path, 'wb') as f_write:
                while hasReceived < int(fileSize):
                    data = self.sk.recv(1024)
                    print("data:",data)
                    hasReceived += len(data)
                    f_write.write(data)
                    s=str(hasReceived/fileSize*100)+"%"
                    print("正在下载文件："+file+"已经下载："+s)
                print('file %s 下载完成!' % file)
        else:
            print("文件不存在!")

if __name__ == '__main__':

    selectFtpClient()

