# sql Stored Blog

## 测试

这里是典型XSS注入,我们会向内部添加存储例如alert(1) 让页面弹窗

我们可以直接尝试 

<script>alert(1)</script>

发现就可以直接输出弹
