import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from core import rpc_client
from core import main
if __name__ == "__main":
    c = main.Choose()
    c.start()
