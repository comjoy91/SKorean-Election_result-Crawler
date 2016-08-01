#!/usr/bin/env python3
# -*- coding=utf-8 -*-


############### is proportional in parse!


import gevent
from gevent import monkey
import itertools
from urllib.parse import urljoin

from utils import flatten, get_json, get_xpath, parse_cell, sanitize, split

monkey.patch_all()

class BaseCrawler(object):
	url_image_base = 'http://info.nec.go.kr'

	attrs = []
	attrs_district = ['district', 'towns', 'pollPlaces', 'population', 'electorates', 'pop_elec_ratio', 'households']
	attrs_result = ['name', 'vote']
	attrs_exclude_parse_cell = ['image', 'cand_no', 'result']


	def parse_proportional(self, url, city_name=None): #지금 이건 비례대표만 해당하는 거임 ㅇㅇㅇㅇㅇ
		tr_list = get_xpath(url, '//tr')
		thead_list = get_xpath(url, '//th')
		td_columns = len(tr_list[1])

		consti_list = []

		for i in range(len(tr_list)):
			if len(tr_list[i]) < 2:
				pass
			elif tr_list[i][0].get('rowspan') == None: # 선거구명 자리의 rowspan이 지정되지 않았다 == 맨 왼쪽칸을 보고 있는 게 아니다.
				pass
			else:
				district = tr_list[i][0] # 여기 저장되는 district 이름은 선거구 단위의 기초자치단체명임 ㅇㅇ. ex. <td rowspan="3" class="firstTd alignL">중구동구</td>
				towns = tr_list[i][1] # 읍면동수 ex. <td rowspan="3" class=alignR>23</td>
				pollPlaces = tr_list[i][2] # 투표구수 ex. <td rowspan="3" class=alignR>52</td>
				population = tr_list[i][3] # ex. <td rowspan="3" class=alignR>148,789<br/>(174 , 0)</td>
				electorates = tr_list[i][td_columns-3] # ex. <td class=alignR>127,836<br/>(163 , 0)</td>
				pop_elec_ratio = tr_list[i][td_columns-2] # 선거인수/인구수 비율 ex. <td rowspan="3" class=alignR>85.9</td>
				households = tr_list[i][td_columns-1] # 세대수 ex. <td rowspan="3" class=alignR>67,548<br/>(172 , 0)</td>

				district_info = (district, towns, pollPlaces, population, electorates, pop_elec_ratio, households)
				district_info = dict(list(zip(self.attrs_district, district_info)))
				consti_list.append(district_info)

		consti_list = [self.parse_consti(consti, city_name=city_name) for consti in consti_list]
		print(('crawled #%d - %s, %s(%d)...' % (self.nth, '비례대표', city_name, len(consti_list))))
		return consti_list


	def parse_constituency(self, url, city_name=None): #지금 이건 지역구만 해당하는 거임 ㅇㅇㅇㅇㅇ
		tr_list = get_xpath(url, '//tr')
		thead_list = get_xpath(url, '//th')
		td_columns = len(tr_list[1])

		consti_list = []

		for i in range(len(tr_list)):
			if len(tr_list[i]) < 2:
				pass
			elif tr_list[i][0].get('rowspan') == None: # 선거구명 자리의 rowspan이 지정되지 않았다 == 맨 왼쪽칸을 보고 있는 게 아니다.
				pass
			elif tr_list[i][0].text != None: # 선거구명이 blank가 아닌 경우에...
				district = tr_list[i][0] # 여기 저장되는 district 이름은 선거구 단위의 기초자치단체명임 ㅇㅇ. ex. <td rowspan="3" class="firstTd alignL">중구동구</td>
				towns = tr_list[i][2] # 읍면동수 ex. <td rowspan="3" class=alignR>23</td>
				pollPlaces = tr_list[i][3] # 투표구수 ex. <td rowspan="3" class=alignR>52</td>
				population = tr_list[i][4] # ex. <td rowspan="3" class=alignR>148,789<br/>(174 , 0)</td>
				electorates = tr_list[i][6] # ex. <td class=alignR>127,836<br/>(163 , 0)</td>
				pop_elec_ratio = tr_list[i][td_columns-2] # 선거인수/인구수 비율 ex. <td rowspan="3" class=alignR>85.9</td>
				households = tr_list[i][td_columns-1] # 세대수 ex. <td rowspan="3" class=alignR>67,548<br/>(172 , 0)</td>

				district_info = (district, towns, pollPlaces, population, electorates, pop_elec_ratio, households)
				district_info = dict(list(zip(self.attrs_district, district_info)))
				consti_list.append(district_info)

		consti_list = [self.parse_consti(consti, city_name=city_name) for consti in consti_list]
		print('crawled #%d - %s, %s(%d)...' % (self.nth, '지역구', city_name, len(consti_list)))
		return consti_list



	def parse(self, url, is_proportional, city_name=None):
		if is_proportional: return self.parse_proportional(url, city_name)
		else: return self.parse_constituency(url, city_name)




	def parse_record(self, record, attr_list):
		for attr in attr_list:
			if attr not in self.attrs_exclude_parse_cell:
				record[attr] = parse_cell(record[attr])

	def parse_dict_record(self, record, attr_list): #parse_record와 비슷. 단, 받은 record(list type)의 element가 dict type.
		for element in record:
			for attr in attr_list:
				if attr not in self.attrs_exclude_parse_cell:
					element[attr] = parse_cell(element[attr])


	def parse_consti(self, consti, city_name=None):
		self.parse_record(consti, self.attrs_district)
		# self.parse_dict_record(consti['result'], self.attrs_result)

		# never change the order
		consti['assembly_no'] = self.nth

		self.parse_district(consti, city_name)
		self.parse_towns(consti)
		self.parse_pollPlaces(consti)
		self.parse_population(consti)
		self.parse_electorate(consti)
		self.parse_pop_elec_ratio(consti)
		self.parse_households(consti)

		return consti


	def parse_district(self, consti, city_name):
		if city_name:
			consti['district'] = '%s %s' % (city_name, consti['district'])

	def parse_towns(self, consti):
		if 'towns' not in consti: return

		consti['towns'] = consti['towns'].replace(',', '')

	def parse_pollPlaces(self, consti):
		if 'pollPlaces' not in consti: return

		consti['pollPlaces'] = consti['pollPlaces'].replace(',', '')

	def parse_population(self, consti):
		if 'population' not in consti: return

		if type(consti['population']) == type([]): #nth != 20
			consti['population'] = sanitize(consti['population'][0])
		else:
			consti['population'] = sanitize(consti['population'])
		consti['population'] = consti['population'].replace(',', '')

	def parse_electorate(self, consti):
		if 'electorates' not in consti: return

		if type(consti['electorates']) == type([]):
			consti['electorates'] = sanitize(consti['electorates'][0])
		else:
			consti['electorates'] = sanitize(consti['electorates'])
		consti['electorates'] = consti['electorates'].replace(',', '')

	def parse_pop_elec_ratio(self, consti):
		if 'pop_elec_ratio' not in consti: return

		consti['pop_elec_ratio'] = consti['pop_elec_ratio'].replace(',', '')

	def parse_households(self, consti):
		if 'households' not in consti: return

		if type(consti['households']) == type([]):
			consti['households'] = sanitize(consti['households'][0])
		else:
			consti['households'] = sanitize(consti['households'])
		consti['households'] = consti['households'].replace(',', '')







	def parse_candi(self, candi):
		if self.is_proportional: #is_proportional
			candi['party_name_kr'] = sanitize(candi['name'])
			del candi['name']

		else: #!is_proportional
			[candi['party_name_kr'], candi['name_kr']] = list(map(sanitize, candi['name'][:2]))
			del candi['name']

		[candi['votenum'], candi['voterate']] = list(map(sanitize, candi['vote'][:2]))
		candi['votenum'] = candi['votenum'].replace(',', '')
		del candi['vote']



class MultiCityCrawler(BaseCrawler):

	def city_codes(self):
		list_ = get_json(self.url_city_codes_json)['jsonResult']['body']
		return [(x['CODE'], x['NAME']) for x in list_]

	def url_list(self, city_code):
		return self.url_list_base + str(city_code)

	def crawl(self):
		# 지역구 대표
		jobs = []
		is_proportional = self.is_proportional
		if is_proportional:
			voting_system = "proportional"
		else:
			voting_system = "constituency"

		print("Waiting to connect http://info.nec.go.kr server (%s)..." % voting_system)
		for city_code, city_name in self.city_codes():
			req_url = self.url_list(city_code)
			job = gevent.spawn(self.parse, req_url, is_proportional, city_name)
			jobs.append(job)
		gevent.joinall(jobs)
		every_result = [{'voting_system':voting_system, 'results':flatten(job.get() for job in jobs)}]

		# 비례대표
		if hasattr(self, 'prop_crawler'):
			prop_result = self.prop_crawler.crawl()
			every_result.extend(prop_result)


		return every_result

class SinglePageCrawler(BaseCrawler):

	def crawl(self):
		people = self.parse(self.url_list)
		return people
