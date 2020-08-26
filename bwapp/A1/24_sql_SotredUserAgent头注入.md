# User-Agent HTTP注入

## 检测

按照题目提示,直接BrupSuite抓包修改User-Agent即可修改

low medium high 都可以实现

说明都可以,接下来测试sql注入

直接修改数据包为 ' 会返回

```
Error: You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near '''')' at line 1
```

可以看到需要闭合括号,测试 ')# 此时可以返回空数据集

开心~  接下来我们可以开始注入

111','222'); #

在第二部分输入sql语句即可

## 结语

我在这里属实脑瘫,之前把这道题源码改了,现在完全没有印象,导致试了好久都不行...一看源码是自己改完没改回来...太难了

