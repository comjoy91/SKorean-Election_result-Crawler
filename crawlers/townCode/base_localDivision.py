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

class BaseCrawler_division(object):

	def parse(self, url, params, target, city_code=None, city_name=None):
		_town_list = get_json(url, params)['jsonResult']['body']
		for x in _town_list:
			if isinstance(x['CODE'], str): # if x['CODE'] is string type object...
				x['CODE'] = int(x['CODE'])

		_result = [dict(city_name=city_name, city_code=int(city_code), town_list=_town_list)]

		_townType = '행정구역(기초자치단체 및 행정구) 목록'
		print('crawled %s election #%d - %s, %s(%d)...' % (target, self.nth, _townType, city_name, len(_town_list)))
		return _result


class JSONCrawler_division(BaseCrawler_division):

	def city_codes(self): # 광역자치단체 code 리스트를 json으로 받게 됨.
		list_ = get_json(self.url_city_codes_json, self.param_city_codes_json)['jsonResult']['body']
		return [(x['CODE'], x['NAME']) for x in list_]

	def url_param(self, city_code): # 각 광역자치단체별 기초자치단체/선거구 code 리스트를 json으로 받게 됨.
		param_dict = copy.deepcopy(self.param_url_list)
		param_dict['cityCode'] = city_code
		return param_dict

	def crawl(self):

		jobs = []
		target = self.target
		townType = "localDivision" #행정구역

		# 기초자치단체 데이터 크롤링의 기본과정.
		print("Waiting to connect http://info.nec.go.kr server (%s)..." % townType)
		for city_code, city_name in self.city_codes():
			req_url = self.url_list_base
			req_param = self.url_param(city_code)
			job = gevent.spawn(self.parse, req_url, req_param, target, city_code, city_name)
			jobs.append(job)
		gevent.joinall(jobs)
		every_result = [{'election_type':target,'town_type':townType,'nth':self.nth,'results':flatten(job.get() for job in jobs)}]

		# 추가될 수도 있는 선거구-constituency 데이터 크롤링을 위해 추가하는 내용.
		if hasattr(self, 'consti_crawler'):
			prop_result = self.consti_crawler.crawl()
			every_result.extend(prop_result)

		return every_result
