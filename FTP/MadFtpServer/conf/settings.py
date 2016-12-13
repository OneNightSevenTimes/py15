
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_CLIENT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

USER_HOME = "%s/home" % BASE_DIR
USER_CLIENT_HOME = '%s/MadFtpClient/db'%BASE_CLIENT_DIR
LOG_DIR =  "%s/log" % BASE_DIR
LOG_LEVEL = "DEBUG"

ACCOUNT_FILE = "%s/conf/accounts.cfg" % BASE_DIR


HOST = "0.0.0.0"
PORT = 8888


