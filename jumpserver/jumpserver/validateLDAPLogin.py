#coding: utf-8
import  ldap

'''
实现LDAP用户登录验证，首先获取用户的dn，然后再验证用户名和密码
'''

ldappath = "ldap://ldap.gomeo2o.cn:389/"#ldap服务器地址
baseDN = "ou=People,dc=ldap,dc=gomeo2o,dc=cn"#根目录
#ldapuser = "lixiaokai";#ldap服务器用户名
#ldappass = "aaa";#ldap服务器密码

#获取用户的dn
def _validateLDAPUser(user, password):
    try:
        l = ldap.initialize(ldappath)
        l.protocol_version = ldap.VERSION3
        l.simple_bind(user,password)

        searchScope  = ldap.SCOPE_SUBTREE
        searchFiltername = "cn"
        retrieveAttributes = None
        searchFilter = '(' + searchFiltername + "=" + user +')'

        ldap_result_id = l.search(baseDN, searchScope, searchFilter, retrieveAttributes)
        result_type, result_data = l.result(ldap_result_id,1)
        if(not len(result_data) == 0):
          # r_a,r_b = result_data[0]
	  #print r_b
          #print r_b["distinguishedName"]
          return 1, result_data[0][0]
        else:
          return 0, ''
    except ldap.LDAPError, e:
        print e
        return 0, ''
    finally:
        l.unbind()
        del l

#连接超时，尝试多次连接
def GetDn(user, password, trynum = 30):
    i = 0
    isfound = 0
    foundResult = ""
    while(i < trynum):
        isfound, foundResult = _validateLDAPUser(user, password)
        if(isfound):
          break
        i+=1
    return foundResult


def LDAPLogin(userName,Password):
    try:
        if(Password==""):
            return "密码不能为空"
        dn = GetDn(userName, Password,10)
        if(dn==''):
            return "用户不存在,请申请LDAP权限"
        my_ldap = ldap.initialize(ldappath)
        my_ldap.simple_bind_s(dn,Password)
        return "success"
    except Exception,e:
        return "用户名或密码错误,请重新输入正确的账户和密码!"

