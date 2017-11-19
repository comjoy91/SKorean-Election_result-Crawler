#!/usr/bin/env python3
# -*- coding=utf-8 -*-


############### is proportional in parse!


import gevent
from gevent import monkey
import itertools
from urllib.parse import urljoin
import copy

from utils import flatten, get_json, get_xpath, parse_cell, sanitize, split

monkey.patch_all()

class BaseCrawler_province(object):
	# url_image_base = 'http://info.nec.go.kr'

	# attrs = []
	attrs_municipal = ['municipal', 'villages', 'pollStations', 'population', 'electorates', 'popul_elector_ratio', 'households']
	# attrs_result = ['name', 'vote']
	# attrs_exclude_parse_cell = ['image', 'cand_no', 'result']


	def parse_city(self, url, params, target, elemType, city_name=None, _isRecent=False):
		tr_list = get_xpath(url, params, '//tr')
		th_list = get_xpath(url, params, '//th')
		td_columns = len(tr_list[1])
		if td_columns < 3: pass

		parse_result = []

		for i in range(len(tr_list)):
			if tr_list[i][0].get('rowspan') == None: # 이 tr의 맨 왼쪽칸이 rowspan=3으로 지정되지 않았다 == 이 tr은 '합계'가 아닌 '남' '여' 칸을 다루고 있다. 따라서 pass.
				pass

			else:
				municipal = tr_list[i][0] # 여기 저장되는 municipal 이름은 기초자치단체명 또는 선거구명임. ex. <td rowspan="3" class="firstTd alignL">중구동구</td>

				if elemType=='local_division':
					villages = tr_list[i][1] # 읍면동수 ex. <td rowspan="3" class=alignR>23</td>
					pollStations = tr_list[i][2] # 투표구수 ex. <td rowspan="3" class=alignR>52</td>
					population = tr_list[i][3] # ex. <td rowspan="3" class=alignR>148,789<br/>(174 , 0)</td>

					###### TODO: electorates 부분의 위치가 계속 바뀌고 있음. 확인할 필요 있음.
					if _isRecent:
						electorates = tr_list[i][td_columns-3] # ex. <td class=alignR>127,836<br/>(163 , 0)</td>
					else:
						electorates = tr_list[i][5] # ex. <td class=alignR>127,836<br/>(163 , 0)</td>
				else: #elemType == 'constituency_in_province'
					villages = tr_list[i][2] # 읍면동수 ex. <td rowspan="3" class=alignR>23</td>
					pollStations = tr_list[i][3] # 투표구수 ex. <td rowspan="3" class=alignR>52</td>
					population = tr_list[i][4] # ex. <td rowspan="3" class=alignR>148,789<br/>(174 , 0)</td>
					###### TODO: electorates 부분의 위치가 계속 바뀌고 있음. 확인할 필요 있음.
					electorates = tr_list[i][6] # ex. <td class=alignR>127,836<br/>(163 , 0)</td>

				popul_elector_ratio = tr_list[i][td_columns-2] # 선거인수/인구수 비율 ex. <td rowspan="3" class=alignR>85.9</td>
				households = tr_list[i][td_columns-1] # 세대수 ex. <td rowspan="3" class=alignR>67,548<br/>(172 , 0)</td>

				# 굳이 'td_columns-1' 인덱스를 쓰는 이유: "역대선거"와 "최근선거"의 표 칸 배치가 달라서.

				municipal_info = (municipal, villages, pollStations, population, electorates, popul_elector_ratio, households)
				municipal_info = dict(list(zip(self.attrs_municipal, municipal_info)))
				parse_result.append(municipal_info)

		parse_result = [self.parse_tr_xhtml(tr_elem, city_name=city_name) for tr_elem in parse_result]

		if elemType=='local_division':
			_elemType_str = '행정구역별(시군구) 선거인수(국내거소미신고 재외국민 포함)'
		else: #elemType == 'constituency_in_province'
			_elemType_str = '선거구별 선거인수'
		print(('crawled %s #%d - %s, %s(%d)...' % (target, self.nth, _elemType_str, city_name, len(parse_result))))
		return parse_result



	def parse_record(self, record, attr_list):
		for attr in attr_list:
#			if attr not in self.attrs_exclude_parse_cell:
			record[attr] = parse_cell(record[attr])

