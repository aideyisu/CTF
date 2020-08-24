# Mail头注入

# low

先正常填写信息然后通过remarks中内容修改使得邮件正常发送

将name=Joe Bloggs修改为

name=Attacker\nbcc: spam@victim.com

通过插入换行符并附加了一个电子邮件地址的密码STMP标头,SMTP服务器将向BCC发送电子邮件

可以通过这种策略匿名大量信息,这个漏洞并不局限于php.可能会影响任何基于用户输入发送电子邮件的应用程序


