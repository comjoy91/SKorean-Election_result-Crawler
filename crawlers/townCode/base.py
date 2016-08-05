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

	def parse(self, url, params, is_constituency, city_code=None, city_name=None):
		_town_list = get_json(url, params)['jsonResult']['body']
		for x in _town_list:
			if isinstance(x['CODE'], str): # if x['CODE'] is string type object...
				x['CODE'] = int(x['CODE'])

		_result = [dict(city_name=city_name, city_code=int(city_code), town_list=_town_list)]

		_townType = '지역구' if is_constituency else '시군구(기초자치단체)'
		print('crawled #%d - %s, %s(%d)...' % (self.nth, _townType, city_name, len(_town_list)))
		return _result


class MultiCityCrawler(BaseCrawler):

	def city_codes(self):
		list_ = get_json(self.url_city_codes_json, self.param_city_codes_json)['jsonResult']['body']
		return [(x['CODE'], x['NAME']) for x in list_]

	def url_param(self, city_code):
		param_dict = copy.deepcopy(self.param_url_list)
		param_dict['cityCode'] = city_code
		return param_dict

	def crawl(self):
		# 지역구 대표
		jobs = []
		is_constituency = self.is_constituency
		if is_constituency:
			townType = "constituency"
		else:
			townType = "basicLocal"

		print("Waiting to connect http://info.nec.go.kr server (%s)..." % townType)
		for city_code, city_name in self.city_codes():
			req_url = self.url_list_base
			req_param = self.url_param(city_code)
			job = gevent.spawn(self.parse, req_url, req_param, is_constituency, city_code, city_name)
			jobs.append(job)
		gevent.joinall(jobs)
		every_result = [{'town_type':townType,'nth':self.nth,'results':flatten(job.get() for job in jobs)}]

		# 비례대표
		if hasattr(self, 'prop_crawler'):
			prop_result = self.prop_crawler.crawl()
			every_result.extend(prop_result)

		return every_result

class SinglePageCrawler(BaseCrawler):

	def crawl(self):
		people = self.parse(self.url_list)
		return people
