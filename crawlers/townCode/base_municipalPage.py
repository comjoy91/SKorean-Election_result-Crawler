#!/usr/bin/env python3
# -*- coding=utf-8 -*-


import gevent
from gevent import monkey
import itertools
from urllib.parse import urljoin
import copy
from time import sleep

from utils import flatten, get_json, get_xpath, parse_cell, sanitize, split, InvalidCrawlerError

monkey.patch_all()

class BaseCrawler_municipal(object):
	def constant_elected(self, target, nth, consti_seq):
		code_toNumElected = dict()

		if (target=='assembly'):
			if 9 <= nth <= 12:
				num_elected = 2
			else:
				num_elected = 1
		elif (target=='local-pp') or (target=='local-ep'):
			num_elected = 1
		else:
			num_elected = 1

		for x in consti_seq:
			code_toNumElected[x] = num_elected
		return code_toNumElected

	def parse_elected(self, url, params, target, city_code, consti_toCode):
		code_toNumElected = dict()
		params['cityCode'] = -1 if (params['electionCode']==7) else city_code
		xpath = get_xpath(url, params, './/table[@id="table01"]')[0]
		tr_list = xpath.findall('.//tr') #개별 <tr> 안에 한 줄씩 <td>들이 들어있음.
		num_trs = len(tr_list)
		row_head = 1

		consti_seq = []

		if (params['electionCode']==7):#'assembly_PR'
			num_elected = num_trs - row_head
			for consti in consti_toCode:
				code = consti_toCode[consti][0]
				code_toNumElected[code] = num_elected
				consti_seq.append(code)
			return (code_toNumElected, consti_seq)

		elif (params['electionCode']==9):#'local-mp_PR'
			name_index = 0
			string_read_index = 1
		elif (params['electionCode']==8):#'local-pp_PR'
			name_index = 0
			string_read_index = 0
		elif (target=='local-pp') or (target=='local-mp'):
			name_index = 1
			string_read_index = 1
		else:
			name_index = 0
			string_read_index = 1

		i = row_head
		while i < num_trs:
			district_name = tr_list[i][name_index].text[string_read_index:]
			if not district_name in consti_toCode:
				i = i+1
				pass
			else:
				district_code = consti_toCode[district_name][0]
				num_elected = 1
				i = i+1
				while i < num_trs and district_name == tr_list[i][name_index].text[string_read_index:]:
					#print("%d, %d, %d, %s, %s" % (num_trs, i, num_elected, district_name, tr_list[i][name_index].text[1:]))
					num_elected = num_elected+1
					i = i+1
				code_toNumElected[district_code] = num_elected
				consti_seq.append(district_code)
				del consti_toCode[district_name][0]

		return (code_toNumElected, consti_seq)

	def parse_city(self, url, params, target, target_kor, nth, city_code=None, city_name=None):
		_town_list = get_json(url['town'], params['town'])['jsonResult']['body']
		_townSeq_list = []
		_towntoCode_dict = dict()
		_codetoTown_dict = dict()
		if (target=='assembly' and nth <= 16) or \
			(target=='local-mp' and nth <= 3) or \
			(target=='local-pp' and nth <= 3):
			for x in _town_list:
				x['CODE'] = int(x['CODE'])
				if x['CODE'] < 10000:
					x['CODE'] = x['CODE']*10 + 3
				_towntoCode_dict[x['NAME']] = x['CODE']
				_codetoTown_dict[x['CODE']] = x['NAME']
				_townSeq_list.append(x['CODE'])

		else:
			for x in _town_list:
				x['CODE'] = int(x['CODE'])
				_towntoCode_dict[x['NAME']] = x['CODE']
				_codetoTown_dict[x['CODE']] = x['NAME']
				_townSeq_list.append(x['CODE'])

		# _sgg_list = get_json(url['sggCity'], params['sggCity'])['jsonResult']['body']
		# _sggSeq_list = []
		# _sggtoCode_dict = dict()
		# _codetoSgg_dict = dict()
		# _codetoNumElected_dict = dict()
		# for x in _sgg_list:
		# 	x['CODE'] = int(x['CODE'])
		# 	if not x['NAME'] in _sggtoCode_dict:
		# 		_sggtoCode_dict[x['NAME']] = []
		# 	_sggtoCode_dict[x['NAME']].append(x['CODE'])
		# 	_codetoSgg_dict[x['CODE']] = x['NAME']
		# 	_sggSeq_list.append(x['CODE'])
		# if (target=='local-pp' or target=='local-mp' or target=='assembly'):
		# 	xhtml_url = self.urlPath_elector_list
		# 	xhtml_params = self.urlParam_elector_list
		# 	(_codetoNumElected_dict, _sggSeq_list_neo) = self.parse_elected(xhtml_url, xhtml_params, target, city_code, copy.deepcopy(_sggtoCode_dict))
		# else:
		# 	_codetoNumElected_dict = self.constant_elected(target, nth, _sggSeq_list)

		_sggSeq_list = []
		_sggtoCode_dict = dict()
		_codetoSgg_dict = dict()
		_codetoNumElected_dict = dict()
		for town_code in _townSeq_list:
			params['sggTown']['townCode'] = town_code
			sleep(0.3)
			_sgg_list = get_json(url['sggTown'], params['sggTown'])['jsonResult']['body']
			for x in _sgg_list:
				print(x['NAME'])
				x['CODE'] = int(x['CODE'])
				if not x['NAME'] in _sggtoCode_dict:
					_sggtoCode_dict[x['NAME']] = []
				_sggtoCode_dict[x['NAME']].append(x['CODE'])
				_codetoSgg_dict[x['CODE']] = x['NAME']
				_sggSeq_list.append(x['CODE'])
		if (target=='local-pp' or target=='local-mp' or target=='assembly'):
			xhtml_url = self.urlPath_elector_list
			xhtml_params = self.urlParam_elector_list
			(_codetoNumElected_dict, _sggSeq_list_neo) = self.parse_elected(xhtml_url, xhtml_params, target, city_code, copy.deepcopy(_sggtoCode_dict))
		else:
			_codetoNumElected_dict = self.constant_elected(target, nth, _sggSeq_list)

		sleep(1)

		_PR_sggSeq_list = []
		_PR_sggtoCode_dict = dict()
		_PR_codetoSgg_dict = dict()
		if 'PR_sgg' in params:
			if (target=='assembly') and (nth==17):
				_PR_sgg_list = [{'CODE':7000000, 'NAME':"비례대표"}]
				_PR_sggtoCode_dict = {"비례대표": [7000000]}
				_PR_codetoSgg_dict = {7000000: "비례대표"}
				_PR_sggSeq_list = [7000000]
			else:
				for town_code in _townSeq_list:
					sleep(0.2)
					params['PR_sgg']['townCode'] = town_code
					_PR_sgg_list = get_json(url['sggTown'], params['PR_sgg'])['jsonResult']['body']
					for x in _PR_sgg_list:
						print(x['NAME'])
						if not x['NAME'] in _PR_sggtoCode_dict:
							_PR_sggtoCode_dict[x['NAME']] = []
						if not x['CODE'] in _PR_sggtoCode_dict[x['NAME']]:
							_PR_sggtoCode_dict[x['NAME']].append(x['CODE'])
						_PR_codetoSgg_dict[x['CODE']] = x['NAME']
						if not x['CODE'] in _PR_sggSeq_list:
							_PR_sggSeq_list.append(x['CODE'])
			xhtml_url = self.urlPath_elector_list
			xhtml_params = self.urlParam_PR_elector_list
			(_PR_codetoNumElected_dict, _PR_sggSeq_list_neo) = self.parse_elected(xhtml_url, xhtml_params, target, city_code, copy.deepcopy(_PR_sggtoCode_dict))

		_result = dict(city_name=city_name, city_code=int(city_code))
		#_result['town_list'] = _town_list
		_result['town_Seq'] = _townSeq_list
		_result['town_toCode'] = _towntoCode_dict
		_result['code_toTown'] = _codetoTown_dict
		if len(_sggSeq_list) > 0:
			#_result['consti_list'] = _sgg_list
			_result['consti_Seq'] = _sggSeq_list
			_result['consti_toCode'] = _sggtoCode_dict
			_result['code_toConsti'] = _codetoSgg_dict
			_result['code_toNumElected'] = _codetoNumElected_dict
		if len(_PR_sggSeq_list) > 0:
			#_result['PR_consti_list'] = _PR_sggSeq_list
			_result['PR_consti_Seq'] = _PR_sggSeq_list
			_result['PR_consti_toCode'] = _PR_sggtoCode_dict
			_result['PR_code_toConsti'] = _PR_codetoSgg_dict
			_result['PR_code_toNumElected'] = _PR_codetoNumElected_dict

		print('\x1b[1;31mcrawled %s election #%d - \x1b[1;m%s' % (target, self.nth, city_name))
		print('\t└  %s, %s(%d)...' % ('구시군 행정구역 목록', city_name, len(_townSeq_list)))
		if len(_PR_sggtoCode_dict) > 0:
			print('\t└  %s, %s(%d)...' % (target_kor+' 비례대표 선거구(자치구시군) 목록', city_name, len(_PR_sggSeq_list)))
		print('\t└  %s, %s(%d)...' % (target_kor+' 선거구 목록', city_name, len(_sggSeq_list)))

		return _result




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

	def JSON_url_param(self, city_code, param_dict): # 각 광역자치단체별 기초자치단체 code 리스트를 json으로 받을 URL의 parameter.
		param_dict['town']['cityCode'] = city_code
		param_dict['sggCity']['cityCode'] = city_code
		if hasattr(self, 'urlParam_PR_sgg_list'):
			param_dict['PR_sgg'] = copy.deepcopy(self.urlParam_PR_sgg_list)
			param_dict['PR_sgg']['cityCode'] = city_code

		if self.target=='assembly' and self.nth==17:
			param_dict['sggCity']['cityCode'] = city_code+'00'
		return param_dict

	def crawl(self):

		jobs = []
		target = self.target
		target_eng = self.target_eng
		target_kor = self.target_kor
		nth = self.nth

		city_code_list = self.city_codes()
		req_url = dict(town=self.urlPath_town_list, sggCity=self.urlPath_sgg_list, sggTown=self.urlPath_sggTown_list)
		param_dict = dict(town=self.urlParam_town_list, sggCity=self.urlParam_sgg_list, sggTown=self.urlParam_sggTown_list)

		# 광역자치단체 내의 기초자치단체 내의 선거구 데이터 크롤링의 기본과정.
		print("\x1b[1;36mWaiting to connect http://info.nec.go.kr server (%s, %d-th)...\x1b[1;m" % (target_eng, nth))

		every_result = [{'election_type':target,'nth':nth,'results':[]}]
		for city_code, city_name in city_code_list: # 각 광역자치단체 별로 아래 단계를 수행.
			req_param = self.JSON_url_param(city_code, param_dict)
			job = self.parse_city(req_url, req_param, target, target_kor, nth, city_code, city_name)
			jobs.append(job)
			sleep(1)
		every_result = [{'election_type':target,'nth':nth,'results':jobs}]
	    #
		# 	job = gevent.spawn(self.parse_city, req_url, req_param, target, target_kor, nth, city_code, city_name)
		# 	jobs.append(job)
		# gevent.joinall(jobs)
		# every_result = [{'election_type':target,'nth':nth,'results':flatten(job.get() for job in jobs)}]

		# for city_code, city_name in city_code_list:
		# 	print('\x1b[1;31mcrawled %s election #%d - \x1b[1;m%s' % (target, self.nth, city_name))
		# 	town_code_list = self.town_codes(city_code, copy.deepcopy(param_dict['town']))
		# 	print('\t└  %s, %s(%d)...' % ('구시군 행정구역 목록', city_name, len(town_code_list)))
		# 	jobs = []
		# 	# 광역자치단체(city_code) 내의 기초자치단체 별로 아래 단계를 수행.
		# 	for town_code, town_name in town_code_list:
		# 		req_param = self.JSON_url_param(town_code, copy.deepcopy(param_dict['sggTown']))
		# 		job = gevent.spawn(self.parse_town, req_url, req_param, target, target_kor, town_code, town_name)
		# 		jobs.append(job)
		# 	# 개별 기초자치단체 수행 끝.
		# 	gevent.joinall(jobs)
		# 	result_by_city = dict(city_name=city_name, city_code=int(city_code), town_list=flatten(job.get() for job in jobs))
		# 	every_result[0]['results'].append(result_by_city)

		# 추가될 수도 있는 데이터 크롤링을 위해 next_crawler를 추가하는 내용.
		if hasattr(self, 'next_crawler'):
			next_result = self.next_crawler.crawl()
			every_result.extend(next_result)

		return every_result
