import sys
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from core import main
from conf import settings

if __name__ == '__main__':
    obj = main.Get_history_data(settings.host,settings.port,settings.user,
                 settings.passwd,settings.db)
    obj.get_itemid(settings.item,settings.file_item)
    obj.get_data(settings.file_item,settings.file_result,
                 settings.clock_from_ago,settings.clock_end_ago,
                 settings.clock_from,settings.clock_end)

