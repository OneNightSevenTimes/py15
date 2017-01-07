from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from conf import settings

Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String(32))
    password = Column(String(32))
    type_id = Column(Integer,ForeignKey('user_type.id'))
    extra = Column(String(16))
    type = relationship("Users_type", backref='t')


class Users_type(Base):
    __tablename__ = 'user_type'
    id = Column(Integer,primary_key=True)
    user_type = Column(String(16))

class Host(Base):
    __tablename__='host'
    nid = Column(Integer,primary_key=True,autoincrement=True)
    hostname = Column(String(32))
    port = Column(String(32))
    ip = Column(String(32))

class HostToHostUser(Base):
    __tablename__='host_to_user'
    nid = Column(Integer,primary_key=True,autoincrement=True)
    host_id = Column(Integer,ForeignKey('host.nid'))
    host_user_id = Column(Integer,ForeignKey('users.id'))

    host = relationship('Host',backref='h')
    host_user = relationship('Users',backref='u')

class Operation_db(object):
    def __init__(self):
        self.engine = create_engine("mysql+pymysql://%s:%s@%s:3306/%s?charset=utf8" \
                                %(settings.mysql_user,settings.mysql_password,settings.mysql_ip,\
                                settings.mysql_db), max_overflow=5)

        Session = sessionmaker(bind=self.engine)
        self.session = Session()


    def create(self):
        Base.metadata.create_all(self.engine)

    def add_data(self):
        # self.session.add_all([
        #     Users(name='alex1',password='123',type_id=1,extra='somebody1'),
        #     Users(name='alex2',password='123',type_id=2,extra='somebody2'),
        #     Users(name='alex3',password='123',type_id=1,extra='somebody3')
        # ])
        # self.session.commit()
        # self.session.add_all([
        #     Users_type(id=1,user_type='root'),
        #     Users_type(id=2,user_type='regular'),
        # ])
        # self.session.commit()
        self.session.add_all([
            Host(hostname='bj01-ngx1.com', port='22', ip='192.168.1.1'),
            Host(hostname='bj01-ngx2.com', port='22', ip='192.168.1.2'),
            Host(hostname='bj01-mql1.com', port='22', ip='192.168.1.3'),
        ])
        self.session.commit()
        self.session.add_all([
            HostToHostUser(host_id=1,host_user_id=1 ),
            HostToHostUser(host_id=2,host_user_id=1 ),
            HostToHostUser(host_id=2,host_user_id=2 ),
            HostToHostUser(host_id=3,host_user_id=3 ),
        ])
        self.session.commit()

    def check_data(self):
        info = {}
        v = self.session.query(Users).join(Users_type).all()
        for item in v:
            info['%s' % item.name]={}
            info['%s'%item.name]['password']=item.password
            info['%s'%item.name]['type'] = item.type.user_type
            #info[item.name]['user_type']=item.type.user_type
        return(info)
            #print(item.name,item.password,item.type.user_type)
        # v = self.session.query(Users).all()
        # print(v)
    def check_host_data(self):
        '''把主机信息和对应授权的用户一起列出来'''
        info = {}
        v = self.session.query(Host).all()
        for i in v:
            #print(item.hostname,item.ip,item.port)

            info['%s' % i.hostname] = {}
            info['%s' % i.hostname]['IP'] = i.ip
            info['%s' % i.hostname]['端口'] = i.port
            info['%s' % i.hostname]['用户'] = []

            obj = self.session.query(Host).filter(Host.hostname==i.hostname).first()
            #取主机对应的用户
            for item in obj.h:
                info['%s'%i.hostname]['用户'].append(item.host_user.name)
        return(info)
    def change_type(self,change_name,change_after):
        dic = {'root':1,'regular':2}
        type = dic[change_after]
        if self.session.query(Users).filter(Users.name==change_name).update({Users.type_id:type}):
            return True
        # v = self.session.query(Users).filter(Users.name==change_name).all()
        # print(v)
        # for row in v:
        #     print(row.type.user_type)
    def add_user(self,username,password,type,extra):
        self.session.add(Users(name=username,password=password,type_id=type,extra=extra))
        #add_all时对象得放在一个列表中
        self.session.commit()
    def remove_user(self,username):
        self.session.query(Users).filter(Users.name==username).delete()
        self.session.commit()

    def add_host(self,name,ip,port):
        self.session.add(Host(hostname=name, port=port,ip=ip))
        self.session.commit()

    def remove_host(self,hostname):
        self.session.query(Host).filter(Host.hostname==hostname).delete()
        self.session.commit()

    def change_host(self,hostname,ip,port):

        self.session.query(Host).filter(Host.hostname==hostname).\
            update({Host.hostname:hostname,Host.ip:ip,Host.port:port})

    def add_host_user(self,host,user):
        '''用户授权'''
        host_id = self.session.query(Host.nid).filter(Host.hostname==host).first()
        host_id = host_id[0]
        user_id = self.session.query(Users.id).filter(Users.name==user).first()
        user_id = user_id[0]
        self.session.add(HostToHostUser(host_id=host_id,host_user_id=user_id))
        self.session.commit()

    def remove_host_user(self,host,user):
        '''用户删除权限'''
        host_id = self.session.query(Host.nid).filter(Host.hostname == host).first()
        host_id = host_id[0]
        user_id = self.session.query(Users.id).filter(Users.name == user).first()
        user_id = user_id[0]
        self.session.query(HostToHostUser).filter(HostToHostUser.host_id==host_id,HostToHostUser.host_user_id==user_id).delete()
        self.session.commit()








if __name__ == '__main__':
    a = Operation_db()
    #a.create()
    #a.add_data()
    #a.check_data()
    a.check_host_data()