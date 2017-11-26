#!/usr/bin/env python3
# -*- coding=utf-8 -*-


############### is constituency in parse!


import gevent
from gevent import monkey
import itertools
from urllib.parse import urljoin
import copy

from utils import flatten, get_json, get_xpath, parse_cell, sanitize, split

monkey.patch_all()

class BaseCrawler(object):

	def parse(self, url, params):
		_party_list = get_json(url, params)['jsonResult']['body'] # 정당 code json을 받음.
		for i in range(int(len(_party_list))):
			x = _party_list[i]
			x['code_thisElec'] = i+1 # 각 정당별 '기호'(순번)을 매겨줌.
			if isinstance(x['CODE'], str): # if x['CODE'] is string type object...
				x['CODE'] = int(x['CODE'])

		print('crawled %s election #%d - 선거참여 정당, 전국(%d)...' % (self.target_eng, self.nth, len(_party_list)))
		return _party_list


class JSONCrawler(BaseCrawler):

	def crawl(self):
		target = self.target
		target_eng = self.target_eng
		jobs = []

		print("Waiting to connect http://info.nec.go.kr server (%s)..." % target_eng)
		req_url = self.urlPath_party_codes
		req_param = self.urlParam_party_codes
		job = self.parse(req_url, req_param)
		every_result = [{'election_type':target,'town_type':"전국",'nth':self.nth,'results':job}]

		return every_result
