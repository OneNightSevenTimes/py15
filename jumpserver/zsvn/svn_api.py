# coding:utf-8

import ConfigParser
import os
import shutil
import time
from zsvn.models import SVNLog

class ParseAuthz:
    # name
    def __init__(self):
        file_path = "/gomeo2o/data/authz"
        self.file_path = file_path
        self.cf = ConfigParser.ConfigParser()
        self.cf.read(file_path)

    # method
    # 将section转成url
    def get_url(self, section):
        start_url = "https://svn.gomeo2o.cn:8443/"
        section = section.replace(':', '')
        full_url = start_url + section
        return full_url

    # 将url转成section
    def get_section(self, url):
        uri = url.split('https://svn.gomeo2o.cn:8443/')[1]
        index = uri.index('/')
        section = uri[:index] + ":" + uri[index:]
        return section

    # 根据用户获取SVN的权限
    def get_permit_svn_url(self, name):
        """
        return {"url": "http://aaa", "permit": 'rw', "permit_type": '[user, group]'}
        """
        has_permission = []
        cf = self.cf
        sections = cf.sections()
        in_group = []
        for s in sections:
            if s == "groups":
                options = cf.options(s)
                for o in options:
                    value = cf.get(s, o).split(",")
                    if name in value:
                        in_group.append(o)
            else:
                options = cf.options(s)
                for o in options:
                    if o.startswith('@'):
                        group_name = o[1:]
                        if group_name in in_group:
                            url = self.get_url(s)
                            permit = cf.get(s, o)
                            permit_type = 'group'
                            record = {'url': url, 'permit': permit, 'permit_type': [permit_type], 'groupname': group_name}
                            has_permission.append(record)
                    else:
                        if o == name:
                            url = self.get_url(s)
                            permit = cf.get(s, o)
                            permit_type = 'user'
                            exist_url = []
                            for p in has_permission:
                                exist_url.append(p['url'])
                            if url in exist_url:
                                index = exist_url.index(url)
                                record = {'url': url, 'permit': permit, 'permit_type': ['user', 'group'], 'groupname': has_permission[index]["groupname"]}
                                has_permission[index] = record
                            else:
                                record = {'url': url, 'permit': permit, 'permit_type': [permit_type]}
                                has_permission.append(record)
        return has_permission

    # 根据SVN地址查看有权限的用户
    def get_permit_user(self, url):
        """
        return {"username": "lifei", "permit": 'rw', "permit_type": '[user, group]', "groupname": ""}
        """
        has_permission_user = []
        cf = self.cf
        section = self.get_section(url)
        options = cf.options(section)
        for o in options:
            record = {}
            permit = cf.get(section, o)
            if o.startswith('@'):
                # 这是一个组，需要读取组里的所有用户
                group_section = 'groups'
                option = o[1:]
                names = cf.get(group_section, option)
                name_list = names.split(',')
                for name in name_list:
                    record = {"username": name, "permit": permit, "permit_type": ['group'], "groupname": option[1:]}
                    has_permission_user.append(record)
            else:
                if has_permission_user:
                    exist_user = []
                    for user in has_permission_user:
                        exist_user.append(user['username'])
                    if o in exist_user:
                        index = exist_user.index(o)
                        record = {"username": o, "permit": permit, "permit_type": ['user'], "groupname": ""}
                        has_permission_user[index] = record
                    else:
                        record = {"username": o, "permit": permit, "permit_type": ['user'], "groupname": ""}
                        has_permission_user.append(record)
                else:
                    record = {"username": o, "permit": permit, "permit_type": ['user'], "groupname": ""}
                    has_permission_user.append(record)

        return has_permission_user

    # 根据用户组，获取该组的svn权限
    def get_group_permit_url(self, groupname):
        """
        return {"url": "http://aaa", "permit": 'rw'}
        """
        has_permission = []
        cf = self.cf
        sections = cf.sections()
        groupname = '@' + groupname
        for s in sections:
            if s != 'groups':
                options = cf.options(s)
                for o in options:
                    if o == groupname:
                        url = self.get_url(s)
                        permit = cf.get(s, o)
                        has_permission.append({"url": url, "permit": permit})

        return has_permission

    # 获取所有组
    def get_group(self):
        cf = self.cf
        groups = cf.options('groups')
        return groups

    # 向组里添加用户
    def set_user_to_group(self, username, groupname):
        cf = self.cf
        file_path = self.file_path
        old_username = cf.get('groups', groupname)
        old_name_list = old_username.split(',')
        if username not in old_name_list:
            new_username = old_username + "," + username
            cf.set("groups", groupname, new_username)
            cf.write(open(file_path, 'w'))
            return "success"
        else:
            return "该组中已经存在此用户"

    # 向SVN目录里添加权限
    def set_user_to_section(self, username, permit, url):
        cf = self.cf
        file_path = self.file_path
        section = self.get_section(url)
        if username not in cf.options(section):
            cf.set(section, username, permit)
            cf.write(open(file_path, 'w'))
            return "success"
        else:
            return u'该用户已经存在'

    # 添加新的用户组
    def add_group(self, groupname, users):
        cf = self.cf
        file_path = self.file_path
        if groupname not in cf.options('groups'):
            cf.set('groups', groupname, users)
            cf.write(open(file_path, 'w'))
            return "success"
        else:
            return u'该分组已经存在'

    # 从section中删除用户
    def remove_section_user(self, username, url):
        section = self.get_section(url)
        cf = self.cf
        file_path = self.file_path
        cf.remove_option(section, username)
        cf.write(open(file_path, 'w'))
        return "success"

    # 从用户组中删除用户
    def remove_group_user(self, groupname, username):
        cf = self.cf
        file_path = self.file_path
        old_names = cf.get('groups', groupname)
        old_name_list = old_names.split(',')
        if username in old_name_list:
            old_name_list.remove(username)
            new_name = ''
            for name in old_name_list:
                new_name += name
                new_name += ','
            new_name = new_name[:-1]
            cf.set('groups', groupname, new_name)
            cf.write(open(file_path, 'w'))
            return "success"
        else:
            return u'用户不存在这个组中'

    # 配置文件备份
    def file_backup(self):
        src_file = "authz"
        base_src_path = "/gomeo2o/data/"
        base_target_path = "/gomeo2o/data/svnbakfile/"
        is_dir = os.path.isdir(base_target_path)
        if not is_dir:
            os.mkdir(base_target_path)

        current_time = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        current_timestamp = time.mktime(time.strptime(current_time, '%Y%m%d%H%M%S'))
        target_file = "authz_" + current_time

        fullname_src = base_src_path + src_file
        fullname_target = base_target_path + target_file
        shutil.copy(fullname_src, fullname_target)
        return_value = {"current_timestamp": current_timestamp, "target_file": target_file}
        return return_value

    # 配置文件回滚
    def file_rollback(self, src_file):
        target_file = "/gomeo2o/data/authz"
        fullname_src = "/gomeo2o/data/svnbakfile/" + src_file
        shutil.copy(fullname_src, target_file)
        return "success"

    # 向数据库中写入日志记录
    def write_svn_log(self, manager, actionlog, addtime, bakfile):
        log_instance = SVNLog(manager=manager, actionlog=actionlog, type='svn', addtime=addtime, bakfile=bakfile)
        log_instance.save()
        return "success"


    # 同步到SVN服务器
    def sync_to_server(self):
        # /usr/bin/rsync /gome/data/authz 10.144.5.210::authzsync/authz > /dev/null 2>&1
        cmd = '/usr/bin/rsync /gomeo2o/data/authz 10.144.5.210::authzsync/authz > /dev/null 2>&1'
        status = os.system(cmd)
        if status != 0:
            return "error"
        return "success"


def send_email(to, subject, body):
    base_dir = os.getcwd()
    mail_path = base_dir + '/tools/Mail/mail'
    to = str(to)
    cmd = 'perl %s --title %s --text "%s" --to %s' % (mail_path, subject, body, to)
    os.system(cmd)
    return 'success'

if __name__ == '__main__':
    # check
    username = "lixiaokai"
    file_path = "/gomeo2o/data/authz.txt"
    pa1 = ParseAuthz()
    svn_url = pa1.get_permit_svn_url(username)
    print svn_url
#    svn_user = pa1.get_permit_user('https://svn.gomeo2o.cn:8443/gomeo2o_dev/src/terminus')
#    pa1.remove_group_user('admin', 'lixiaokai')
#    pa1.remove_section_user('lixiaokai', 'https://svn.gomeo2o.cn:8443/gomeo2o_dev/src/terminus')
#    pa1.add_group('zeus', 'lixiaokai,sunfeng,zhaijianbo')
#    pa1.set_user_to_section('lixiaokai', 'rw', 'https://svn.gomeo2o.cn:8443/gomeo2o_dev/src/terminus')
#    pa1.set_user_to_group('lixiaokai', 'admin')
#    pa1.get_url('O2O:/maintain')

#    print "THE END"
