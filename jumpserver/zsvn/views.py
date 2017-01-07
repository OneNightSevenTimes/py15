# coding: utf-8

from django.shortcuts import render
from svn_api import ParseAuthz, send_email
from django.shortcuts import render_to_response
from jumpserver.api import *
import time
from models import SVNLog, SVNCommitLog


# Create your views here.
@require_role('admin')
def svn_manage(request):
    header_title, path1 = u'SVN管理', u'svn管理'
    if request.method == 'POST':
        aaa = request.POST.get('ops_type')
        print aaa
    # if request.method == 'POST':
    #     search_name = request.POST.get('search_username')
    #     print "i am here"
    #     print search_name
    #     pa = ParseAuthz()
    #     find_url = pa.get_permit_svn_url(search_name)
    #
    #     print find_url
    return render_to_response('zsvn/svn_manage.html', locals(), context_instance=RequestContext(request))


@require_role('admin')
def get_svn_url(request):

    show_result = False
    header_title, path1, path2 = u'SVN管理', u'svn管理', u'查询用户开通的svn权限'
    if request.method == 'POST':
        search_name = request.POST.get('search_username')
        pa = ParseAuthz()
        find_url = pa.get_permit_svn_url(search_name)
        show_result = True
    return render_to_response('zsvn/get_svn_url.html', locals(), context_instance=RequestContext(request))


@require_role('admin')
def get_svn_user(request):
    show_result = False
    header_title, path1, path2 = u'SVN管理', u'svn管理', u'查询SVN目录开通哪些用户权限'
    if request.method == 'POST':
        search_url = request.POST.get('search_url')
        pa = ParseAuthz()
        find_user = pa.get_permit_user(search_url)
        show_result = True
    return render_to_response('zsvn/get_svn_user.html', locals(), context_instance=RequestContext(request))


@require_role('admin')
def add_svn_group_user(request):
    header_title, path1, path2 = u'SVN管理', u'svn管理', u'添加SVN用户到组'
    #读取所有组
    pa = ParseAuthz()
    groups = pa.get_group()
    if request.method == 'POST':
        groupname = request.POST.get('groupname')
        sendmail = request.POST.get('sendmail')

        # 先备份
        backup_value = pa.file_backup()

        # 添加用户
        add_user = request.POST.get('add_user')
        status_add = pa.set_user_to_group(add_user, groupname)

        # 写日志
        manager = request.user.username
        actionlog = u"%s向%s组里添加了%s用户" % (manager, groupname, add_user)
        pa.write_svn_log(manager, actionlog, backup_value["current_timestamp"], backup_value["target_file"])

        if status_add == 'success':
            msg = u'添加用户成功'

            # 发邮件
            if sendmail:
                to = add_user + '@yolo24.com'
                subject = 'SVN添加用户到组'
                body = '用户添加成功, 用户%s新添加的svn目录权限如下：\n' % str(add_user)
                group_permit = pa.get_group_permit_url(groupname)
                for gp in group_permit:
                    body += gp['url']
                    body += '    '
                    body += gp['permit']
                    body += '\n'
                send_email(to, subject, body)
        else:
            error = u'添加用户失败'

    return render_to_response('zsvn/add_svn_group_user.html', locals(), context_instance=RequestContext(request))


@require_role('admin')
def add_svn_url_user(request):
    header_title, path1, path2 = u'SVN管理', u'svn管理', u'添加用户或组到SVN地址'
    if request.method == 'POST':
        svn_url = request.POST.get('svn_url')
        add_user = request.POST.get('add_user')
        permit = request.POST.get('permit')
        sendmail = request.POST.get('sendmail')
        pa = ParseAuthz()
        # 备份
        backup_value = pa.file_backup()

        status_add = pa.set_user_to_section(add_user, permit, svn_url)
        if status_add == 'success':
            msg = u'添加用户成功'
            # 发邮件
            if sendmail:
                if not add_user.startswith('@'):
                    to = add_user + '@yolo24.com'
                    subject = '添加SVN目录权限'
                    body = '权限添加成功, 用户%s新添加的svn目录权限如下：\n %s    %s' % (str(add_user), str(svn_url), str(permit))
                    send_email(to, subject, body)
        else:
            error = u'添加用户失败'

        # 写日志
        manager = request.user.username
        actionlog = u"%s向%ssvn地址里添加了%s用户,权限为%s" % (manager, svn_url, add_user, permit)
        pa.write_svn_log(manager, actionlog, backup_value["current_timestamp"], backup_value["target_file"])

    return render_to_response('zsvn/add_svn_url_user.html', locals(), context_instance=RequestContext(request))


