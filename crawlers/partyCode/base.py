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
		_party_list = get_json(url, params)['jsonResult']['body']

		print('crawled #%d - %s, %s(%d)...' % (self.nth, '선거참여 정당', '전국', len(_party_list)))
		return _party_list


class MultiCityCrawler(BaseCrawler):

	def url_param(self):
		return self.param_url_list

	def crawl(self):
		# 지역구 대표
		jobs = []

		print("Waiting to connect http://info.nec.go.kr server (%s)..." % 'partyList')
		req_url = self.url_list_base
		req_param = self.url_param()
		job = self.parse(req_url, req_param)
		every_result = [{'town_type':"전국",'nth':self.nth,'results':job}]

		return every_result

class SinglePageCrawler(BaseCrawler):

	def crawl(self):
		people = self.parse(self.url_list)
		return people
