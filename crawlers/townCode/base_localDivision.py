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

	def parse_city(self, url, params, target, city_code=None, city_name=None):
		_elem_list = get_json(url, params)['jsonResult']['body']
		for x in _elem_list:
			if isinstance(x['CODE'], str): # if x['CODE'] is string type object...
				x['CODE'] = int(x['CODE'])

		_result = [dict(city_name=city_name, city_code=int(city_code), town_list=_elem_list)]

		_elemType = '행정구역(기초자치단체 및 행정구) 목록'
		print('crawled %s election #%d - %s, %s(%d)...' % (target, self.nth, _elemType, city_name, len(_elem_list)))
		return _result


class JSONCrawler_division(BaseCrawler_division):

	def city_codes(self): # 광역자치단체 code 리스트를 json으로 받게 됨.
		list_ = get_json(self.urlPath_city_codes, self.urlParam_city_codes)['jsonResult']['body']
		return [(x['CODE'], x['NAME']) for x in list_]

	def town_url_param(self, city_code): # 각 광역자치단체별 기초자치단체/선거구 code 리스트를 json으로 받게 됨.
		param_dict = copy.deepcopy(self.urlParam_town_list)
		param_dict['cityCode'] = city_code
		return param_dict

	def crawl(self):

		jobs = []
		target = self.target
		elemType = "localDivision" #행정구역

		# 광역 및 기초자치단체 행정구역 데이터 크롤링의 기본과정.
		print("Waiting to connect http://info.nec.go.kr server (%s)..." % elemType)
		for city_code, city_name in self.city_codes(): # 각 광역자치단체 별로 아래 단계를 수행.
			req_url = self.urlPath_town_list
			req_param = self.town_url_param(city_code)
			job = gevent.spawn(self.parse_city, req_url, req_param, target, city_code, city_name)
			jobs.append(job)
		gevent.joinall(jobs)
		every_result = [{'election_type':target,'element_type':elemType,'nth':self.nth,'results':flatten(job.get() for job in jobs)}]

		# 추가될 수도 있는 선거구-constituency 데이터 크롤링을 위해 추가하는 내용.
		if hasattr(self, 'consti_crawler'):
			prop_result = self.consti_crawler.crawl()
			every_result.extend(prop_result)

		return every_result
