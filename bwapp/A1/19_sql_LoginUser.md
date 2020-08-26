# sql Loging User 

## 测试

既然是user登录,我们直接输入自己的用户名密码发现可以正常登录

还会提示 Your secret: 11111

肯定是判断用户是否存在随后判断密码是否正确

测试order by 失败,因为只有当密码也正确的是否才会显示信息

https://blog.csdn.net/angry_program/article/details/104545171#0x07%E3%80%81SQL%20Injection%20(Login%20Form%2FUser)

看博客也都是针对源码分析才知道可以使用

```
login=' and 0 UNION SELECT 1,2,'356a192b7913b04c54574d18c28d46e6395428ab',4,5,6,7,8,9#
&password=1
&form=submit
```

这样的操作,其他方法都是sqlmap直接跑,直接手动应该是不太行...
