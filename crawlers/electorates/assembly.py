#!/usr/bin/env python
# -*- encoding=utf-8 -*-

from crawlers.electorates.base_provincePage import *
from utils import sanitize

def Crawler(nth, election_name):
	target = 'assembly'
	if 1 <= nth <= 17:
		raise NotImplementedError('Korean National Election Committee does not have any data about electorates in each constituencies of the 1st~17th general election.')
		# 지역구별 선거인수가 나오지 않고, 기초자치단체별 선거인수만 나옴.
		# 선거인수를 받기 위해서는, 결국 개표 결과에 나오는 선거인수를 받아야 함.
	elif 18 <= nth <= 20:
		crawler = ElectorCrawler_Old(int(nth), election_name, target)
	elif nth == 21:
		raise InvalidCrawlerError('assembly', 'electorates', nth)
		#"최근선거"로 들어갈 때의 code: crawler = ElectorCrawler_Recent(int(nth), election_name, target)
	else:
		raise InvalidCrawlerError('assembly', 'electorates', nth)
	return crawler



class ElectorCrawler_GuOld(MultiCityCrawler_province):

#	def parse_tr(self, consti, city_name=None):
#		consti = super(ElectorCrawler_GuOld, self).parse_tr(consti, city_name)
#		return consti

	def __init__(self, nth, _election_name, _target):
		self.nth = nth
		self.target = _target
		self.elemType = 'constituency_in_province'

		self.urlPath_city_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson_GuOld.json'
		self.urlParam_city_codes = dict(electionId='0000000000')

		self.urlPath_sgg_list = 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml'
		self.urlParam_sgg_list = dict(electionId='0000000000',\
										requestURI='/WEB-INF/jsp/electioninfo/0000000000/vc/vccp09.jsp',\
										statementId='VCCP09_#90',\
										oldElectionType=1, electionType=2, electionCode=2,\
										townCode=-1, sggCityCode=-1)

		self.urlParam_city_codes['electionCode'] = _election_name
		self.urlParam_sgg_list['electionName'] = _election_name


class ElectorCrawler_Old(MultiCityCrawler_province):

#	def parse_tr(self, consti, city_name=None):
#		consti = super(ElectorCrawler_Old, self).parse_tr(consti, city_name)
#		return consti

	def __init__(self, nth, _election_name, _target):
		self.nth = nth
		self.target = _target
		self.elemType = 'constituency_in_province'

		self.urlPath_city_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson_Old.json'
		self.urlParam_city_codes = dict(electionId='0000000000',\
										subElectionCode=2)

		self.urlPath_sgg_list = 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml'
		self.urlParam_sgg_list = dict(electionId='0000000000',\
									requestURI='/WEB-INF/jsp/electioninfo/0000000000/bi/bipb02.jsp',\
									statementId='BIPB02_#3_2',\
									oldElectionType=1, electionType=2, electionCode=2,\
									searchType=3, townCode=-1, sggCityCode=-1)

		self.urlParam_city_codes['electionCode'] = _election_name
		self.urlParam_sgg_list['electionName'] = _election_name

		self.urlParam_sgg_list['statementId'] = 'BIPB02_#3_2_1' if nth==20 else 'BIPB02_#3_2' #왜 얘만 다른지는 모르겠습니다.

		# 재외국민선거 도입으로 지역구 선거인수와 비례대표 선거인수가 달라짐.
		# 비례대표 선거인수는 시군구 단위를 따름.
		if nth == 18: # 18대 총선(2008)은 재외국민선거 도입 이전: 지역구 선거인수와 비례대표 선거인수가 같음. 따라서 지역구 선거인수만 크롤링함.
			pass
		else:
			self.next_crawler = prop_ElectorCrawler_Old(nth, _election_name, _target)
			self.next_crawler.nth = nth


class ElectorCrawler_Recent(MultiCityCrawler_province):

#	def parse_tr(self, consti, city_name=None):
#		consti = super(ElectorCrawler_Recent, self).parse_tr(consti, city_name)
#		return consti

	def __init__(self, nth, _election_name, _target):
		self.nth = nth
		self.target = _target
		self.election_name = _election_name
		self.elemType = 'constituency_in_province'

		self.urlPath_city_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson.json'
		self.urlParam_city_codes = dict(electionCode=2)

		self.urlPath_sgg_list = 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml'
		self.urlParam_sgg_list = dict(requestURI='/WEB-INF/jsp/electioninfo/'+election_name+'/bi/bipb02.jsp',\
									statementId='BIPB02_#3_2',\
									electionCode=2, searchType=3, townCode=-1)

		self.urlParam_city_codes['electionId'] = _election_name
		self.urlParam_sgg_list['electionId'] = _election_name

		self.next_crawler = prop_ElectorCrawler_Recent(nth, _election_name, _target)
		self.next_crawler.nth = nth






class prop_ElectorCrawler_Old(MultiCityCrawler_province):

#	def parse_tr(self, consti, city_name=None):
#		consti = super(prop_ElectorCrawler_Old, self).parse_tr(consti, city_name)
#		return consti

	def __init__(self, nth, _election_name, _target):
		self.nth = nth
		self.target = _target
		self.elemType = 'local_division'

		self.urlPath_city_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson_Old.json'
		self.urlParam_city_codes = dict(electionId='0000000000',\
										subElectionCode=2)

		self.urlPath_town_list = 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml'
		self.urlParam_town_list = dict(electionId='0000000000',\
									requestURI='/WEB-INF/jsp/electioninfo/0000000000/bi/bipb02.jsp',\
									statementId='BIPB02_#2_1',\
									oldElectionType=1, electionType=2, electionCode=2,\
									searchType=2, townCode=-1, sggCityCode=-1)

		self.urlParam_city_codes['electionCode'] = _election_name
		self.urlParam_town_list['electionName'] = _election_name

		self.urlParam_sgg_list['statementId'] = 'BIPB02_#2_1' if nth==20 else 'BIPB02_#2' #왜 얘만 다른지는 모르겠습니다.

class prop_ElectorCrawler_Recent(MultiCityCrawler_province):

#	def parse_tr(self, consti, city_name=None):
#		consti = super(prop_ElectorCrawler_Recent, self).parse_tr(consti, city_name)
#		return consti

	def __init__(self, nth, _election_name, _target):
		self.nth = nth
		self.target = _target
		self.election_name = _election_name
		self.elemType = 'local_division'

		self.urlPath_city_codes = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson.json'
		self.urlParam_city_codes = dict(electionCode=7)

		self.urlPath_town_list = 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml'
		self.urlParam_town_list = dict(requestURI='/WEB-INF/jsp/electioninfo/'+election_name+'/bi/bipb02.jsp',\
									statementId='BIPB02_#3_7',\
									electionCode=7, searchType=3, townCode=-1)

		self.urlParam_city_codes['electionId'] = _election_name
		self.urlParam_town_list['electionId'] = _election_name
