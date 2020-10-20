# 第三章 主机发现 ping 

激动!!看了两章小故事终于开始正式教程了=。=

## 前言

任何网络侦查任务的第一步是将一组巨大的IP范围缩减为活动主机或有趣主机列表

本章节先讨论高级控制选项的Nmap ping扫描如何整体工作.然后介绍特定技术,包括它们如何工作以及何种情况最合适

## 指定目标主机和网络

Nmap上不是选项的内容都被看作主机规范

最简单的情况是指定要扫描的IP地址或主机名

当我们想扫描整个网络,Nmap支持CIDR样式寻址,也可以使用192.168.0.1-254跳过0和255,并且可以192.168.3-5,7.1这样会扫描4个地址

Nmap同时接受多个主机规范,并且不必是同一类型. nmap scanme.nmap.org 192.168.0.0/8 10.0.0,1,3-7.-可以满足需求

## 清单输入 -iL

在命令后传递大量主机不方便,因此可以使用文件名作为 iL 参数

## 随即选择目标 -iR <numtarget>

如果您发现自己真的在一个下雨的下午感到无聊，请尝试使用命令nmap -sS -PS80 -iR 0 -p 80 查找随机Web服务器进行浏览

## 排除目标 --exclude --excludefile <filename>

任何情况下都有不希望扫描的机器,但是 --exclude不能使用逗号表示范围,因为--exclude自身需要使用逗号

## 练习例子

NMAP scanme.nmap.org， NMAP scanme.nmap.org/32， NMAP 64.13.134.52

假设scanme.nmap.org解析为64.13.134.52，这三个命令都具有相同的作用。他们扫描一个IP，然后退出

NMAP scanme.nmap.org/24， NMAP 64.13.134.52/24， NMAP 64.13.134.-， NMAP 64.13.134.0-255

这四个命令都要求Nmap从64.13.134.0到64.13.134.255扫描256个IP地址。换句话说，他们要求扫描scanme.nmap.org周围C类大小的地址空间

nmap 64.13.134.52/24 --exclude scanme.nmap.org,insecure.org

告诉Nmap在64.13.134.52附近扫描C类，但如果在该地址范围内找到scanme.nmap.org和insecure.org，则跳过它们

nmap 10.0.0.0/8 --exclude 10.6.0.0/16,ultra-sensitive-host.company.com

告诉Nmap扫描整个私有10范围，但它必须跳过以10.6开头的所有内容以及ultra-sensitive-host.company.com

egrep'^ lease'/var/lib/dhcp/Dhcpd.leases | awk'{print $ 2}'| nmap -iL-

获取分配的DHCP IP地址列表，并将其直接送入Nmap进行扫描。请注意，将连字符传递给-iL从标准输入读取

nmap -6 2001:800:40:2a03::3

扫描地址为2001:800:40:2a03::3 的IPv6主机

# 查找组织IP地址

nmap可以自动执行网络扫描的方方面面,但是我们仍然需要制定目标

我们可以 -iR 瞎打,也可以使用 0.0.0.0/0扫描整个互联网,这些行为可能耗时数年

这一节将会演示以公司域名转换为目标公司拥有,运营,附属的网络模块列表

## 例子 3.1 host命令查询插件dns记录

```shell
> host -t ns target.com
target.com名称服务器ns4.target.com。
target.com名称服务器ns3.target.com。
target.com名称服务器ns1-auth.sprintlink.net。
target.com名称服务器ns2-auth.sprintlink.net。
target.com名称服务器ns3-auth.sprintlink.net。
> host -t a target.com
target.com的地址为161.225.130.163
target.com地址为161.225.136.0
> host -t aaaa target.com
target.com没有AAAA记录
> host -t mx target.com
target.com邮件由50 smtp02.target.com处理。
target.com邮件由5 smtp01.target.com处理。
> host -t soa target.com
target.com的SOA记录为extdns02.target.com。hostmaster.target.com。
```

dns将域名解析为IP地址

于是找到了很多target.com的名称和地址

主机名	IP地址
ns3.target.com	161.225.130.130
ns4.target.com	161.225.136.136
ns5.target.com	161.225.130.150
target.com	161.225.136.0、161.225.130.163
smtp01.target.com	161.225.140.120
smtp02.target.com	198.70.53.234，198.70.53.235
extdns02.target.com	172.17.14.69
www.target.com	207.171.166.49

至此已经发现7这台域名服务器,但是这些服务器拒绝=。=

## 例子3.2 target.com使用dig(域信息groper)工具进行区域传输尝试失败,然后是针对不相关组织的成功尝试(cpsr.org)

