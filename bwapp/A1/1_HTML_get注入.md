# HTML_Get注入

## low

#### 测试

输入两个名字会在下方返回结果

#### 学习

HTML注入顾名思义,就是使用HTML将原有页面生成逻辑破坏,所以我们可以在对应位置嵌入HTML或JS代码达到目的

```
<a href=www.aideyisu.com>我的博客</a>

<script>alert(document.cookie)</script>
```

# 源码分析

```php
<?php

if(isset($_GET["firstname"]) && isset($_GET["lastname"]))
{

    $firstname = $_GET["firstname"];
    $lastname = $_GET["lastname"];

    if($firstname == "" or $lastname == "")
    {

        echo "<font color=\"red\">Please enter both fields...</font>";

    }

    else
    {

        echo "Welcome " . htmli($firstname) . " " . htmli($lastname);

    }

}

?>
```

直接获取了两个名称,并echo

当安全级别为low时没有检测

## medium

#### 测试

按照low级别的方法尝试发现将输入转化为字符串原样输出了Otz

#### 分析

直接进入源码分析
```php
// Converts only "<" and ">" to HTLM entities
$input = str_replace("<", "&lt;", $data);
$input = str_replace(">", "&gt;", $input);

// Failure is an option
// Bypasses double encoding attacks
// <script>alert(0)</script>
// %3Cscript%3Ealert%280%29%3C%2Fscript%3E
// %253Cscript%253Ealert%25280%2529%253C%252Fscript%253E
$input = urldecode($input);

return $input;
```

发现这里使用了字符串替换随后url编码,因此我们可以使用字符URl编码

我在这里使用了在线url编码,<h1>test</h1>
https://tool.oschina.net/encode?type=4

编码后效果为 %3Ch1%3Etest%3C/h1%3E%20

再次尝试发现可以正常显示


## high

尝试发现此前的方法输入会被以纯文本的形式输出

我们首先可以查看源代码
```php
function xss_check_3($data, $encoding = "UTF-8")
{

    // htmlspecialchars - converts special characters to HTML entities
    // '&' (ampersand) becomes '&amp;'
    // '"' (double quote) becomes '&quot;' when ENT_NOQUOTES is not set
    // "'" (single quote) becomes '&#039;' (or &apos;) only when ENT_QUOTES is set
    // '<' (less than) becomes '&lt;'
    // '>' (greater than) becomes '&gt;'

    return htmlspecialchars($data, ENT_QUOTES, $encoding);

}
```

我们可以看到此处调用了php基础方法htmlspecialchars将五种符号转化为了HTML实体

参数ENT_QUOTES会编码双引号和单引号

在上网穿越各种资料后,此处high为安全
