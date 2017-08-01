import sys

import datetime
import time
from time import gmtime, strftime
from bs4 import BeautifulSoup

import os
import re
from factory_selector import SelectorFactory
import urllib2
from lxml import etree
import csv
import threading
# from gbd_scrapper.rules import definitions
#from helper import get_site_id, get_password,get_username

import csv
## Parser Config Here

debug = 1

class UnknownSelectorError(EnvironmentError):
    def __init__(self):
        pass

class ProductParser:
    def __init__(self, br, NoOfRetries = 0):
        self.br = br
        self.lock = threading.RLock()
        self.NoOfRetries = 0

    def extract_contents(self, selector, alias, default_value, html,tree_object_for_xpath,soup_obj_for_css_regex,thread_id = 0):        
        # making soup object each time, may not be diserable
        #soup = BeautifulSoup(html, "lxml")
        #print("extract_contents called")
        soup = soup_obj_for_css_regex
        #print("extract_contents called")
        tree = tree_object_for_xpath
        parser_logic = SelectorFactory.make(selector)        
        #print("extract_contents called")
        try:            
            #XPATH  .//*[@id='OptionDiv']/div[2]/div/select/option/text()
            if selector == "xpath":                                
                xpathvalues= tree.xpath(alias)
                return xpathvalues;                
            # Regular Expression
            if selector == "regex":
                #print "regex alias: {}".format(alias)                
                regex = re.compile(alias)
                reg_selected_string = regex.findall(html) # Returns the list
                output = default_value
                if len(reg_selected_string) > 0:
                    output = reg_selected_string[0].strip()
                
                return output

            if soup != None:
                method_name = getattr(soup, parser_logic)           
                if method_name is None and selector != "xpath":
                    print "alias: {}".format(alias)
                    regex = re.compile(alias)
                    reg_selected_string = regex.findall(html) # Returns the list
                    output = default_value
                    if len(reg_selected_string) > 0:
                        output = reg_selected_string[0].strip()

                    return output
                else:
                    #print html.findall
                    #print("alias is ::",alias)
                    output = method_name(alias)
                    #print("output is ::", output)
                    if len(output):
                        string = output[0].get_text().strip()
                        return string
                    else:
                        return default_value

        except UnknownSelectorError as e:
            print "UnknownSelector specified"
            raise e

    def parse(self, rule_definitions, url, thread_id = 0,include_only=""):
        try:
            fields = []

            # Get HTML by retrieving the URL
            soup_obj_for_css_regex = None
            # Making tree object for  xpath parsing                                   
            #print("Urllib starts")            
            response = self.br.open(url=url, timeout=200)    
            #print('br opened')
            time.sleep(2)
            #print('response code is',response.code)
            tree_object_for_xpath = etree.parse(response,etree.HTMLParser() ) 
            #print('html text received')
            html = etree.tostring(tree_object_for_xpath)             
            #html = response.read()
            #print("html", html)

            ####### Write html tpo local file disabled for now
            # filename = "static/HtmlPages/" + url.replace('/', '_').replace('\r\n','').replace(':','').replace('.','').replace('?','')+".html"
            # #print('filename is ', filename)
            # writer = open(filename, "wb")
            # writer.write(html)


            for rules in rule_definitions:                
                for column in rules:
                    try:
                        column_name = rules[column]
                        selector = column_name["selector"]
                        alias = column_name["alias"]
                        default_value = column_name["default_value"]
                        #print("selector :: ",selector," alias ::", alias,"default_value:: ", default_value)
                        #print "Thread id ::",thread_id," Extracting :: ",column
                    #   title = rule_definitions[column["selector"]]
                        values = self.extract_contents(selector, alias, default_value, html,tree_object_for_xpath,soup_obj_for_css_regex,thread_id)
                        #print("values is ::",values)
                        fields.append(values)
                        # sys.exit(0)
                    except:
                        print('page scrape for the selector fails')

            return fields
        except Exception as e:
            failed = open("failed.log","a+")
            failed.write("Exception Occured AT: {}".format(url))
            failed.write("Exception Message : {}".format(e.message))
            raise e
            # print "Exception Occurred"
            # raise e
    def ParseAndWrite(self,writer,definitions,url,thread_id, try_attempt = 1):
        try:   
            print('Thread ::',thread_id,'Scraping :: ',url, " Attempt Scrape ::", try_attempt)                                
            field_values = self.parse(definitions, url=url,thread_id = thread_id )
            #print("Scraped Values ::",field_values)
            print('Thread ::',thread_id,"Writing to File")            
            field_values.append(url)            
            self.lock.acquire()            
            writer.writerow(field_values)                    
            self.lock.release()
            print('Thread ::',thread_id," Completed")        
        except Exception as e:        
            if(try_attempt < self.NoOfRetries+1):
                print('Failed Attempt ::',try_attempt,'Thread ::',thread_id,"Failed: {}-404 Not Found".format(url))
                # increase the sleep as the number of retries increases
                time.sleep(try_attempt*2)
                try_attempt += 1
                self.ParseAndWrite(writer,definitions,url,thread_id, try_attempt) 
            else :
                failed = []
                failed.append(url)
                failed_fp = open("failed-{}.csv".format(datetime.date.today()),"a+")
                failed_csv_writer = csv.writer(failed_fp)
                failed_csv_writer.writerow(url)
                print('Thread ::',thread_id,'Failed. Url logged sucessfully') 

