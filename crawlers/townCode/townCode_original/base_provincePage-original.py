#!/usr/bin/env python3
# -*- coding=utf-8 -*-


import gevent
from gevent import monkey
import itertools
from urllib.parse import urljoin
import copy

from utils import flatten, get_json, get_xpath, parse_cell, sanitize, split

monkey.patch_all()

class BaseCrawler_province(object):

	def parse_city(self, url, params, target, elemType, city_code=None, city_name=None):
		_elem_list = get_json(url, params)['jsonResult']['body']
		for x in _elem_list:
			if isinstance(x['CODE'], str): # if x['CODE'] is string type object...
				x['CODE'] = int(x['CODE'])

		if elemType == 'local_division':
			_result = [dict(city_name=city_name, city_code=int(city_code), town_list=_elem_list)]
			_elemType_str = '행정구역(기초자치단체, 행정구) 목록'

		else: #elemType == 'constituency_in_province'
			_result = [dict(city_name=city_name, city_code=int(city_code), consti_list=_elem_list)]
			if target=='assembly':
				_elemType_str = '국회의원 지역구 목록'
			elif target=='local_eduParliament':
				_elemType_str = '교육의원(광역자치의회) 지역구 목록'
			else:
				raise InvalidCrawlerError(target, elemType, nth)

		print('crawled %s election #%d - %s, %s(%d)...' % (target, self.nth, _elemType_str, city_name, len(_elem_list)))
		return _result


class JSONCrawler_province(BaseCrawler_province):

	def city_codes(self): # 광역자치단체 code 리스트를 json으로 받게 됨.
		list_ = get_json(self.urlPath_city_codes, self.urlParam_city_codes)['jsonResult']['body']
		return [(x['CODE'], x['NAME']) for x in list_]

	def JSON_url_param(self, elemType, city_code): # 각 광역자치단체별 선거구/기초자치단체 code 리스트를 json으로 받을 URL의 parameter.
		if elemType == 'local_division':
			param_dict = copy.deepcopy(self.urlParam_town_list)
		else: # elemType == 'constituency_in_province'
			param_dict = copy.deepcopy(self.urlParam_sgg_list)
		param_dict['cityCode'] = city_code
		return param_dict

	def crawl(self):

		jobs = []
		target = self.target
		elemType = self.elemType # 'local_division' or 'constituency_in_province'
		nth = self.nth

		# 광역자치단체 단위 페이지의 데이터 크롤링의 기본과정.
		print("Waiting to connect http://info.nec.go.kr server (%s)..." % elemType)
		for city_code, city_name in self.city_codes(): # 각 광역자치단체 별로 아래 단계를 수행.
			if elemType == 'local_division':
				req_url = self.urlPath_town_list
			else: #elemType == 'constituency_in_province'
				req_url = self.urlPath_sgg_list
			req_param = self.JSON_url_param(elemType, city_code)
			job = gevent.spawn(self.parse_city, req_url, req_param, target, elemType, city_code, city_name)
			jobs.append(job)
		gevent.joinall(jobs)
		every_result = [{'election_type':target,'element_type':elemType,'nth':nth,'results':flatten(job.get() for job in jobs)}]

		# 추가될 수도 있는 데이터 크롤링을 위해 next_crawler를 추가하는 내용.
		if hasattr(self, 'next_crawler'):
			next_result = self.next_crawler.crawl()
			every_result.extend(next_result)

		return every_result
