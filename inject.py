#my own shitty sqli injection tool
from urlparse import parse_qs, urlparse , urlsplit
from urllib import urlencode
import requests
import os
import sys
import mechanize
from collections import OrderedDict
import urllib2
from random import choice




scrape_post_urls = []
get_inj_tests = []
basic_sql = "'"
#check multiple values to  strip out duplicate and useless checks
def parse_url(url):
    parsed = urlparse(url,allow_fragments=False)
    
    if parsed.query:
       
        #need to check if only the param is diff if thats the case no need to hit
        if url not in get_inj_tests:
           get_inj_tests.append(url)
      
        
    else:
        if url not in scrape_post_urls:
           scrape_post_urls.append(url)
           
#http://edmundmartin.com/random-user-agent-requests-python/
desktop_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0']
 
def random_headers():
    return {'User-Agent': choice(desktop_agents),'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}          

def requester_get(url_in):
    req = requests.get(url_in,timeout=3,verify=False,headers=random_headers())
    req.encoding      # returns 'utf-8'
    req.status_code   # returns 200
    req.elapsed       # returns datetime.timedelta(0, 1, 666890)
    req.url           # returns url_in
    req.history      
    # returns [<Response [301]>, <Response [301]>]
 
    req.headers['Content-Type']
    # returns 'text/html; charset=utf-8'
    return req.status_code,req.encoding,req.text

def main():
    unparsed_urls = open('in.txt','r')
    for urls in unparsed_urls:
        try:
           parse_url(urls)
        except:
            pass
        
    print(len(scrape_post_urls))
    print(len(get_inj_tests))
    clean_list = list(OrderedDict.fromkeys(get_inj_tests))
    reaasembled_url = ""
   
    for query_test in clean_list:
        print query_test
        url_object = urlparse(query_test,allow_fragments=False)
        #parse query paramaters
        url_query = query_test.split("?")[1].strip()
        #https://stackoverflow.com/questions/50058154/parsing-query-parameters-in-python
        dicty = {x[0] : x[1] for x in [x.split("=") for x in url_query.split("&") ]}
        query_pairs = [(k,v) for k,vlist in dicty.iteritems() for v in vlist]
        reaasembled_url = "http://" + str(url_object.netloc) + str(url_object.path) +  '?'
        
        temp_sqli_query = {}
        #here we will manipulate the url paramters and create a basic vuln scanner
        for k,v in dicty.iteritems():
            print dicty[k]
            entry_data_local = {k:v + basic_sql}
            temp_sqli_query.update(entry_data_local)
        reaasembled_query = urlencode(temp_sqli_query)
        full_url = reaasembled_url + reaasembled_query
        print full_url
        #now we call the sql injection test
        status,encoding,text = requester_get(full_url)
        print status,encoding,text
        
      
       

       
       
        
main()