```shell
> dig @ns2-auth.sprintlink.net -t AXFR target.com
; <<>> DiG 9.5.0b3 <<>> @ns2-auth.sprintlink.net -t AXFR target.com

; Transfer failed.

> dig @ns2.eppi.com -t AXFR cpsr.org
; <<>> DiG 9.5.0b1 <<>> @ns2.eppi.com -t AXFR cpsr.org

cpsr.org             10800   IN      SOA   ns1.findpage.com. root.cpsr.org.
cpsr.org.            10800   IN      NS    ns.stimpy.net.
cpsr.org.            10800   IN      NS    ns1.findpage.com.
cpsr.org.            10800   IN      NS    ns2.eppi.com.
cpsr.org.            10800   IN      A     208.96.55.202
cpsr.org.            10800   IN      MX    0 smtp.electricembers.net.
diac.cpsr.org.       10800   IN      A     64.147.163.10
groups.cpsr.org.     10800   IN      NS    ns1.electricembers.net.
localhost.cpsr.org.  10800   IN      A     127.0.0.1
mail.cpsr.org.       10800   IN      A     209.209.81.73
peru.cpsr.org.       10800   IN      A     208.96.55.202
www.peru.cpsr.org.   10800   IN      A     208.96.55.202
[...]
```

收集这样的DNS结果时，一个常见的错误是假定一个域名下的所有系统都必须是该组织网络的一部分并且可以安全地进行扫描

实际上，没有什么可以阻止组织添加指向Internet上任何地方的记录

可能是将服务器放在了第三方,同时保留了域名

例如，www.target.com解析为207.171.166.49。这是目标网络的一部分，还是由我们可能不想扫描的第三方管理？DNS反向解析是三种快速简便的测试， traceroute，以及针对相关IP地址注册表的whois

## 例子3.3 对www.target.com 进行反向nmapdns和traceroute扫描

```shell
＃nmap -Pn -T4 --traceroute www.target.com

启动Nmap（http://nmap.org）166-49.amazon.com（207.171.166.49 ）的
Nmap扫描报告
未显示：998个过滤的端口
端口状态服务
80 / tcp打开http 
443 / tcp打开https 
TRACEROUTE（使用端口80 / tcp）
HOP RTT地址
[cut] 
9 84.94 ae-2.ebr4.NewYork1.Level3.net（4.69.135.186）
10 87.91 ae-3.ebr4.Washington1.Level3.net（4.69.132.93）
11 94.80 ae -94-94.csw4.Washington1.Level3.net（4.69.134.190）
12 86.40 ae-21-69.car1.Washington3.Level3.net（4.68.17.7）
13 185.10 AMAZONCOM.car1.Washington3.Level3.net（4.71 .204.18）
14 84.70 72.21.209.38 
15 85.73 72.21.193.37

16 85.68   166-49.amazon.com（207.171.166.49）已

完成Nmap：在20.57秒内扫描了1个IP地址（1个主机已启动）
```

## 例子3.4 使用whois查找www.target.com

```shell
> whois 207.171.166.49
[查询whois.arin.net] 
[whois.arin.net]机构名称

：Amazon.com，Inc.机构
ID：AMAZON-4
地址：605 5th Ave S
市：SEATTLE
州
省：WA邮政编码：98104
国家：美国
[.. 。]
```

在3.3中反向dns和traceroute发现 Amazon.com域名在使用该网站,说明很可能由亚马逊代理运行,且最后whois结果显示亚马逊为此IP持有者

如果Target邀请我们测试网站安全性,我们还需要亚马逊单独授权以触碰这段IP地址

也可以用Web数据库在给定域下查找主机名 例如Netcraft具备DNS搜索功能

Google也可以使用相关语法 site:target.com

## 针对知识产权的whois查询

当发现一小部分初始"种子IP"之后必须对其进行研究

此前查询到target.com发现的IP之一是 161.225.130.163

```shell
> whois 161.225.130.163
[查询whois.arin.net] 
[whois.arin.net]

机构
名称：Target Corporation机构ID：TARGET-14
地址：1000 Nicollet TPS 3165
城市：明尼阿波利斯
州州：MN
邮政编码：
55403
国家/地区：US 
NetRange：161.225.0.0-161.225 .255.255 
CIDR：161.225.0.0/16 
NETNAME：TARGETNET 
NetHandle：NET-161-225-0-0-1
家长：NET-161-0-0-0-0 
NETTYPE：直接分配
名称服务器：NS3.TARGET.COM
名称服务器：NS4.TARGET.COM
评论    ：RegDate 
：1993-03-04
更新：2005-11-02 

OrgTechHandle：DOMAI45-ARIN
OrgTechName：域名管理员
OrgTech电话：+ 1-612-696-2525 
OrgTech电子邮件：Domainnames.admin@target.com
```

毫不奇怪,target拥有一个巨大的B类IP段,161.255.-.- 

那么下一步我们可以从更高级查询开始

whois -h whois.arin.net \? 给出arin的查询语法

如果我们可以搜索并给定地址OrgID或OrgTechEmail匹配的所有网络块想必是极好的,但IP注册表通常不允许,但运势使用其他有用的查询

whois -h whois.arin.net @ target.com 显示所有ARIn联系人中邮件地址来自target.com的

whois -h whois.arin.net "n target * " 现已所有开头以netblock具柄target,不区分大小学

whois -h whois.arin.net "o target * " 显示以开头所有组织名称target

我们可以查找与每个条目相关的地址,电话和联系邮件
