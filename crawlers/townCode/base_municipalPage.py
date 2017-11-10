#!/usr/bin/env python3
# -*- coding=utf-8 -*-


import gevent
from gevent import monkey
import itertools
from urllib.parse import urljoin
import copy

from utils import flatten, get_json, get_xpath, parse_cell, sanitize, split, InvalidCrawlerError

monkey.patch_all()

class BaseCrawler_municipal(object):

	def parse_city(self, url, params, target, city_code=None, city_name=None):
		_elem_list = get_json(url, params)['jsonResult']['body']
		for x in _elem_list:
			if isinstance(x['CODE'], str): # if x['CODE'] is string type object...
				x['CODE'] = int(x['CODE'])

		_result = [dict(city_name=city_name, city_code=int(city_code), town_list=_elem_list)]
		_elemType_str = '기초자치단체 목록'

		print('crawled %s election #%d - %s, %s(%d)...' % (target, self.nth, _elemType_str, city_name, len(_elem_list)))
		return _result



	def parse_town(self, url, params, target, town_code=None, town_name=None):
		_elem_list = get_json(url, params)['jsonResult']['body']
		for x in _elem_list:
			if isinstance(x['CODE'], str): # if x['CODE'] is string type object...
				x['CODE'] = int(x['CODE'])

		_result = [dict(town_name=town_name, town_code=int(town_code), consti_list=_elem_list)]

		if target=='local_provincal_parliament':
			_elemType_str = '광역자치의회 지역구 목록'
		elif target=='local_municipal_parliament':
			_elemType_str = '기초자치의회 지역구 목록'
		else:
			raise InvalidCrawlerError(target, 'target', self.nth)
		print('crawled %s election #%d - %s, %s(%d)...' % (target, self.nth, _elemType_str, town_name, len(_elem_list)))
		return _result


class JSONCrawler_municipal(BaseCrawler_municipal):

	def city_codes(self): # 광역자치단체 code 리스트를 json으로 받게 됨.
		list_ = get_json(self.urlPath_city_codes, self.urlParam_city_codes)['jsonResult']['body']
		return [(x['CODE'], x['NAME']) for x in list_]

	def town_codes(self, city_code): # 특정 광역자치단체(city_code) 내의 기초자치단체 code 리스트를 json으로 받게 됨.
		param_dict = copy.deepcopy(self.urlParam_town_codes)
		param_dict['cityCode'] = city_code
		list_ = get_json(self.urlPath_town_codes, param_dict)['jsonResult']['body']
		return [(x['CODE'], x['NAME']) for x in list_]

	def JSON_url_param(self, town_code): # 각 기초자치단체별 선거구 code 리스트를 json으로 받을 URL의 parameter.
		param_dict = copy.deepcopy(self.urlParam_consti_list)
		param_dict['townCode'] = town_code
		return param_dict

	def crawl(self):

		target = self.target
		elemType = self.elemType #'constituency_in_municipal_division'
		nth = self.nth

		# 광역자치단체 내의 기초자치단체 내의 선거구 데이터 크롤링의 기본과정.
		print("Waiting to connect http://info.nec.go.kr server (%s)..." % elemType)

		every_result = [{'election_type':target,'element_type':elemType,'nth':nth,'results':[]}]
		# 각 광역자치단체 별로 아래 단계를 수행.
		for city_code, city_name in self.city_codes():
			jobs = []
			# 광역자치단체(city_code) 내의 기초자치단체 별로 아래 단계를 수행.
			for town_code, town_name in self.town_codes(city_code):
				req_url = self.urlPath_consti_list
				req_param = self.JSON_url_param(town_code)
				job = gevent.spawn(self.parse_town, req_url, req_param, target, town_code, town_name)
				jobs.append(job)
			# 개별 기초자치단체 수행 끝.
			gevent.joinall(jobs)
			result_by_city = dict(city_name=city_name, city_code=int(city_code), town_list=flatten(job.get() for job in jobs))
			every_result[0]['results'].append(result_by_city)

			print('crawled %s election #%d - %s, 광역자치단체 내 지역구 목록(%d)...' % (target, nth,  city_name, len(result_by_city['town_list'])))

		# 추가될 수도 있는 데이터 크롤링을 위해 next_crawler를 추가하는 내용.
		if hasattr(self, 'next_crawler'):
			prop_result = self.next_crawler.crawl()
			every_result.extend(prop_result)

		return every_result
