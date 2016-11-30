# import time
# a = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
dict = {'key':[1]}
dict['key'].append(2)
print(dict.get('vv'))
import json
with open('ds','w')as f:
    json.loads(f.read())
    f.write(json.dumps(data))
    json.dump(data,f)