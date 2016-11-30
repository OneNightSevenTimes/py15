import sys
import os
import json
basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def user_judge(user_id):
    db = '%s/db/accounts/%s.json' %(basedir,'user%s'%user_id)
    #print(db)
    count = 0
    if os.path.isfile(db):
        return True
    else:
        return False
