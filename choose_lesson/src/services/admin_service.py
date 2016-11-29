from src.models import Admin
from src.models import School
from src.models import Teacher
from src.models import Course
def create_school():
    try:
        name = input('请输入学校名：').strip()
        addr = input('请输入学校地址：').strip()
        school_name_list = [(obj.name,obj.addr) for obj in School.get_all_obj_list()]
        if (name,addr) in school_name_list:
            raise Exception('\033[43;1m[%s] [%s]校区已存在，不可重复创建\033[0m'%(name,addr))
        obj = School(name,addr)
        obj.save()
        status = True
        error = ''
        data='\033[33;1m[%s] [%s]校区 创建成功\033[0m' %(obj.name,obj.addr)
    except Exception as e:
        status=False
        error=str(e)
        data=''
    return {'status':status,'error':error,'data':data}

def show_school():
    for obj in School.get_all_obj_list():
        print('\033[45;1m学校[%s] 地址[%s] 创建日期[%s]\033[0m'.center(60,'-') \
              %(obj.name,obj.addr,obj.create_time))
def create_teacher():
    try:
        name=input('请输入老师姓名: ').strip()
        level=input('请输入老师级别: ').strip()
        teacher_name_list=[obj.name for obj in Teacher.get_all_obj_list()]
        if name in teacher_name_list:
            raise Exception('\033[43;1m老师[%s] 已经存在,不可重复创建\033[0m' %(name))
        obj=Teacher(name,level)
        obj.save()
        status=True
        error=''
        data='\033[33;1m老师[%s] 级别[%s] 时间[%s]创建成功\033[0m' %(obj.name,obj.level,obj.create_time)
    except Exception as e:
        status=False
        error=str(e)
        data=''
    return {'status':status,'error':error,'data':data}


def show_teacher():
    for obj in Teacher.get_all_obj_list():
        print('\033[33;1m老师[%s] 级别[%s] 创建时间[%s]\033[0m'.center(60,'-') \
              %(obj.name,obj.level,obj.create_time))


def create_course():
    try:
        print('创建课程'.center(60,'='))
        school_list=School.get_all_obj_list()
        for k,obj in enumerate(school_list):
            print(k,obj,obj.addr)
        sid=int(input('请选择学校: '))
        school_obj=school_list[sid]

        name=input('请输入课程名: ').strip()
        price=input('请输入课程价格: ').strip()
        period=input('请输入课程周期: ').strip()

        course_name_list=[(obj.name,obj.school_nid.uuid) for obj in Course.get_all_obj_list()]
        if (name,school_obj.nid.uuid) in course_name_list:
            raise Exception('\033[43;1m课程[%s] 已经存在,不可重复创建\033[0m' %(name))
        obj=Course(name,price,period,school_obj.nid)
        obj.save()
        status=True
        error=''
        data='\033[33;1m课程[%s] 价格[%s] 周期[%s]创建成功\033[0m' %(obj.name,obj.price,obj.period)
    except Exception as e:
        status=False
        error=str(e)
        data=''
    return {'status':status,'error':error,'data':data}

def show_course():
    for obj in Course.get_all_obj_list():
        print('\033[33;1m[%s] [%s]校区 [%s]课程 价格[%s] 周期[%s]\033[0m'.center(60,'-') \
              %(obj.school_nid.get_obj_by_uuid().name,obj.school_nid.get_obj_by_uuid().addr,\
                obj.name,obj.price,obj.period))

def create_course_to_teacher():
    pass

def create_classes():
    pass

def show_classes():
    pass

def create_student():
    pass

def show_student():
    pass



def show():
    msg='''
        0:选项
        1:创建学校
        2:查看学校
        3:创建老师
        4:查看老师
        5:创建课程
        6:查看课程
        7:关联老师与课程
        8:创建班级
        9:查看班级
        10:创建学生
        11:查看学生
        12:退出
    '''
    print(msg)


def main():
    choice_dic={
        '0':show,
        '1':create_school,
        '2':show_school,
        '3':create_teacher,
        '4':show_teacher,
        '5':create_course,
        '6':show_course,
        '7':create_course_to_teacher,
        '8':create_classes,
        '9':show_classes,
        '10':create_student,
        '11':show_student,
        '12':exit
    }
    show()
    while True:
        choice=input('请输入选项: ').strip()
        if choice not in choice_dic:continue
        ret=choice_dic[choice]()
        if ret:
            if ret['status']:
                print(ret['data'].center(60,'-'))
            else:
                print(ret['error'].center(60,'-'))


def login():
    ret=Admin.login()
    if ret:
            if ret['status']:
                print(ret['data'].center(60,'-'))
                main()
            else:
                print(ret['error'].center(60,'-'))

if __name__ == '__main__':
    main()



