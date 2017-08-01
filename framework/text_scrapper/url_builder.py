import cookielib
import os
import urllib2

import datetime
import sys
import threading
import time
import re
from Queue import Queue

import mechanize
from bs4 import BeautifulSoup
import logging
from urlparse import urlparse
#from classichome_login import ClassicHomeLogin
from login import Login
from helpers.logger import AppLogger
from helpers.color import Color
from helper import get_site_id, get_password, get_username
import lxml
from lxml import html
               
class UrlBuilder:
    #self.timeout = 300
    THREAD_COUNT = 8

    def __init__(self,br , homepage, login_page_if_different_to_homepage = None, timeout = 300):
        self.br = br
        o = urlparse(homepage)
        log_filename = o.netloc.replace(".","_")
        #print('log starts at ',"{}-{}-{}.log".format(log_filename, datetime.date.today(),time.time()) )
        try:
            logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:%(asctime)s %(message)s', filename="{}-{}-{}.log".format(log_filename, datetime.date.today(),time.time()))
        except Exception as e:
            print('Log Write failed at Root directory.Check file write permission on the root directory')
            raise e
        #print('log ends')
        self.crawled = set()
        self.added_to_queue = set()
        self.failed = []
        self.timeout = timeout

        self.queue = Queue()
        self.reg_skip_url_patterns = []
        if login_page_if_different_to_homepage == None:
            self.login_page_if_different_to_homepage = login_page_if_different_to_homepage
        else:
            self.login_page_if_different_to_homepage = homepage

        self.reg_skip_url_patterns = [
            '/ajaxcart/index/options/',
            '/media/catalog/product/',
            '/customer/account/',
            '/customer-service/',
            '/account/logout/'
            '/sendfriend/product/send/',
            '/wishlist/index/add/product/',
            '/about-us/news/',
            '/wishlist/index/add/product/',
            'media/catalog/product/cache/',
            'fileuploader/download/download/',
            '/checkout/cart/',
            'shopping-cart',
            '/images',
            '/document',
            '/about',
            '/terms'
            ,'signout','logoff','logout'

        ]
        self._homepage = homepage
        self.internal_path_regex = "{}".format(homepage)
        self.lock = threading.Lock()

        # Browser received via param
        #self.br = mechanize.Browser()
        #self.initialize_browser()

    def initialize_browser(self):
        # self.br = mechanize.Browser()
        cj = cookielib.LWPCookieJar()
        self.br.set_cookiejar(cj)
        self.br.set_handle_robots(False)

        # Browser options
        self.br.set_handle_equiv(True)
        # self.br.set_handle_gzip(True)
        self.br.set_handle_redirect(True)
        self.br.set_handle_referer(True)
        self.br.set_handle_robots(False)
        self.br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

        userAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8) AppleWebKit/535.6.2 (KHTML, like Gecko) Version/5.2 Safari/535.6.2'
        self.br.addheaders = [('User-Agent', userAgent)]

    def find_links(self, url, timeout =300 ):
        try:
            # if self.timeout is None: self.timeout = UrlBuilder.self.timeout
            timeout=60

            # print self.timeout
            #print("Finding links in URL: {}".format(url))
            # print("self.timeout: {}".format(self.timeout))

            response = self.br.open(url=url, data=None, timeout=self.timeout)
            time.sleep(2)
            # response = urllib2.urlopen(url, self.timeout=300)
            if response.code != 200:
                print('Error, response code for rurl reques is',response.code)
            html = response.read()
            #print(html)
            #sys.exit()

            if len(html) < 0 or response.code == 404:
                print("HTML is EMPTY")
                return None
            else:
                tree = lxml.html.fromstring(str(html))
                return(tree.xpath('//a/@href'))
                #sys.exit()        
        except Exception as e:
            raise e
            
    # def requires_login(self, see_text="Logout"):
    #     homepage = urlparse(self._homepage)
    #     site_id = get_site_id(homepage.netloc)
    #     print('site id is ::',site_id, 'home page ::',homepage)
    #     username, password = get_username(site_id), get_password(site_id)
    #     print "> username : {}".format(username)
    #     print "> password : {}".format(password)
    #     login = Login(homepage=self.login_page_if_different_to_homepage,username=username, password=password)
    #     self.br = login.do_login()
    #     return self

    def crawl_page(self, page_url, output_filename, skip_log_file_filename, thread_name, site_specific_url_extender = ''):
        # global seen
        # global queue
        # print page_url
        logging.debug("Crawl page : {}".format(page_url))

        print ("> Crawling URL And Adding it to already crawled list : {}".format(page_url)," START Thread named ", thread_name)
        self.lock.acquire()
        self.crawled.add(page_url)  # mark as self.crawled
        self.lock.release()

        internal_path_regex = re.compile(self.internal_path_regex)

        url = None
        try:
            self.lock.acquire()
            count = 0
            self.lock.release()
            timeout = self.timeout
            url_list = self.find_links(url=page_url, timeout=timeout)
            for url in url_list:                
                processing_url = url
                ## internal links handler
                #print('site extender',site_specific_url_extender)                              
                #print('site extender',site_specific_url_extender)
                _site_specific_url_extender = ''
                if site_specific_url_extender != '':
                    _site_specific_url_extender = '&'+site_specific_url_extender if(self._homepage + url).find('?') >= 0  else '?'+site_specific_url_extender
        
                if url != None and (url+'append/').index('/') == 0:
                    url_splitted = (self._homepage + url).split("/")
                    url = "/".join(sorted(set(url_splitted), key=url_splitted.index))
                    url = url + _site_specific_url_extender
                    #print('Processing url ',processing_url, ' Output Processed URL is ::',url)
              
                self.lock.acquire()
                count += 1
                self.lock.release()

                skip_url = False
                # add to crawl list only if the  url is not in crawled list and  not in added to queue list
                if internal_path_regex.match(url) \
                        and url not in self.crawled \
                        and url not in self.added_to_queue:

                    # Skip certain patterns
                    for reg_pattern in self.reg_skip_url_patterns:
                        # print reg_pattern
                        # print patterns_test[index]
                        regex = re.compile(reg_pattern)
                        # print regex
                        matches = regex.findall(url)

                        # logging.debug("Matches : {}".format(matches))

                        # If found, just skip this URL move to next
                        if len(matches):
                            skip_url = True

                    if skip_url:
                        continue
                    

                    #print("Adding to Crawler queue url ", url)
                    self.lock.acquire()
                    self.queue.put(url)           ## Add to Queue
                    self.added_to_queue.add(url)  ## Mark URL as added to queue
                    self.lock.release()
                    #print("Added to Crawler queue  ", url)

                    #print "> logged to Crawl file url: {}".format(url)
                    logging.debug("> A: {}".format(url))
                    today = datetime.date.today()
                    with open("{}-{}.csv".format(output_filename, today), "a+") as writer:
                        writer.write(url)
                        writer.write("\n")
                        print('Write to file completed for url ::',url, 'SUCCESS at ',output_filename)

                else:
                    pass
                    today = datetime.date.today()
                    #print('Skipped url from crawl queue and file write',url,' at ',skip_log_file_filename)
                    with open("{}-{}.csv".format(skip_log_file_filename, today), "a+") as skip_writer:
                        skip_writer.write(url)
                        skip_writer.write("\n")
                    #print "\n> S:{}".format(url)  # Already processed

        except KeyboardInterrupt as e:
            logging.debug(">System Interrupted by the user, Ctrl+c Detected...")
            print "> Ctrl+C detected. Quit Program."
            sys.exit(0)
        except Exception as e:
            logging.debug("Failed - {}".format(url))
            self.failed.append(url)
            print(e.message)

    def generate(self, filename,skip_log_file_filename, thread_count=THREAD_COUNT, site_specific_url_extender = ''):
        try:
            start_time = time.time()
            print "> Started AT : {}".format(start_time)            
            if site_specific_url_extender == '':
                site_specific_url_extender = ''
            self.crawl_page(self._homepage, filename, skip_log_file_filename,"thread 0 ",site_specific_url_extender)
            total_count = 0

            # thread_count = 8
            while not self.queue.empty():
                # url_to_crawl = queue.get()
                threads = []
                for i in range(thread_count):
                    if self.queue.qsize():
                        page = self.queue.get()
                        t = threading.Thread(name="crawler{}".format(i), target=self.crawl_page, args=(page, filename, skip_log_file_filename,i,site_specific_url_extender) )
                        threads.append(t)
                        t.start()
                    else:
                        print "> Queue Empty. Exit."
                        break

                main_thread = threading.currentThread()
                for t in threading.enumerate():
                    if t is not main_thread:
                        t.join()

                # logging.debug("Threads joined")
                total_count += thread_count
                # end_time = time.time()
            print("> Total URLS Found : {}".format(total_count))
            logging.debug("Total URLS Found : {}".format(total_count))
        except KeyboardInterrupt as e:
            print "> Ctrl+C detected. Quit Program."
            sys.exit(0)
        except Exception as e:
            print("> Exception occured: {}".format(e.message))



if __name__=="__main__":
    try:
        site_url = "www.arteriorshome.com"
        u = UrlBuilder(homepage=site_url)
        u.internal_path_regex = site_url
        u.requires_login()
        final_filename = "arteriors-home-{}-{}".format(datetime.date.today(), time.time())
        u.generate(final_filename, thread_count=10)
    except KeyboardInterrupt as e:
        print "> Ctrl+C detected. Quit Program."
        sys.exit(0)
    except Exception as e:
        print e.message
        raise e