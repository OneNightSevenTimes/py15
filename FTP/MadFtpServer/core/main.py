
import optparse
from core.ftp_server import FTPHandler
import socketserver
from conf import settings


class ArvgHandler(object):
    def __init__(self):
        self.parser = optparse.OptionParser()
        # parser.add_option("-s","--host",dest="host",help="server binding host address")
        # parser.add_option("-p","--port",dest="port",help="server binding port")
        (options, args) = self.parser.parse_args()
        #options.host
        if not args:
            exit('usage:python3 ftp_server.py start')
        self.verify_args(options, args)

    def verify_args(self,options,args):
        '''校验并调用相应的功能'''
        if hasattr(self,args[0]):
            func = getattr(self,args[0])
            func()
        else:
            self.parser.print_help()

    def start(self):
        print('---going to start server----')
        # Create the server, binding to localhost on port 9999
        server = socketserver.ThreadingTCPServer((settings.HOST, settings.PORT), FTPHandler)
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()