@require_role('admin')
def add_svn_newgroup(request):
    header_title, path1, path2 = u'SVN管理', u'svn管理', u'添加SVN用户组'
    if request.method == 'POST':
        add_group = request.POST.get('add_group')
        add_user = request.POST.get('add_user')
        pa = ParseAuthz()
        # 备份
        backup_value = pa.file_backup()

        status_add = pa.add_group(add_group, add_user)
        if status_add == 'success':
            msg = u'添加用户成功'
        else:
            error = u'添加用户失败'

        # 写日志
        manager = request.user.username
        actionlog = u"%s添加新的用户组%s" % (manager, add_group)
        pa.write_svn_log(manager, actionlog, backup_value["current_timestamp"], backup_value["target_file"])

    return render_to_response('zsvn/add_svn_newgroup.html', locals(), context_instance=RequestContext(request))


@require_role('admin')
def delete_from_section(request):
    if request.method == 'POST':
        delete_user = request.POST.get('del_user')
        url = request.POST.get('url')
        pa = ParseAuthz()
        # 备份
        backup_value = pa.file_backup()

        remove_status = pa.remove_section_user(delete_user, url)

        # 写日志
        manager = request.user.username
        actionlog = u"从%s中删除用户%s" % (manager, delete_user)
        pa.write_svn_log(manager, actionlog, backup_value["current_timestamp"], backup_value["target_file"])

        if remove_status == "success":
            return HttpResponse(u'删除成功')
    return HttpResponse(u'删除失败')


@require_role('admin')
def delete_from_group(request):
    if request.method == 'POST':
        groupname = request.POST.get('groupname')
        username = request.POST.get('username')
        pa = ParseAuthz()
        # 备份
        backup_value = pa.file_backup()

        remove_status = pa.remove_group_user(groupname, username)

        # 写日志
        manager = request.user.username
        actionlog = u"从%s组中删除用户%s" % (manager, groupname)
        pa.write_svn_log(manager, actionlog, backup_value["current_timestamp"], backup_value["target_file"])

        if remove_status == "success":
            return HttpResponse(u'删除成功')
    return HttpResponse(u'删除失败')


@require_role('admin')
def show_svn_log(request):
    header_title, path1, path2 = u'SVN管理', u'svn管理', u'查看操作日志/回滚'
    svn_log = SVNLog.objects.order_by('-id')[:30]

    return render_to_response('zsvn/show_svn_log.html', locals(), context_instance=RequestContext(request))


@require_role('admin')
def svn_rollback(request):
    src_file = request.POST.get('src_file')
    pa = ParseAuthz()
    # 备份
    backup_value = pa.file_backup()

    rollback_status = pa.file_rollback(src_file)

    # 写日志
    manager = request.user.username
    actionlog = u"从%s执行了回滚操作，回滚文件为%s" % (manager, src_file)
    pa.write_svn_log(manager, actionlog, backup_value["current_timestamp"], backup_value["target_file"])

    if rollback_status == 'success':
        return HttpResponse(u'回滚成功')
    return HttpResponse(u'回滚失败')


def insert_svn_commit_log(request):
    ctime = request.POST.get('ctime')
    user = request.POST.get('user')
    files = request.POST.get('files')
    project = request.POST.get('project')
    commitlog = request.POST.get('commitlog')

    svn_commit_log = SVNCommitLog(ctime=ctime, user=user, files=files, project=project, commitlog=commitlog)
    svn_commit_log.save()

    return HttpResponse('insert success')


@require_role('admin')
def show_svn_commit_log(request):
    show_log = SVNCommitLog.objects.order_by('-id')
    contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(show_log, request)

    return render_to_response('zsvn/show_svn_commit_log.html', locals(), context_instance=RequestContext(request))


