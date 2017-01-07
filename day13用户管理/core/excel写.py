import xlwt
import time


f = xlwt.Workbook()

sheet1 = f.add_sheet('hosts')
sheet1.col(0).width = 6666
sheet1.col(1).width = 6666
row0=['主机','IP','端口']
row1=['bj01-tfs1.com','192.168.2.2','22']

for i in range(0,len(row0)):
    sheet1.write(0,i,row0[i])
for i in range(0, len(row1)):
    sheet1.write(1, i, row1[i])
f.save('hosts%s.xls'%time.strftime('%Y-%m-%d'))