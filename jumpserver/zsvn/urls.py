# coding:utf-8
from django.conf.urls import patterns, include, url
from zsvn.views import *

urlpatterns = patterns('',
    url(r'^svn/manage/$', svn_manage, name='svn_manage'),
    url(r'^svn/get_svn_url/$', get_svn_url, name='get_svn_url'),
    url(r'^svn/get_svn_user/$', get_svn_user, name='get_svn_user'),
    url(r'^svn/add_svn_group_user/$', add_svn_group_user, name='add_svn_group_user'),
    url(r'^svn/add_svn_url_user/$', add_svn_url_user, name='add_svn_url_user'),
    url(r'^svn/add_svn_newgroup/$', add_svn_newgroup, name='add_svn_newgroup'),
    url(r'^svn/delete_from_section/$', delete_from_section, name='delete_from_section'),
    url(r'^svn/delete_from_group/$', delete_from_group, name='delete_from_group'),
    url(r'^svn/show_svn_log/$', show_svn_log, name='show_svn_log'),
    url(r'^svn/svn_rollback/$', svn_rollback, name='svn_rollback'),
    url(r'^svn/insert_svn_commit_log/$', insert_svn_commit_log, name='insert_svn_commit_log'),
    url(r'^svn/show_svn_commit_log/$', show_svn_commit_log, name='show_svn_commit_log'),
)
