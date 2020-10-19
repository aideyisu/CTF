# Chapter 1. Getting Started with Nmap

最简单例子 1.1 nmap针对IP地址进行扫描

nmap -sL 6.209.24.0/24 6.207.0.0/22

```shell
felix> nmap -sL 6.209.24.0/24 6.207.0.0/22

Starting Nmap ( http://nmap.org )
Nmap scan report for 6.209.24.0
Nmap scan report for fw.corp.avataronline.com (6.209.24.1)
Nmap scan report for dev2.corp.avataronline.com (6.209.24.2)
Nmap scan report for 6.209.24.3
Nmap scan report for 6.209.24.4
...
Nmap scan report for dhcp-21.corp.avataronline.com (6.209.24.21)
Nmap scan report for dhcp-22.corp.avataronline.com (6.209.24.22)
Nmap scan report for dhcp-23.corp.avataronline.com (6.209.24.23)
...
Nmap scan report for 6.207.0.0
Nmap scan report for gw.avataronline.com (6.207.0.1)
Nmap scan report for ns1.avataronline.com (6.207.0.2)
Nmap scan report for ns2.avataronline.com (6.207.0.3)
Nmap scan report for ftp.avataronline.com (6.207.0.4)
Nmap scan report for 6.207.0.5
Nmap scan report for 6.207.0.6
Nmap scan report for www.avataronline.com (6.207.0.7)
Nmap scan report for 6.207.0.8
...
Nmap scan report for cluster-c120.avataronline.com (6.207.2.120)
Nmap scan report for cluster-c121.avataronline.com (6.207.2.121)
Nmap scan report for cluster-c122.avataronline.com (6.207.2.122)
...
Nmap scan report for 6.207.3.255
Nmap done: 1280 IP addresses (0 hosts up) scanned in 331.49 seconds
felix>
```

直接可以看结果,felix发现了具有反向dns的机器

这些结果可以使得Felix可以大致了解正在使用的机器数量与状况

随后felix做好了准备,尝试进行端口扫描

使用nmap来尝试确定网络上侦听的每个服务应用程序和版本号

还想通过一系列成为OS指纹识别的TCP/IP探测来猜测远程操作系统

felix还对AO管理员是否注意到这些公然扫描很感兴趣,经过一番考虑，Felix选择了这个指令

例子1.2

nmap -sS -p- -PE -PP -PS80,443 -PA3389 -PU40125 -A -T4 -oA avatartcpscan-％D 6.209.24.0/24 6.207.0.0/22

解释 
```
-sS TCP扫描 
-p- 1-65535全部端口 
-PE -PP -PS80,443 -PA3389 -PU40125 以上主机发现技术一起使用
-A 打开一个先进适用和一个操作系统+服务检测 在此处等效于 -sV -sC -O --traceroute(版本检测,具有默认脚本集的nmap脚本引擎,远程OS检测,traceroute)
-T4 时间序列调整到affressive级别(第4个,总共五个) 等价于 -T aggressive,但是更加一如键入和拼写 在网络连接合理快速可靠时推荐使用
-oA avatartcpscan-%D 以每种格式（普通,XML,可重复）将结果输出到文件扩展名为.nmap .xml .gnmap的文件中 所有输出格式都包括了日期时间 但Felix喜欢唉文件名中明确注明日期.正常输出和错误仍会发送到stdout中 
6.209.24.0/24 6.207.0.0/22 IP网段,CIDR形式及更多
```

测试结果

```shell
Nmap scan report for fw.corp.avataronline.com (6.209.24.1)
(The 65530 ports scanned but not shown below are in state: filtered)
PORT     STATE  SERVICE    VERSION
22/tcp   open   ssh        OpenSSH 3.7.1p2 (protocol 1.99)
| ssh-hostkey: 1024 7c:14:2f:92:ca:61:90:a4:11:3c:47:82:d5:8e:a9:6b (DSA)
|_2048 41:cf7d:839d:7f66:0ae1:8331:7fd4:5a97:5a (RSA)
|_sshv1: Server supports SSHv1
53/tcp   open   domain     ISC BIND 9.2.1
110/tcp  open   pop3       Courier pop3d
113/tcp  closed auth
143/tcp  open   imap       Courier Imap 1.6.X - 1.7.X
3128/tcp open   http-proxy Squid webproxy 2.2.STABLE5
Device type: general purpose
Running: Linux 2.4.X|2.5.X
OS details: Linux Kernel 2.4.0 - 2.5.20
Uptime 3.134 days
```

