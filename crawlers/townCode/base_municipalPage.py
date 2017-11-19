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

	def parse_town(self, url, params, target, target_kor, town_code=None, town_name=None):
		_sgg_list = get_json(url, params)['jsonResult']['body']
		for x in _sgg_list:
			if isinstance(x['CODE'], str): # if x['CODE'] is string type object...
				x['CODE'] = int(x['CODE'])

		_result = [dict(town_name=town_name, town_code=int(town_code), consti_list=_sgg_list)]

		print('\t└└  %s, %s(%d)...' % (target_kor+' 선거구 목록', town_name, len(_sgg_list)))
		return _result


class JSONCrawler_municipal(BaseCrawler_municipal):

	def city_codes(self): # 광역자치단체 code 리스트를 json으로 받게 됨.
		list_ = get_json(self.urlPath_city_codes, self.urlParam_city_codes)['jsonResult']['body']
		return [(x['CODE'], x['NAME']) for x in list_]

	def town_codes(self, city_code): # 특정 광역자치단체(city_code) 내의 시군구 code 리스트를 json으로 받게 됨.
		param_dict = copy.deepcopy(self.urlParam_town_list)
		param_dict['cityCode'] = city_code
		list_ = get_json(self.urlPath_town_list, param_dict)['jsonResult']['body']
		return [(x['CODE'], x['NAME']) for x in list_]

	def JSON_url_param(self, town_code): # 각 시군구별 선거구 code 리스트를 json으로 받을 URL의 parameter.
		param_dict = copy.deepcopy(self.urlParam_sgg_list)
		param_dict['townCode'] = town_code
		return param_dict

	def crawl(self):

		target = self.target
		target_kor = self.target_kor
		nth = self.nth

		# 광역자치단체 내의 기초자치단체 내의 선거구 데이터 크롤링의 기본과정.
		print("Waiting to connect http://info.nec.go.kr server (%s, %d)..." % (target, nth))

		every_result = [{'election_type':target,'nth':nth,'results':[]}]
		# 각 광역자치단체 별로 아래 단계를 수행.
		for city_code, city_name in self.city_codes():
			print('crawling %s election #%d - %s' % (target, self.nth, city_name))
			print('\t└  %s, %s(%d)...' % ('구시군 행정구역 목록', city_name, len(self.town_codes(city_code))))
			jobs = []
			# 광역자치단체(city_code) 내의 기초자치단체 별로 아래 단계를 수행.
			for town_code, town_name in self.town_codes(city_code):
				req_url = self.urlPath_sgg_list
				req_param = self.JSON_url_param(town_code)
				job = gevent.spawn(self.parse_town, req_url, req_param, target, target_kor, town_code, town_name)
				jobs.append(job)
			# 개별 기초자치단체 수행 끝.
			gevent.joinall(jobs)
			result_by_city = dict(city_name=city_name, city_code=int(city_code), town_list=flatten(job.get() for job in jobs))
			every_result[0]['results'].append(result_by_city)

		# 추가될 수도 있는 데이터 크롤링을 위해 next_crawler를 추가하는 내용.
		if hasattr(self, 'next_crawler'):
			next_result = self.next_crawler.crawl()
			every_result.extend(next_result)

		return every_result