def write_header(definitions):
    header = []
    for rules in definitions:
        #print 'rules key',rules.keys()        
        header.append(rules.keys().pop())
    #print 'header is ',header
    return header

def get_browser_object():
    br = mechanize.Browser()
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)
    br.set_handle_robots(False)

    # Browser options
    br.set_handle_equiv(True)
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

    userAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8) AppleWebKit/535.6.2 (KHTML, like Gecko) Version/5.2 Safari/535.6.2'
    br.addheaders = [('User-Agent', userAgent)]
    return br




       

# if __name__=="__main__":
#     import csv
#     from login import Login
#     from rules import RuleGenerator
#     import cookielib
#     import mechanize
#     import threading
#     from Queue import Queue
#     from time import gmtime, strftime

#     br = get_browser_object()
#     main_url = "www.amazon.com"
#     definitions = RuleGenerator.generate(main_url)
#     #print "Definitions Received:"
#     #print definitions   

#     #login_form = Login("http://www.greekgear.com", "", "")
#     #br = login_form.do_login(title_success_login="Regina Andrew")
#     ########################################### NO Login REquired ################################
   
#     product_parser = ProductParser(br)

#     #csv_file = open("../urls-2016-03-14.csv","r")    
#     csv_file = open("../InputData/GreekGear/LinksToParse_GreekGearProductsAtAmazon_Part2.txt","rb")
#     #output_file = "../OutputData/output.csv"
#     output_file = "".join(["../OutputData/",'output-',main_url,"-",strftime("%Y-%m-%d_%H-%M-%S", gmtime()),".csv"])
#     final_csv_file = open(output_file, "wb")  # binary mode to not add extra line breaks between rows in windows  
    

#     writer = csv.writer(final_csv_file)

#     ## Writing header to output file
#     header = write_header(definitions)    
#     writer.writerow(header)
#     #sys.exit(0)
#     q = Queue()
#     # exclusive lock acquired by the main program
    
    

#     failed = []
#     NoOfUrlsToParse = 999999999
#     thread_count = 10

#     for rows in csv.reader(csv_file):
#         if NoOfUrlsToParse > 0:            
#              NoOfUrlsToParse -=1
#              q.put(rows.pop())
#         else:
#             pass

#     lock = threading.Lock()
#     print(q.qsize())

#     try:       
#         while not q.empty():            
#             threads = []
#             for i in range(thread_count):
#                 if q.qsize() > 0:        
#                     #print("sleep starts", strftime("%Y-%m-%d %H:%M:%S", gmtime()))
#                     #time.sleep(2)
#                     #print("sleep ends", strftime("%Y-%m-%d %H:%M:%S", gmtime()))                                 
#                     url = q.get()
#                     t = threading.Thread(name="ParserAndWriter{}".format(i), target = ParseAndWrite, args = (writer,definitions,url,i))                
#                     threads.append(t)
#                     t.start()
#                     print("Starting thread ::", t.getName())
#                     print('in lopp',q.qsize())                    
#                 else:
#                     print("q is empty. no thread started")           
            

#             main_thread = threading.currentThread()   
#             # Wait for all threads to complete except for the main thread
#             for t in threading.enumerate():
#               if t is not main_thread:
#                    t.join()
                
#         print("Main Thread  exits here")

#     except KeyboardInterrupt as e:
#         print "\n> Ctrl+C detected. Quit Program."
#         sys.exit(0)
#     except Exception as e:
#         print("\n> Exception occured: {}".format(e.message))    
        #print("Total failed rows: {}".format(len(failed)))