Felix首先记录了反向dns的名称,显然检测到的是某公司网络的防火墙

第一个端口是ssh端口 发现了版本,并且发现支持安全性很低的SSHv1协议.Felix记录下了尝试对服务器使用Ncrack暴力身份破解程序

还有53断后在运行ISC BIND,具有可远程利用安全漏洞的悠久历史.Felix可能会尝试使用区域传入请求和侵入式查询从非重要服务器中搜集重要信息;也可能会尝试缓存投毒,通过欺骗下载服务器,诱惑毫无戒心的内部客户端用户运行木马,从而为Felix提供位于防火墙后面的完整网络访问权限

110(POP3)和143(IMAP).他们之间的113为close状态.POP3和ICMP是邮件检索服务,和BIND一样,在此服务器上没有合法位置.这存在风险,它们通常传输未经加密的邮件和身份验证凭证.Felix将尝试对这些服务进行用户枚举和密码猜测攻击,这可能比针对SSH更加有效

最后还开放了代理功能,这不应该可以被外部访问,Felix将测试这能否可以滥用到此代码连接到因特网的其他站点(垃圾邮件发送者和恶意黑客经常以这种方式来使用代理隐藏踪迹)Felix将尝试代理自己的方式进入内网

## 例子1.3 另一个有趣的OA机器

```shell
Nmap scan report for dhcp-23.corp.avataronline.com (6.209.24.23)
(The 65526 ports scanned but not shown below are in state: closed)
PORT      STATE    SERVICE       VERSION
135/tcp   filtered msrpc
136/tcp   filtered profile
137/tcp   filtered netbios-ns
138/tcp   filtered netbios-dgm
139/tcp   filtered netbios-ssn
445/tcp   open     microsoft-ds  Microsoft Windows XP microsoft-ds
1002/tcp  open     windows-icfw?
1025/tcp  open     msrpc         Microsoft Windows msrpc
16552/tcp open     unknown
Device type: general purpose
Running: Microsoft Windows NT/2K/XP
OS details: Microsoft Windows XP Professional RC1+ through final release

Host script results:
|_nbstat: NetBIOS name: TRACYD, NetBIOS user: <unknown>,  NetBIOS MAC: 00:20:35:00:29:a2:7f (IBM)
|_smbv2-enabled: Server doesn't support SMBv2 protocol
| smb-os-discovery:  
|   OS: Windows XP (Windows 2000 LAN Manager)
|_  Name: WORKGROUP\JOHND
```

Felix笑开了花当发现XP系统,有一堆MS RPC漏洞,如果操作系统补丁不是最新的,那就很难摆脱损害

它们尝试在135-139专门阻止它们认为危险的Windows端口,445和1025是本次扫描的两个例子,虽然nmap没办法是被16552,但是Felix已经看到这个端口,足以通过经验推断可能为MS Messenger Service

Felix仔细研究结果,以发现可以利用的漏洞来危害网络.在生产环境中，看到gw.avataronline.com是一台思科路由器,并充当来系统基本防火墙.

它们仅阻断特权端口(小于1024),从而使该网络上可以访问大量容易受到攻击的服务.

名称各异的计算机具有数十个nmap无法识别的端口,它们可能是AO的自定义守护程序.

www.avataronline.com是一个Linux机器,在HTTP和HTTPS端口上具有开放的Apache服务器,不幸的是它与OpenSSL库的可利用版本链接在一起.

在太阳下山之前，Felix已获得对公司网络和生产网络上主机的特权访问(QAQ太厉害了)

在下一行享受另外两个逗比故事

https://nmap.org/book/nmap-overview-and-demos.html

其余部分都是在说一些不重要的东西
