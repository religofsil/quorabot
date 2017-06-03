#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 24 04:17:51 2017

@author: algernon
"""

import time
import urllib, json
import lxml.html as parser

headers = {"UserAgent": "Mozilla 5.0"}


def open_page(url):
    req = urllib.request.Request(url, data=None, headers=headers)
    f = urllib.request.urlopen(req)
    a = f.read()
    f.close()
    return a


def parse_question(page):
    d = {}
    html = parser.fromstring(page)
    d['topic'] = [i.text_content() for i in html.xpath('//span[@class="TopicNameSpan TopicName"]')]
    d['q'] = [i.text_content() for i in html.xpath('//h1')]
    d['a'] = [i.text_content() for i in html.xpath('//div[@class="layout_2col_main"]/div[5]//*[contains(@class,"qtext")]')]
    return d


def parse_numpage(page):
    arr = []
    html = parser.fromstring(page)
    links = html.xpath('//div/div/a')
    for link in links:
        d = {}
        d['link'] = link.get('href')
        d['q'] = link.text_content()
        if 'unanswered' not in d['link']:
            arr.append(d)
    # print(arr)
    return arr


def main():
    f = open('i.jl', 'a')
    for i in range(30, 601):
        time.sleep(.01)
        print(i)
        page = open_page('https://www.quora.com/sitemap/questions?page_id='+str(i))
        qs = parse_numpage(page)
        for q in qs[4:]:
            time.sleep(.001)
            try:
                q_page = open_page(q['link'])
                qa = parse_question(q_page)
                line = json.dumps(qa) + '\n'
                f.write(line)
            except:
                print('ERROR: ', q)
    f.close()


main()
