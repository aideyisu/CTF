#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2016-2018 Shuziguanxing (http://www.shuziguanxing.com/)
@Author: mO0n@guanxin
@Created: 2018-12-10 14:15
"""

import requests as req
from urlparse import urlparse, urljoin
import re

def parse_ip_port(url):
	'''将url格式数据转化成ip&port数据
	@param url string: URL
		url = https://x.x.x.x:8443
		url = https://x.x.x.x
		url = x.x.x.x
		url = x.x.x.x:80
	@return: (IP,Port)
	'''
	host = ''
	if '/' not in url:
		host = url
	else:
		if '://' not in url:
			host = host[:host.find('/')]
		else:
			host = urlparse(url).netloc
	
	if len(host) == 0:
		host = url
	
	if ":" in host:
		ip, port = host.split(":")
	else:
		ip = host
		# 预定义默认端口
		if 'https://' in url:
			port = 443
		elif 'http://' in url:
			port = 80
		else:
			port = 0
	
	return ip, int(port)


class web_spider():
	'''网页爬虫
	'''
	
	def get_link(self, url, file_exts = ['action', 'jsp', 'do', 'screen']):
		'''根据URL和扩展名获取符合条件的URL
		@param url string: 起始URL
		@param file_exts array: 允许爬取的URL对应的扩展名
		@return url or ''
		'''
		rnt = ''
		try:
			page_content = req.get(url, verify=False, timeout=3).content
			# print page_content
			# 根据后缀提取
			match = re.findall(r'''(?:href|action|src)\s*?=\s*?(?:"|')\s*?([^'"]*?\.(?:%s))''' % '|'.join(file_exts), page_content)
			# print match
			for item_url in match:
				if not item_url.startswith('http'):
					item_url = self.getAbsoluteURL(url, item_url)
					rnt = item_url
					break
				if self.is_url_exist(item_url):
					if self.isSameDomain(item_url, url):
						rnt = item_url
						break
					else:
						continue
			return rnt
		except Exception, e:
			# raise e
			return rnt

	def getAbsoluteURL(self, base, url):
		url1 = urljoin(base, url)
		return url1

	def is_url_exist(self, url):
		try:
			page_status_code = req.get(url,verify=False,timeout=3).status_code
			if int(page_status_code) != 404:
				return True
			else:
				return False
		except:
			return False

	def isSameDomain(self, url1, url2):
		try:
			if urlparse(url1).netloc.split(':')[0] == urlparse(url2).netloc.split(':')[0]:
				return True
			else:
				return False
		except Exception, e:
			return False
