import os
basedir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def transfer(user_id,send_id,type,money,now):
    file = '%s/log/log%s' % (basedir, user_id)
    with open(file,'a')as f:
        f.write('%s %s %s %sRMB at %s\n'%(user_id,type,send_id,money,now))
def withdraw(user_id,money,acc_data,now):
    file = '%s/log/log%s' % (basedir,user_id)
    with open(file,'a')as f:
        f.write('%s withdraw %sRMB at %s\n'%(user_id,money,now))
def repay(user_id,repay,now):
    file = '%s/log/log%s' % (basedir,user_id)
    with open(file,'a')as f:
        f.write('%s repay %sRMB at %s\n'%(user_id,repay,now))
def bill(user_id):
    file = '%s/log/log%s' % (basedir,user_id)
    f = open(file,'r')
    for line in f:
        print(line.strip())
def pay(user_id,account,now):
    file = '%s/log/log%s' % (basedir,user_id)
    with open(file,'a')as f:
        f.write('%s pay %sRMB at %s\n'%(user_id,account,now))



