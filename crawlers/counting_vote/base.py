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

class BaseCrawler(object):
	url_image_base = 'http://info.nec.go.kr'

	attrs = []
	attrs_district = ['district', 'electorates', 'counted_votes', 'cand_no', 'result', 'valid_votes', 'undervotes', 'blank_ballots']
	attrs_result = ['name', 'vote']
	attrs_exclude_parse_cell = ['image', 'cand_no', 'result']


	def parse_constant_candiNum(self, url, params, target, target_kor, city_name=None): #지금 이건 비례대표만 해당하는 거임 ㅇㅇㅇㅇㅇ
		elems = get_xpath(url, params, './/table[@id="table01"]')[0].findall('.//td') #fucking_4th_president_ths!!!!
		th_list = get_xpath(url, params, './/table[@id="table01"]')[0].findall('.//th') #fucking_4th_president_ths!!!!

		if th_list[0].get('rowspan') != None: #"최근선거"가 아니라면
			for i in range(int(len(th_list))):
				if th_list[i].get('colspan') != None: #이 칸은 "정당별/후보자별 득표수"임. colspan = 총 후보자수 + 1(합계).
					num_ths_left = i #정당/후보별 득표수 왼쪽에 있는 칸: '구시군명', '선거인수', '투표수'. 보통은 3일 것임.
					max_candidate_num = int(th_list[i].get('colspan')) - 1 #총 후보자수
					break
			candi_name_list = th_list[6:(6+max_candidate_num)] #element: <th><strong>한나라당</strong></th>
			row_head = 0 #읽기 시작할 행의 번째. 0번째줄의 "합계" 칸을 비울 것인가?
			num_tds = 6 + max_candidate_num #저 6의 확장일반화 방법은 없는가.
			num_rows = int(len(elems) / num_tds) #row_head를 포함한 전체 행 수

		else: #"최근선거"라면
			for i in range(int(len(th_list))):
				if th_list[i].get('colspan') != None: #이 칸은 "정당별/후보자별 득표수"임. colspan = 총 후보자수.
					num_ths_left = i #정당/후보별 득표수 왼쪽에 있는 칸: '구시군명', '선거인수', '투표수'. 보통은 3일 것임.
					max_candidate_num = int(th_list[i].get('colspan')) #총 후보자수
					break
			candi_name_list = elems[num_ths_left:(num_ths_left+max_candidate_num)] #element: <td><strong>한나라당</strong></td>
			row_head = 1 #읽기 시작할 행의 번째. 0번째줄의 후보/정당명은 비우고, 1번째줄의 "합계" 칸을 비울 것인가?
			num_tds = len(th_list) + max_candidate_num - 1
			num_rows = int(len(elems) / num_tds) #row_head를 포함한 전체 행 수

		region_info = () # 이 region '전체'의 개표결과를 담음.
		district_list = [] # 이 region 내의 각 district별 개표결과를 담음.
		candidate_num = max_candidate_num

		for i in range(num_rows - row_head):
			index = (i+row_head) * num_tds
			district = elems[index]#.text # 여기 저장되는 district 이름은 '전체'(첫 줄)+기초자치단체명임 ㅇㅇ
			electorates = elems[index + 1]#.text
			counted_vote = elems[index + 2]#.text

			votes_num_percent = elems[index + num_ths_left : index + num_ths_left+candidate_num] #element: <td>1,940,259<br>(42.28)</td>
			cand_list = list(map(lambda x, y: dict(list(zip(self.attrs_result, [x, y]))), candi_name_list, votes_num_percent)) #('name': <th><strong>한나라당</strong></th>, 'vote': <td>1,940,259<br>(42.28)</td>)

			valid_vote = elems[index + num_ths_left + max_candidate_num+0]#.text
			undervote = elems[index + num_ths_left + max_candidate_num+1]#.text
			blank_ballot = elems[index + num_ths_left + max_candidate_num+2]#.text

			district_info = (district, electorates, counted_vote, candidate_num, cand_list, valid_vote, undervote, blank_ballot)
			district_info = dict(list(zip(self.attrs_district, district_info)))

			if i==0: # 이 region '전체'의 개표결과를 담음.
				region_info = district_info
			else: # 이 region 내의 각 district별 개표결과를 담음.
				district_list.append(district_info)

		return_result = [{'region': city_name, \
						'region_result': self.parse_consti(region_info, city_name=city_name), \
						'district_result': [self.parse_consti(district, city_name=city_name) for district in district_list]}]
		print('crawled %s election #%d - %s, %s(%d)' % \
			(target, self.nth, target_kor+' 구시군별 득표', city_name, len(return_result[0]['district_result'])))

		return return_result




	def parse_various_candiNum(self, url, params, target, target_kor, city_name=None): #지금 이건 지역구만 해당하는 거임 ㅇㅇㅇㅇㅇ
		tr_list = get_xpath(url, params, './/table[@id="table01"]')[0].findall('.//tr') #개별 <tr> 안에 한 줄씩 <td>들이 들어있음.
		thead_list = get_xpath(url, params, './/table[@id="table01"]')[0].findall('.//th')
		max_candidate_num = len(tr_list[2]) - len(thead_list) # +1-1. 후보자 부분의 '계' 때문.
		for i in range(len(thead_list)):
			if thead_list[i].get('colspan') != None:
				num_ths_left = i
				break

		consti_list = []

		for i in range(len(tr_list)):
			if len(tr_list[i]) < 2:
				pass
			elif tr_list[i][1].text == None: # 선거인수 칸이 blank인 줄을 찾으면, 그 칸 아래가 실득표수이므로...
				#index = i+1
				candidate_num = 0
				candi_name_list = []
				votes_num_percent = []

				district = tr_list[i][0]#.text # 여기 저장되는 district 이름은 선거구 이름임.
				electorates = tr_list[i+1][num_ths_left-2]#.text
				counted_vote = tr_list[i+1][num_ths_left-1]#.text

				for j in range(max_candidate_num):
					j_index = j+num_ths_left
					if (tr_list[i][j_index].findtext('strong') != None) : #\
								#and (tr_list[i][j_index].findtext('strong') != '') \
								#and (tr_list[i][j_index].text != '계') \
								#:
						candidate_num = candidate_num+1
						candi_name_list.append(tr_list[i][j_index]) #element: <td><strong>한나라당<br>김광영</strong></td>
						votes_num_percent.append(tr_list[i+1][j_index]) #element: <td>3,050<br>(4.09)</td>

					cand_list = list(map(lambda x, y: dict(list(zip(self.attrs_result, [x, y]))), candi_name_list, votes_num_percent)) #('name': <td><strong>한나라당<br>김광영</strong></td>, 'vote': <td>3,050<br>(4.09)</td>)

				valid_vote = tr_list[i+1][num_ths_left + max_candidate_num+0]#.text
				undervote = tr_list[i+1][num_ths_left + max_candidate_num+1]#.text
				blank_ballot = tr_list[i+1][num_ths_left + max_candidate_num+2]#.text

				district_info = (district, electorates, counted_vote, candidate_num, cand_list, valid_vote, undervote, blank_ballot)
				district_info = dict(list(zip(self.attrs_district, district_info)))
				consti_list.append(district_info)

		return_result = [{'region': city_name, 'district_result': [self.parse_consti(consti, city_name=city_name) for consti in consti_list]}]
		print('crawled %s election #%d - %s, %s(%d)' % \
			(target, self.nth, target_kor+' 지역구별 득표', city_name, len(return_result[0]['district_result'])))

		return return_result



	def parse(self, url, params, constant_candidates, target, target_kor, city_name=None):
		if constant_candidates: #표의 각 열에서 후보자수가 동일하다면
			return self.parse_constant_candiNum(url, params, target, target_kor, city_name)
		else: #표의 각 열에서 후보자수가 동일하지 않다면
			return self.parse_various_candiNum(url, params, target, target_kor, city_name)





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
		self.parse_dict_record(consti['result'], self.attrs_result)

		# never change the order
		consti['nth'] = self.nth

		self.parse_district(consti, city_name)
		self.parse_electorate(consti)
		self.parse_counted_votes(consti)
		self.parse_result(consti)
		self.parse_valid_votes(consti)
		self.parse_undervotes(consti)
		self.parse_blank_ballots(consti)

		return consti


	def parse_district(self, consti, city_name):
		if city_name:
			consti['region'] = city_name
			consti['district'] = sanitize(consti['district'])

	def parse_electorate(self, consti):
		if 'electorates' not in consti: return

		if type(consti['electorates']) == type([]): #역대선거
			consti['electorates'] = sanitize(consti['electorates'][0])
		else: #최근선거
			consti['electorates'] = sanitize(consti['electorates'])
		consti['electorates'] = consti['electorates'].replace(',', '')
		consti['electorates'] = int(consti['electorates'])

	def parse_counted_votes(self, consti):
		if 'counted_votes' not in consti: return

		if type(consti['counted_votes']) == type([]): #역대선거
			consti['counted_votes'] = sanitize(consti['counted_votes'][0])
		else: #최근선거
			consti['counted_votes'] = sanitize(consti['counted_votes'])
		consti['counted_votes'] = consti['counted_votes'].replace(',', '')
		consti['counted_votes'] = int(consti['counted_votes'])

	def parse_result(self, consti):
		if 'result' not in consti: return

		for candi in consti['result']:
			self.parse_candi(candi)

	def parse_valid_votes(self, consti):
		if 'valid_votes' not in consti: return

		consti['valid_votes'] = consti['valid_votes'].replace(',', '')
		consti['valid_votes'] = int(consti['valid_votes'])

	def parse_undervotes(self, consti):
		if 'undervotes' not in consti: return

		consti['undervotes'] = consti['undervotes'].replace(',', '')
		consti['undervotes'] = int(consti['undervotes'])

	def parse_blank_ballots(self, consti):
		if 'blank_ballots' not in consti: return

		consti['blank_ballots'] = consti['blank_ballots'].replace(',', '')
		consti['blank_ballots'] = int(consti['blank_ballots'])

	def parse_candi(self, candi):
		if self.candidate_type == 'party_candidate': # candi['name'] == <th><strong>새정치민주연합<br>박원순</strong></th>
			[candi['party_name_kr'], candi['name_kr']] = list(map(sanitize, candi['name'][:2]))
			del candi['name']

		elif self.candidate_type == 'party_list': # candi['name'] == <th><strong>새정치민주연합</strong></th>
			candi['party_name_kr'] = sanitize(candi['name'])
			del candi['name']

		elif self.candidate_type == 'independent_candidate': # candi['name'] == <th><strong>조희연</strong></th>
			candi['name_kr'] = sanitize(candi['name'])
			del candi['name']

		else:
			raise NotImplementedError("잘못된 candidate_type이 들어옴: one of three, 'party_candidate', 'party_list', or 'independent_candidate'")

		[candi['votenum'], candi['voterate']] = list(map(sanitize, candi['vote'][:2]))
		candi['votenum'] = candi['votenum'].replace(',', '')
		candi['votenum'] = int(candi['votenum'])
		candi['voterate'] = float(candi['voterate'])
		del candi['vote']



