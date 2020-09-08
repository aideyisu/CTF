# OS 命令注入

## low

看题解给定域名会返回dns信息,但是docker环境没有安装nslookup,导致源码中 shell_exec("nslookup  " . xxx) 失败

所以我们需要先进入docker容器中安装一下nslookup才能正常从第一步开始做题

```shell
apt-get install dnsutils
```

shell_exec通过shell环境执行命令并将结果以字符串形式返回

# 突发奇想

第一次做题有思路.

直接使用linux中命令链接符号

```
www.nsa.gov;whoami
```

发现返回结果末尾带了www-data即为当前用户

再尝试其他语句

```
whois.nsa.gov|whoami
```

可以只返回 www-data

类似的我们还可以使用

```
www.nsa.gov&whoami 
```

也可以完成这个任务

# 警告

直接 ;ls 会把环境搞崩 =.=

直接重启就好 docker restart xxx

## medium

再次尝试使用low 指令 

成功指令 |

失败指令 ; & &&

## high

使用了escapeshellcmd 过滤了一堆字符,所以误无解

## 拓展阅读 - Linux一行执行多指令

1 管道符 |

2 分号 ;

3 语句连续执行 &

4 与门 &&

5 非门 ||

## 推荐软件

commix 系统命令注入漏洞测试工具
