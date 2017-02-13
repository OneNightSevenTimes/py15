from sqlalchemy import create_engine, and_, or_, func, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, DateTime
from sqlalchemy.orm import sessionmaker, relationship
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from conf import settings
Base = declarative_base()  # 生成一个SqlORM 基类


class Host(Base):
    __tablename__ = 'host'
    id = Column(Integer, primary_key=True, autoincrement=True)
    hostname = Column(String(64), unique=True, nullable=False)
    ip_addr = Column(String(128), unique=True, nullable=False)
    port = Column(Integer, default=22)


class HostUser(Base):
    __tablename__ = 'host_user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(64), unique=True, nullable=False)
    AuthTypes = [
        ('p', 'SSH/Password'),
        ('r', 'SSH/KEY'),
    ]
    auth_type = Column(String(16))
    cert = Column(String(255))

    host_id = Column(Integer, ForeignKey('host.id'))

    __table_args__ = (
        UniqueConstraint('host_id', 'username', name='_host_username_uc'),
    )


class Group(Base):
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), unique=True, nullable=False)


class UserProfile(Base):
    __tablename__ = 'user_profile'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(64), unique=True, nullable=False)
    password = Column(String(255), nullable=False)


class Group2UserProfile(Base):
    __tablename__ = 'group_2_user_profile'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_profile_id = Column(Integer, ForeignKey('user_profile.id'))
    group_id = Column(Integer, ForeignKey('group.id'))
    __table_args__ = (
        UniqueConstraint('user_profile_id', 'group_id', name='ux_user_group'),
    )


class Group2HostUser(Base):
    __tablename__ = 'group_2_host_user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    host_user_id = Column(Integer, ForeignKey('host_user.id'))
    group_id = Column(Integer, ForeignKey('group.id'))
    __table_args__ = (
        UniqueConstraint('group_id', 'host_user_id', name='ux_group_host_user'),
    )


class UserProfile2HostUser(Base):
    __tablename__ = 'user_profile_2_host_user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    host_user_id = Column(Integer, ForeignKey('host_user.id'))
    user_profile_id = Column(Integer, ForeignKey('user_profile.id'))
    __table_args__ = (
        UniqueConstraint('user_profile_id', 'host_user_id', name='ux_user_host_user'),
    )


class AuditLog(Base):
    __tablename__ = 'audit_log'
    id = Column(Integer, primary_key=True, autoincrement=True)

    action_choices2 = [
        (u'cmd', u'CMD'),
        (u'login', u'Login'),
        (u'logout', u'Logout'),
    ]
    action_type = Column(String(16))
    cmd = Column(String(255))
    date = Column(DateTime)
    user_profile_id = Column(Integer, ForeignKey('user_profile.id'))
    host_user_id = Column(Integer, ForeignKey('host_user.id'))

engine = create_engine(settings.conn)
Session = sessionmaker(bind=engine)
session = Session()
def list_host(user):
    obj = session.query(UserProfile).filter(UserProfile.username == user).all()#堡垒机用户obj
    host_user_list = []#主机用户id
    for i in obj:
        userprofile_id = i.id
        host_obj = session.query(UserProfile2HostUser).filter(UserProfile2HostUser.user_profile_id==userprofile_id).all()
        for i in host_obj:
            host_user_list.append(i.host_user_id)
    print(host_user_list)

    host_list = []#主机id
    user = []
    for i in host_user_list:
        host_ip = session.query(HostUser).filter(HostUser.id==i).all()
        for i in host_ip:
            user.append(i.username)
            host_list.append(i.host_id)
    host_list=list(set(host_list))
    user=list(set(user))
    #print(host_list)


    for i in host_list:
        hostname_obj = session.query(Host).filter(Host.id==i).all()
        for i in hostname_obj:
            host_user=session.query(HostUser).filter(i.id==HostUser.host_id).all()
            print(i.hostname,i.ip_addr,user)

def user_exist(username):
    auth = session.query(UserProfile).filter(UserProfile.username == username).first()
    return auth
def search(username):
    hosts = session.query()
def get_passwd(username,ip):
    obj = session.query(HostUser).filter(HostUser.username==username,Host.ip_addr==ip).join(Host,isouter=True).all()
    for i in obj:
        pwd = i.cert
    return pwd
def register(username,password):
    session.add_all([
        UserProfile(username=username,password=password)
    ])
    session.commit()
if __name__ == '__main__':
    list_host('hongpeng1')