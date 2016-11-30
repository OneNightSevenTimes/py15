import os
import sys
basedir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(basedir)
from core import atm_main
from core import shopping_mall_main

def main():
    msg = '''
    1.  ATM
    2.  shopping_mall
    3.  exit
    '''
    menu = {
        '1':atm_main,
        '2':shopping_mall_main,
        '3':exit
    }
    while True:
        print('ATM+shopping_mall'.center(50,'*'))
        print(msg)
        print(''.center(50,'*'))
        choice = input('please choose:').strip()
        if len(choice) == 0 or choice not in menu:continue
        if choice == '3':break
        menu[choice].interactive()
if __name__ == '__main__':
    main()