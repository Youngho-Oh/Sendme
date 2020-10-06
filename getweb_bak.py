#!/usr/bin/python

import sys
import requests
import shutil
from HTMLParser import HTMLParser
import time
import csv
from parse import *

class MyHTMLParser(HTMLParser):
    is_print = 0

    def handle_starttag(self, tag, attrs):
        '''if tag == "th" :
            MyHTMLParser.is_print = 1
        elif tag == "tr" :
            MyHTMLParser.is_print = 1
        elif tag == "td" :
            MyHTMLParser.is_print = 1'''
        if tag == "div" and attrs[0] == "id" and attrs[1] == "Lead-3-QuoteHeader-Proxy" :
            MyHTMLParser.is_print = 1
            print "aaa"

        if MyHTMLParser.is_print == 1 :
            print "Encountered a start tag:",tag

    def handle_endtag(self, tag):
        if MyHTMLParser.is_print == 1 :
            print "Encountered an end tag:",tag
            MyHTMLParser.is_print = 0

    def handle_data(self, data):
        if MyHTMLParser.is_print == 1 :
            print "Encountered some data:",data

def data_parse(string):
    parser = MyHTMLParser()
    parser.feed(string)
    #print("end")

def get_current_time():
    secs = time.time()
    print(secs)

def find_tbody_tag(save_list, name, string):
    start = string.find("class=\"Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)")

    end = start+200
  
    # current rate
    string = string[start:end]
    
    start = string.find("data-reactid=\"32\">")+18

    string = string[start:end]
    currate_end = string.find("</span>")
    currate = string[:currate_end]

    currate_start = currate.find("\"")+1
    currate = currate[currate_start:currate_end]
    temp_end = currate.find("\"")
    currate = currate[currate_start:temp_end]

    #print currate
    start = currate_end+7

    # differancial number
    string = string[start:end]
    
    start = string.find("data-reactid=\"33\">")+18

    string = string[start:end]
    currate_end = string.find("</span>")
    string_temp = string[:currate_end]
    #print string_temp

    diffrate_start = string_temp.find("(")+1
    diffrate_end = string_temp.find(")")

    diff = string_temp[:diffrate_start-1]
    #print diff
    diff_rate = string_temp[diffrate_start:diffrate_end]
    #print diff_rate

    curtime = time.time()
    save_list.append([curtime, name, currate, diff, diff_rate])

    #print save_list
    return save_list

def get_file_data() :
    f = open('/home/pi/Study/gcloud/getweb_list', 'rt')

    data = f.readlines()
    f.close()
    return data

def get_web(url):
    result = requests.get(url)
    #print(result.text)
    #res = reuqests.get(url, stream=True)
    text = (result.text).encode('utf-8')

    #print(text)
    return text

def save_csv(save_data):
    with open('/home/pi/Study/gcloud/finance.csv', 'a') as f:
        wt = csv.writer(f)
        wt.writerows(save_data)

def main(method, length):
    #print(method[1])
    #url = "https://finance.yahoo.com/quote/%5EIXIC/history?period1=867715200&period2=1583020800&interval=1d&filter=history&frequency=1d"
    #file_name = "KS11"

    num_query = 0

    if length == 2 :
        num_query = int(sys.argv[1])

    url_list = get_file_data()
    save_list = []
 
    for_count = 1

    for i in url_list:
        #print for_count
        if (num_query == 0) or (for_count == num_query) :
            print(i)
            result = parse("{name} {url}", i)
            print result['name']
            print result['url']
            save_list = find_tbody_tag(save_list, result['name'], get_web(result['url']))
            #data_parse(find_tbody_tag(get_web(result['url'])))
        for_count = for_count + 1

    print save_list
    save_csv(save_list)

if __name__ == '__main__' :
    #if len(sys.argv) >= 3 :
        #print(len(sys.argv))
        get_current_time()
        main(sys.argv, len(sys.argv))
