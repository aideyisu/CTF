# Java Web 介绍

MVC架构

v - view 页面渲染

m - model中间类

c - controller

后端再放一个DB

#### 发展历程

Applets -> Servlet -> Jsp -> Structs1 -> Structs2|JSP -> Spring MVC -> Spring Boot -> Spring Microservices

各有各自的苦

Applets Java 支持的网页,有用户类

Servlet java编写的服务器程序,动态生成Web内容,没有用户类

JSP Java Server Pages 本质也是Servlet,JSP会自动编译生成报文最终,但是版本变动不太好

Structs1 初次MVC提出,2004年,侵入型框架，严重依赖自己API

Structs2 JSF 

Spring MVC 最受欢迎,但是配置复杂

Spring Boot 约定大于配置,简化配置,但是大型项目更新慢

Spring Microservices 微服务,优化大型项目更新部署时间

#### java web 代码审计

防御性编程,减少错误

###### 审计方式

先创建一个核心问题清单,包括安全漏洞,身份验证问题

授权问题,内存泄漏,不良设计习惯之类问题

跟踪用户输入数据和敏感函数参数回溯最常用