class MultiCityCrawler(BaseCrawler):

	def city_codes(self, nationalSum): # 광역자치단체 code 리스트를 json으로 받게 됨.
		list_ = get_json(self.urlPath_city_codes, self.urlParam_city_codes)['jsonResult']['body']
		if nationalSum: # '전국 합계를 받아라' 라고 설정되었다면
			list_.insert(0, {'CODE': 0, 'NAME': "전국 광역자치단체"})
		return [(x['CODE'], x['NAME']) for x in list_]

	def XHTML_url_param(self, city_code): # XHTML(결과 아웃풋)을 받을 URL의 parameter.
		param_dict = copy.deepcopy(self.urlParam_result_list)
		param_dict['cityCode'] = city_code
		return param_dict

	def crawl(self):
		# 지역구 대표
		jobs = []
		constant_candidates = self.constant_candidates
		candidate_type = self.candidate_type
		nationalSum = self.nationalSum if hasattr(self, 'nationalSum') else False
		target = self.target
		target_kor = self.target_kor
		nth = self.nth
		req_url = self.urlPath_result_list

		print("Waiting to connect http://info.nec.go.kr server (%s, %d-th)..." % (target, nth))
		for city_code, city_name in self.city_codes(nationalSum):
			req_param = self.XHTML_url_param(city_code)
			job = gevent.spawn(self.parse, req_url, req_param, constant_candidates, target, target_kor, city_name)
			jobs.append(job)
		gevent.joinall(jobs)
		every_result = [{'election_type':target, 'nth':nth, 'candidate_type':candidate_type, \
						'results':flatten(job.get() for job in jobs)}]

		# 비례대표
		if hasattr(self, 'next_crawler'):
			prop_result = self.next_crawler.crawl()
			every_result.extend(prop_result)


		return every_result
