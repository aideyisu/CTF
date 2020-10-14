## SSRF

SSRF server-side-request-forgery 服务端请求伪造

由攻击者构造,服务端发起的攻击行为

## 危害

1 敏感信息泄漏

2 造成内网攻击

3 被当作跳板机持续攻击

## 环境部署

```
docker pull registry.cn-shanghai.aliyuncs.com/yhskc/chatsys
docker run -d -p 0.0.0.0:80:80 registry.cn-shanghai.aliyuncs.com/yhskc/chatsys
```

## 具体使用

http://xforburp.com

访问上述地址,使用ssrf配合burpsuite食用
