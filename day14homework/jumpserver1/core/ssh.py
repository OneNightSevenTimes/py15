# import paramiko
# import sys
# import os
# import socket
# import select
# import getpass
# import termios
# import tty
# from paramiko.py3compat import u
#
#
# def connect(ip, username,password):
#     tran = paramiko.Transport((ip, 22,))
#     tran.start_client()
#     tran.auth_password(username, password)
#
#     # 打开一个通道
#     chan = tran.open_session()
#     # 获取一个终端
#     chan.get_pty()
#     # 激活器
#     chan.invoke_shell()
#
#     # 获取原tty属性
#     oldtty = termios.tcgetattr(sys.stdin)
#     try:
#         # 为tty设置新属性
#         # 默认当前tty设备属性：
#         # 输入一行回车，执行
#         # CTRL+C 进程退出，遇到特殊字符，特殊处理。
#
#         # 这是为原始模式，不认识所有特殊符号
#         # 放置特殊字符应用在当前终端，如此设置，将所有的用户输入均发送到远程服务器
#         tty.setraw(sys.stdin.fileno())
#         tty.setcbreak(sys.stdin.fileno())
#         chan.settimeout(0.0)
#
#         log = open('handle.log', 'a+', encoding='utf-8')
#         flag = False
#         temp_list = []
#
#         while True:
#             r, w, e = select.select([chan, sys.stdin], [], [])
#             if chan in r:
#                 try:
#                     x = u(chan.recv(1024))
#                     if len(x) == 0:
#                         sys.stdout.write('\r\n*** EOF\r\n')
#                         break
#                     # 如果用户上一次点击的是tab键，则获取返回的内容写入在记录中
#                     if flag:
#                         if x.startswith('\r\n'):
#                             pass
#                         else:
#                             temp_list.append(x)
#                         flag = False
#                     sys.stdout.write(x)
#                     sys.stdout.flush()
#                 except socket.timeout:
#                     pass
#             if sys.stdin in r:
#                 # 读取用户在终端数据每一个字符
#                 x = sys.stdin.read(1)
#                 if len(x) == 0:
#                     break
#                 # 如果用户点击TAB键
#                 if x == '\t':
#                     flag = True
#                 else:
#                     # 未点击TAB键，则将每个操作字符记录添加到列表中，以便之后写入文件
#                     temp_list.append(x)
#
#                 # 如果用户敲回车，则将操作记录写入文件
#                 if x == '\r':
#                     log.write(''.join(temp_list))
#                     log.flush()
#                     temp_list.clear()
#                 chan.send(x)
#
#     finally:
#         # 重新设置终端属性
#         termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)
#
#     chan.close()
#     tran.close()
import os
import sys
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

path=os.path.join(base_dir,'dsdsd','ds')
print(path)
# file = open('log\handle.log','a+',encoding='utf-8')
# file.write('dsadasd')
