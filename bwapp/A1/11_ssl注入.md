# ssl注入

在docker里直接使用的话会提醒

The requested URL /ssii.shtml was not found on this server.

进入容器寻找

```shell
find / -name "ssii.shtml"
```

也没有这个文件

暂且认为这道题目docker封装有点问题,跳过
