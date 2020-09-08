# HTML url注入

## low

我们尝试直接使用 ?<h1>test</h1> 写到路径后面,发现被字符化了

#### 修改IP
上网看了一下,这道题目就是用BurpSuite抓包修改一下Host就可以的题目

所以我们直接抓包,将Host字段修改为test 发现test顶替了原本ip的位置

#### XSS弹窗
/htmli_current_url.php?<script>alert(123)</script>

通过BurpSuite在HTTP头直接添加,成功弹窗

#### h1显示

通过BurpSuite,将浏览器URL编码后的文字复原为<h1>test</h1>恢复显示

## medium

修改IP失效

h1显示也失败

弹窗也失败

看网上说中等此处无法绕过

## high

此处看源码还是 xss_check_3 失望而返
