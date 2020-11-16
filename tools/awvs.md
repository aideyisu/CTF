# Acunetix Web Vulnerability Scanner（AWVS）

经典漏扫工具

#### Docker安装

```shell
#  pull 拉取下载镜像
docker pull secfa/docker-awvs

#  将Docker的3443端口映射到物理机的 13443端口
docker run -it -d -p 13443:3443 secfa/docker-awvs

# 容器的相关信息
awvs13 username: admin@admin.com
awvs13 password: Admin123
AWVS版本：13.0.200217097

# 后续访问 
https://127.0.0.1:13443/#/about
```

开箱即用,不过要是想舒服还是配一下证书
