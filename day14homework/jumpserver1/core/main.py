from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine
from conf import settings
from db import module

engine = create_engine(settings.conn)
Session = sessionmaker(bind=engine)
session = Session()

def register():
    while True:
        user = input('username:').strip()
        if len(user) == 0:continue
        users = session.query(module.UserProfile).filter(module.UserProfile.username==user).first()
        if users:
            print('用户存在')
            continue
        else:
            password = input('password:').strip()
            if len(password) == 0:continue
            module.register(user,password)
            print('注册成功')

def auth():
    while True:
        username = input('堡垒机用户名：').strip()
        if len(username) == 0:continue
        password = input('密码：').strip()
        if len(password) == 0:continue
        user_info = module.login(username,password)
        if user_info:
            print('login')

        else:
            print('wrong username or password')
        return user_info
def host_owner():


    pass