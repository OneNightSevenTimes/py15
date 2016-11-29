import os,sys
from src.services import admin_service
from src.services import teacher_service
from src.services import student_service
from src.services import initialize_service
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)




def show_role():
    msg='''
    0:初始化
    1:管理员
    2:老师
    3:学生
    '''
    print(msg)

if __name__ == '__main__':
    role_main={
        '0':initialize_service.main,
        '1':admin_service.login,
        '2':teacher_service.login,
        '3':student_service.login,
    }
    while True:
        show_role()
        choice=input('输入角色: ').strip()
        if choice not in role_main:continue
        role_main[choice]()