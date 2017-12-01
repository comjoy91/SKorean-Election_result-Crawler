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

	def parse_city(self, url, params, target, target_kor, nth, city_code=None, city_name=None):
		_town_list = get_json(url['town'], params['town'])['jsonResult']['body']
		_town_dict = dict()
		if (target=='president' and nth <= 15) or \
			(target=='assembly' and nth <= 16) or \
			(target=='local-ma' and nth <= 3) or \
			(target=='local-mp' and nth <= 3) or \
			(target=='local-pa' and nth <= 3) or \
			(target=='local-pp' and nth <= 3):
			for x in _town_list:
				x['CODE'] = int(x['CODE'])
				if x['CODE'] < 10000:
					_town_dict[x['NAME']] = x['CODE']*10 + 3
				else:
					_town_dict[x['NAME']] = x['CODE']
		else:
			for x in _town_list:
				x['CODE'] = int(x['CODE'])
				_town_dict[x['NAME']] = x['CODE']

		_sgg_list = get_json(url['sgg'], params['sgg'])['jsonResult']['body']
		_sgg_dict = dict()
		for x in _sgg_list:
			x['CODE'] = int(x['CODE'])
			if not x['NAME'] in _sgg_dict:
				_sgg_dict[x['NAME']] = []
			_sgg_dict[x['NAME']].append(x['CODE'])

		_PR_sgg_dict = dict()
		if 'PR_sgg' in params:
			_PR_sgg_list = get_json(url['sgg'], params['PR_sgg'])['jsonResult']['body']
			for x in _PR_sgg_list:
				if not x['NAME'] in _PR_sgg_dict:
					_PR_sgg_dict[x['NAME']] = []
				_PR_sgg_dict[x['NAME']].append(x['CODE'])

		_result = [dict(city_name=city_name, city_code=int(city_code), town_list=_town_list, town_dict=_town_dict)]
		if len(_sgg_list) > 0:
			_result[0]['consti_list'] = _sgg_list
			_result[0]['consti_dict'] = _sgg_dict
		if len(_PR_sgg_dict) > 0:
			_result[0]['PR_consti_list'] = _PR_sgg_list
			_result[0]['PR_consti_dict'] = _PR_sgg_dict

		print('crawled %s election #%d - %s' % (target, self.nth, city_name))
		print('\t└  %s, %s(%d)...' % ('구시군 행정구역 목록', city_name, len(_town_dict)))
		if len(_PR_sgg_dict) > 0:
			print('\t└  %s, %s(%d)...\n' % (target_kor+' 비례대표 선거구(자치구시군) 목록', city_name, len(_PR_sgg_dict)))
		print('\t└  %s, %s(%d)...\n' % (target_kor+' 선거구 목록', city_name, len(_sgg_dict)))

		return _result


class JSONCrawler_province(BaseCrawler_province):

	def city_codes(self): # 광역자치단체 code 리스트를 json으로 받게 됨.
		list_ = get_json(self.urlPath_city_codes, self.urlParam_city_codes)['jsonResult']['body']
		return [(x['CODE'], x['NAME']) for x in list_]

	def JSON_url_param(self, city_code): # 각 광역자치단체별 기초자치단체 code 리스트를 json으로 받을 URL의 parameter.
		param_dict = dict(town=copy.deepcopy(self.urlParam_town_list), sgg=copy.deepcopy(self.urlParam_sgg_list))
		param_dict['town']['cityCode'] = city_code
		param_dict['sgg']['cityCode'] = city_code
		if hasattr(self, 'urlParam_PR_sgg_list'):
			param_dict['PR_sgg'] = copy.deepcopy(self.urlParam_PR_sgg_list)
			param_dict['PR_sgg']['cityCode'] = city_code

		if self.target=='assembly' and self.nth==17:
			param_dict['sgg']['cityCode'] = city_code+'00'
		return param_dict

	def crawl(self):

		jobs = []
		target = self.target
		target_eng = self.target_eng
		target_kor = self.target_kor
		nth = self.nth
		req_url = dict(town=self.urlPath_town_list, sgg=self.urlPath_sgg_list)

		# 광역자치단체 단위 페이지의 데이터 크롤링의 기본과정.
		print("Waiting to connect http://info.nec.go.kr server (%s, %d-th)..." % (target_eng, nth))
		for city_code, city_name in self.city_codes(): # 각 광역자치단체 별로 아래 단계를 수행.
			req_param = self.JSON_url_param(city_code)
			job = gevent.spawn(self.parse_city, req_url, req_param, target, target_kor, nth, city_code, city_name)
			jobs.append(job)
		gevent.joinall(jobs)
		every_result = [{'election_type':target,'nth':nth,'results':flatten(job.get() for job in jobs)}]

		# 추가될 수도 있는 데이터 크롤링을 위해 next_crawler를 추가하는 내용.
		if hasattr(self, 'next_crawler'):
			next_result = self.next_crawler.crawl()
			every_result.extend(next_result)

		return every_result
