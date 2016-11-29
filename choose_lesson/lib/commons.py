import uuid,hashlib
import time

def create_uuid():
    return str(uuid.uuid1())

def create_md5():
    m = hashlib.md5()
    m.update(bytes(str(time.time()),encoding='utf-8'))
    return m.hexdigest()

if __name__ == '__main__':
    x = create_md5()
    print(x)
    y = create_uuid()
    print(y)