#	def parse_dict_record(self, record, attr_list): #parse_record와 비슷. 단, 받은 record(list type)의 element가 dict type.
#		for element in record:
#			for attr in attr_list:
#				if attr not in self.attrs_exclude_parse_cell:
#				element[attr] = parse_cell(element[attr])


	def parse_tr_xhtml(self, tr_elem, city_name=None):
		self.parse_record(tr_elem, self.attrs_municipal)
		# self.parse_dict_record(tr_elem['result'], self.attrs_result)

		# never change the order
		tr_elem['nth'] = self.nth

		self.parse_municipal(tr_elem, city_name)
		self.parse_villages(tr_elem)
		self.parse_pollStations(tr_elem)
		self.parse_population(tr_elem)
		self.parse_electorate(tr_elem)
		self.parse_popul_elector_ratio(tr_elem)
		self.parse_households(tr_elem)

		return tr_elem

	# 여기서부터의 parse_ () 함수들은, 각 숫자의 점, 괄호 등을 제거하는 역할임.
	def parse_municipal(self, tr_elem, city_name):
		if city_name:
			tr_elem['province'] = city_name
			tr_elem['municipal'] = sanitize(tr_elem['municipal'])

	def parse_villages(self, tr_elem):
		if 'villages' not in tr_elem: return

		tr_elem['villages'] = tr_elem['villages'].replace(',', '')
		tr_elem['villages'] = int(tr_elem['villages'])

	def parse_pollStations(self, tr_elem):
		if 'pollStations' not in tr_elem: return

		tr_elem['pollStations'] = tr_elem['pollStations'].replace(',', '')
		tr_elem['pollStations'] = int(tr_elem['pollStations'])

	def parse_population(self, tr_elem):
		if 'population' not in tr_elem: return

		if type(tr_elem['population']) == type([]): #nth != 20
			tr_elem['population'] = sanitize(tr_elem['population'][0])
		else:
			tr_elem['population'] = sanitize(tr_elem['population'])
		tr_elem['population'] = tr_elem['population'].replace(',', '')
		tr_elem['population'] = int(tr_elem['population'])

	def parse_electorate(self, tr_elem):
		if 'electorates' not in tr_elem: return

		if type(tr_elem['electorates']) == type([]):
			tr_elem['electorates'] = sanitize(tr_elem['electorates'][0])
		else:
			tr_elem['electorates'] = sanitize(tr_elem['electorates'])
		tr_elem['electorates'] = tr_elem['electorates'].replace(',', '')
		tr_elem['electorates'] = int(tr_elem['electorates'])

	def parse_popul_elector_ratio(self, tr_elem):
		if 'popul_elector_ratio' not in tr_elem: return

		tr_elem['popul_elector_ratio'] = tr_elem['popul_elector_ratio'].replace(',', '')
		tr_elem['popul_elector_ratio'] = float(tr_elem['popul_elector_ratio'])

	def parse_households(self, tr_elem):
		if 'households' not in tr_elem: return

		if type(tr_elem['households']) == type([]):
			tr_elem['households'] = sanitize(tr_elem['households'][0])
		else:
			tr_elem['households'] = sanitize(tr_elem['households'])
		tr_elem['households'] = tr_elem['households'].replace(',', '')
		tr_elem['households'] = int(tr_elem['households'])




class MultiCityCrawler_province(BaseCrawler_province):

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
		elemType = self.elemType
		nth = self.nth
		isRecent = self.isRecent

		print("Waiting to connect http://info.nec.go.kr server (%s)..." % elemType)
		for city_code, city_name in self.city_codes():
			if elemType == 'local_division':
				req_url = self.urlPath_town_list
			else: #elemType == 'constituency_in_province'
				req_url = self.urlPath_sgg_list
			req_param = self.JSON_url_param(elemType, city_code)
			job = gevent.spawn(self.parse_city, req_url, req_param, target, elemType, city_name, isRecent)
			jobs.append(job)
		gevent.joinall(jobs)
		every_result = [{'election_type':target,'element_type':elemType,'nth':nth,'results':flatten(job.get() for job in jobs)}]

		# 추가될 수도 있는 데이터 크롤링을 위해 next_crawler를 추가하는 내용.
		if hasattr(self, 'next_crawler'):
			next_result = self.next_crawler.crawl()
			every_result.extend(next_result)


		return every_result

#class SinglePageCrawler(BaseCrawler):

	#def crawl(self):
		#people = self.parse(self.url_list)

		#return people
