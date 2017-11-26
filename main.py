#!/usr/bin/env python3
# -*- encoding=utf-8 -*-

from argparse import ArgumentParser, RawTextHelpFormatter
import codecs
import gevent
from gevent import monkey
import json
from datetime import datetime
from threading import Timer, Thread
import sched, time

from crawlers import Crawler
from utils import check_dir

def print_json(filename, encoding, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=(encoding=='unicode'))

def crawl(target, _dataType, nth, printer, filename, encoding, localType=None):
    crawler = Crawler(target, _dataType, nth, localType)
    cand_list = crawler.crawl()
    printer(filename, encoding, cand_list)

def create_parser():
    parser = ArgumentParser(formatter_class=RawTextHelpFormatter)
    #target: 의회 총선거-assembly, 지방선거-local, 대통령-president
    parser.add_argument('target', choices=['assembly', 'local', 'president'],\
            help="name of target election\n"
            "- if you choose 'local', you have to input -l argument.\n")
    #dataType: 기초자치단체or국회의원선거구 코드-townCode, 선거인수-electorates, 정당 코드-partyCode, 개표결과-counting_vote, 읍면동별 개표결과-counting_vote_dong
    parser.add_argument('dataType', choices=['townCode', 'electorates', 'partyCode', 'counting_vote', 'counting_vote_dong'],\
            help="type of collecting data\n")
    #start, end: 선거 대수
    parser.add_argument('start', help="starting election id", type=int)
    parser.add_argument('end', help="ending election id", type=int,\
            nargs='?', default=None)

    #-time: 파일 이름에 시간을 넣을 것이냐 말 것이냐.
    parser.add_argument('-time', dest='filename_time', action='store_true',\
            help="Descript the crawling moment time info in filename.")
    #-interval n: n초 간격으로 자동 크롤링 할 것인가.
    parser.add_argument('-interval', dest='interval_time',\
                help="number of interval seconds.\n"
                "- if you type integer number, the program will automatically crawl data in every 'interval' seconds.\n"
                "- if you type 0 or do not type anything, the program will crawl only once.",\
                type=int, default=None)
    #-e: utf8(default), unicode 중에서 인코딩 선택
    parser.add_argument('-e', dest='encoding', choices=['unicode', 'utf8'], default='utf8',\
            help="Korean Hangul encoding.\n"
                "- utf8 for default.")
    #-d: 아웃풋 데이터 저장 디렉토리 지정
    parser.add_argument('-d', dest='directory', help="Specify data directory.")

    # TODO: change to subparser
    parser.add_argument('-l', choices=['pa', 'pp', 'ma', 'mp', 'ea', 'ep'],
            dest="localType",
            help="Specify election type for local elections.\n"
                "- 1st char: {p:province, m:municipality, e:education},\n"
                "- 2nd char: {a: administration, p: parliament}")

    return parser

def print_file(arg_namespace):
    _arg = arg_namespace

    printer = print_json
    encoding = _arg.encoding

    target = _arg.target
    dataType = _arg.dataType
    start = _arg.start
    end = _arg.end if _arg.end else start
    filename_time = _arg.filename_time
    filetype = 'json'

    interval_time = _arg.interval_time
    if target=='local':
        localType = _arg.localType
    else:
        localType = None

    if _arg.directory:
        datadir = _arg.directory
    else:
        if (target=='local' and localType):
            datadir = './crawled_data/%s-%s/%s' % (target, localType, dataType)
        else:
            datadir = './crawled_data/%s/%s' % (target, dataType)

    time_string = datetime.today().strftime("%Y%m%d%H%M%S")
    check_dir(datadir)

    jobs = []
    if target=='local':
        if filename_time:
            for n in range(start, end+1):
                filename = '%s/%s-%s-%s-%d-%s.%s'\
                    % (datadir, target, localType, dataType, n, time_string, filetype)
                job = gevent.spawn(crawl, target=target, localType=localType,\
                    _dataType=dataType, nth=n, filename=filename, encoding=encoding, printer=printer)
                jobs.append(job)
        else:
            for n in range(start, end+1):
                filename = '%s/%s-%s-%s-%d.%s'\
                    % (datadir, target, localType, dataType, n, filetype)
                job = gevent.spawn(crawl, target=target, localType=localType,\
                    _dataType=dataType, nth=n, filename=filename, encoding=encoding, printer=printer)
                jobs.append(job)

    else:
        if filename_time:
            for n in range(start, end+1):
                filename = '%s/%s-%s-%d-%s.%s'\
                        % (datadir, target, dataType, n, time_string, filetype)
                job = gevent.spawn(crawl, target=target, _dataType=dataType, nth=n,\
                        filename=filename, encoding=encoding, printer=printer)
                jobs.append(job)
        else:
            for n in range(start, end+1):
                filename = '%s/%s-%s-%d.%s'\
                        % (datadir, target, dataType, n, filetype)
                job = gevent.spawn(crawl, target=target, _dataType=dataType, nth=n,\
                        filename=filename, encoding=encoding, printer=printer)
                jobs.append(job)

    gevent.joinall(jobs)
    print('Data written to %s' % filename)

    if interval_time!=0 and interval_time!=None:
        s = sched.scheduler(time.time, time.sleep)
        print('The program will crawl the next data within %d seconds.' % interval_time)
        s.enter(interval_time, 1, print_file, kwargs=dict(arg_namespace=_arg))
        s.run()


def main(args):
    print_file(args)

if __name__ == '__main__':
    monkey.patch_all()
    parser = create_parser()
    args = parser.parse_args()
    main(args)
