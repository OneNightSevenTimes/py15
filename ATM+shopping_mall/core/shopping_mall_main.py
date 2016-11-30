from core import atm_main
from core import auth
def interactive():
    dict_list = {
        "iphone":5888,
        "mac":12000,
        "cloth": 300,
        "durex": 58,
        "shoes": 500,
        "apple": 10,
        "pen": 20,
    }
    buy_list = []
    account = 0
    print('我们有如下商品：'.center(50,'-'))
    for index,key in enumerate(dict_list):
        print(index,key,dict_list[key])
    while True:
        choice = input('请选择商品序号：[q]退出[g]结算')
        if len(choice)==0 and choice not in dict_list:continue
        if choice == 'q':break
        if choice.isdigit():
            choice = int(choice)
            key = list(dict_list.keys())[choice]
            #去重，统计相同商品数量
            buy_list.append(key)
            se = set(buy_list)
            shopping_car = {}
            for i in se:
                a = buy_list.count(i)
                shopping_car[i]=a
            print('%s加入购物车'%key)
        if choice == 'g':
            for key in shopping_car:
                account+=shopping_car[key]*dict_list[key]#消费金额
                print('商品%s 件数 %s'%(key,shopping_car[key]))
            card_id = int(input('卡号：'))
            password = input('密码：')
            status = auth.get_info(card_id,password)
            if status == True:
                atm_main.pay(card_id,account)
