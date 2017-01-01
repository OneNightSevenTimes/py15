import pika
import uuid


class SSHRpcClient(object):
    def __init__(self):
        credentials = pika.PlainCredentials('testuser', 'testuser')
        self.connection = pika.BlockingConnection(pika.ConnectionParameters
                                             (host='192.168.147.147', credentials=credentials))


        self.channel = self.connection.channel()
        #生成一个随机队列，接收端退出时，销毁临时产生的队列，这样就不会占用资源
        result = self.channel.queue_declare(exclusive=True) # 客户端的结果必须要返回到这个queue
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response,queue=self.callback_queue) #声明从这个queue里收结果,只有当下面channel.start_consuming时才
        #调用on_response函数

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id: #任务标识符
            self.response = body
            #print(body)
    def get_response(self,queue_name,uuid):
        self.uuid = uuid
        self.response = None
        self.channel.basic_consume(self.on_response,  # 只要收到消息就执行on_response
                                   queue=queue_name)
        while self.response is None:
            self.connection.process_data_events()  # 非阻塞版的start_consuming
        return self.response
    def call(self,n):
        self.response = None
        self.corr_id = str(uuid.uuid4()) #唯一标识符

        self.channel.basic_publish(exchange='',
                                   routing_key='rpc_queue6',#exchange，服务端没申明queue，客户端没启动的话，第一次发的消息就没啦
                                   properties=pika.BasicProperties(
                                       reply_to=self.callback_queue,#随机queue
                                       correlation_id=self.corr_id,#唯一标识符
                                   ),

                                   body=str(n))

        #
        # print("start waiting for cmd result ")
        # #self.channel.start_consuming()
        # count = 0
        # while self.response is None: #如果命令没返回结果
        #     #print("loop ",count)
        #     #count +=1
        #     self.connection.process_data_events() #以不阻塞的形式去检测有没有新事件
        #     #如果没事件，那就什么也不做， 如果有事件，就触发on_response事件

        return self.callback_queue,self.corr_id


# ssh_rpc = SSHRpcClient()
#
# print(" [x] sending cmd")
# response = ssh_rpc.call("ls")
#
#
# print(" [.] Got result ")
# print(response.decode("gbk"))