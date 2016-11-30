import os
import sys
import time
from db import register
from core import auth
from core import judge
from core import logger
basedir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(basedir)
status = False

def login(func):
    #print('welcome to oldboy bank'.center(50, '-'))
    def inner(*args,**kwargs):
        global status
        if not status:
            #user_id = input('请输入卡号:').strip()
            password = input('请输入密码:').strip()
            status = auth.get_info(user_id,password)
        if status:
            # global user_id1
            # card_id = int(user_id1)
            func(*args,**kwargs)
    return inner

#acc_data = register.load(user_id1)
@login
def transfer(card_id):
    acc_data = register.load(card_id)
    send_id = input('请输入需要转账的账户：').strip()
    status= judge.user_judge(send_id)
    if status:
        send_data = register.load(send_id)
        money = int(input('请输入金额：').strip())
        acc_data['balance'] = int(acc_data['balance'])
        send_data['balance'] = int(send_data['balance'])
        if money > acc_data['balance']:
            print('\033[31;1m账户余额不足\033[0m')
        else:
            acc_data['balance'] -= money
            send_data['balance'] += money
            register.dump(card_id,acc_data)
            register.dump(send_id,send_data)
            now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
            print("\033[31;1m成功转给用户[%s]%sRMB\033[0m"%(send_id,money))
            type = 'transfer'
            logger.transfer(card_id,send_id,type,money,now)

    else:
        print('\033[31;1m你需要转入的账号不存在\033[0m')
@login
def withdraw(card_id):
    acc_data = register.load(card_id)
    balance = acc_data['balance']
    credit = acc_data['credit']
    print("\033[31;1m你的余额为%s,你的透支额度为%s\033[0m"%(balance,credit))
    money = int(input('输入取款金额：').strip())
    if money < int(balance):
        acc_data['balance'] -= money
    else:
        acc_data['balance'] = 0
        acc_data['credit'] = int(credit) - money + int(balance)
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    print('\033[31;1m成功取款[%s],账户余额[%s],透支额度[%s]\033[0m'%(money,acc_data['balance'],acc_data['credit']))
    register.dump(card_id,acc_data)
    logger.withdraw(card_id,money,acc_data,now)
@login
def repay(card_id):
    acc_data = register.load(card_id)
    limit = int(acc_data['limit'])
    credit = int(acc_data['credit'])
    print(limit,credit)
    if credit < limit:
        repay = int(input('输入还款金额：'))
        if repay < limit-credit:
            acc_data['credit'] = acc_data['credit']+repay
            # register.dump(card_id,acc_data)
            # now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
            # logger.repay(card_id,repay,now)
            left = limit-credit-repay
            print('已还款%s,还需要还%s'%(repay,left))
        else:
            need = limit-credit
            credit = limit
            acc_data['balance'] = repay-need
            acc_data['credit'] = limit
            print('已还款%s,已存款%s'%(need,acc_data['balance']))
    else:
        repay=int(input('无需还款，请输入存款金额'))
        acc_data['balance'] = int(acc_data['balance'])+repay
        # register.dump(card_id,acc_data)
        # now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        # logger.repay(card_id,recharge,now)
        print('已存款[%s]'%repay)
    register.dump(card_id, acc_data)
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    logger.repay(card_id, repay, now)
@login
def bill(card_id):
    #user_id = input('请输入需要查询的用户：').strip()
    logger.bill(card_id)

def pay(card_id,account):
    acc_data = register.load(card_id)
    balance = int(acc_data['balance'])
    credit = int(acc_data['credit'])
    if account > balance+credit:
        print('余额不足')
    else:
        if account < balance:
            balance -= account
            acc_data['balance'] = balance
        else:
            left = account - balance
            credit -= left
            acc_data['balance'] = 0
            acc_data['credit'] = credit
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        print('支付成功，共消费%s'%account)
        register.dump(card_id,acc_data)
        logger.pay(card_id,account,now)

def registe(*args,**kwargs):
    user_id = int(input('input the card_id you choose:').strip())
    passwd = input('input your password:').strip()
    credit = int(input('input your credit:').strip())
    balance = int(input('input your balance:').strip())
    register.username(user_id,passwd,credit,balance)

def interactive():
    msg = '''
    1. 注册
    2. 转账
    3. 取款
    4. 还款
    5. 账单
    6. 退出
    '''

    menu_dic = {
        '1':registe,
        '2':transfer,
        '3':withdraw,
        '4':repay,
        '5':bill,
        '6':exit
    }
    #card_id = int(input('account'))
    while True:
        global user_id
        user_id = int(input('请输入卡号：').strip())
        flag = True
        while flag:
            db = '%s/db/accounts/%s.json' % (basedir, 'user%s' % user_id)
            if os.path.isfile(db):
                print(msg)
                choice = input('please choose:').strip()
                if choice in menu_dic:
                    menu_dic[choice](user_id)
                else:
                    print('\033[31;1mchoice do not exist!\033[0m')
            else:
                user_id = input('\033[31;1m返回重输按[b]没卡输入[r]注册\033[0m')
                if user_id == 'r':
                    registe()
                if user_id == 'b':
                    break

