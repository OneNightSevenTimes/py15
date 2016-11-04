#haha
#record_list中存放的是需要写入新文件的内容
import os
def file_handle(filename,backend_data,type,record_list=None):
    new_file=filename+'_new'
    bak_file=filename+'_bak'
    if type == 'fetch':
        r_list = []
        with open(filename,'r')as f:
            tag = False
            for line in f:
                if line.strip() == backend_data:
                    tag = True
                    continue
                if tag and line.startswith('backend'):
                    break
                if tag and line:
                    r_list.append(line.strip())
            for i in r_list:
                print(i)
            return r_list
    elif type == 'append':
        with open(filename,'r')as old,\
                open('haproxy_new.conf','w')as new:
            for line in old:
                new.write(line)
            for new_line in record_list:
                if new_line.startswith('backend'):
                    new.write('\n'+new_line+'\n')
                else:
                    new.write('%s%s\n'%(' '*8,new_line))
        os.rename(filename, bak_file)
        os.rename(new_file, filename)
        os.remove(bak_file)
    elif type == 'change':
        with open(filename, 'r')as old, \
                open(new_file, 'w')as new:
            tar = False
            has_write = False
            for line in old:
                if line.strip() == backend_data:
                    tar = True
                    continue
                if tar and line.startswith('backend'):
                    tar = False
                if not tar:  # 没匹配到backend
                    new.write(line)
                else:  # 匹配到backend
                    if not has_write:  # 如果不加这个，因为遍历文件,record_list列表中有几个值，就会重复写几次
                        for line in record_list:
                            if line.startswith('backend'):
                                new.write(line + '\n')
                            else:
                                new.write('%s%s\n' % (' ' * 8, line))
                        has_write = True
        os.rename(filename, bak_file)
        os.rename(new_file, filename)
        os.remove(bak_file)

def fetch(data):
    backend_data = 'backend %s'%data
    return file_handle('haproxy.conf',backend_data,type='fetch')

def remove(data):
    backend = data['backend']
    record_list = fetch(backend)
    backend_data = 'backend %s'%backend
    record_data = 'server %s %s weight %s maxconn %s'\
                  %(data['record']['server'],\
                    data['record']['server'],\
                    data['record']['weight'],\
                    data['record']['maxconn'])
    if not record_list or record_data not in record_list:
        print('\033[31;1m不存在\033[0m')
        return
    else:
        record_list.insert(0,backend_data)
        record_list.remove(record_data)
        file_handle('haproxy.conf',backend_data,'change',record_list)
def add(data):
    backend = data['backend']#取字典中'backend'对应的值
    record_list = fetch(backend)#调用fetch，取backend对应的record，放入列表中
    record_data = 'server %s %s weight %s maxconn %s'\
             %(data['record']['server'],\
               data['record']['server'],\
               data['record']['weight'],\
               data['record']['maxconn'])
    backend_data ='backend %s'%backend

    #backend不存在,record_list里面加上backend和record，文件处理
    if not record_list:
        record_list.append(backend_data)
        record_list.append(record_data)
        file_handle('haproxy.conf',backend_data,'append',record_list)
    #backend存在
    else:
        #把输入的backend信息都加入record_list中
        record_list.insert(0,backend_data)
        #如果用户输入的record不在record_list中
        if record_data not in record_list:
            #把这条record加到record_list
            record_list.append(record_data)
        file_handle('haproxy.conf',backend_data,'change',record_list)
def change(data):
    backend = data[0]['backend']
    backend_data = 'backend %s'%backend
    record_list = fetch(backend)
    old_record = 'server %s %s weight %s maxconn %s'\
             %(data[0]['record']['server'],\
               data[0]['record']['server'],\
               data[0]['record']['weight'],\
               data[0]['record']['maxconn'])
    new_record = 'server %s %s weight %s maxconn %s'\
             %(data[1]['record']['server'],\
               data[1]['record']['server'],\
               data[1]['record']['weight'],\
               data[1]['record']['maxconn'])
    if not record_list or old_record not in record_list:
        print('\033[33;1m不存在\033[0m')
    else:
        record_list.insert(0, backend_data)
        index = record_list.index(old_record)
        record_list[index] = new_record
        file_handle('haproxy.conf', backend_data, 'change', record_list)


if __name__ == '__main__':
    msg = '''
    1. 查询
    2. 增加
    3. 删除
    4. 修改
    5. 退出
    '''
    '''把程序的功能都写到一个字典中，这里不能用函数，因为需要传入参数
    把用户的选择写在字典里的好处就是以后如果要修改的话，只需要在这个字典里修改
    不需要去下面的主逻辑中修改，程序的可扩展性提高
    '''
    menu_list = {
        '1':fetch,
        '2':add,
        '3':remove,
        '4':change,
        '5':exit
    }
    while True:
        print(msg)
        choice = input('选项-->').strip()
        if len(choice) == 0 or choice not in menu_list:continue
        if choice == '5':break
        data = input('数据-->').strip()
        #除了查，其他都是输入字典类型的字符串，通过eval转换成字典
        if choice != '1':
            data = eval(data)
        menu_list[choice](data)#== fetch(data)

        #{'backend':'www.hongpeng.org','record':{'server':'1.1.1.1','weight':20,'maxconn':33333}}
