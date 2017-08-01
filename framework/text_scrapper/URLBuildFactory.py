import csv
import datetime
import pprint
import sys
import threading
import urlparse
from Queue import Queue
from threading import RLock

from helper import *
from helper import insert_sitemap_url
from helpers.color import Color
from helpers.sitemap_parser import get_sitemap_url
from login import Login
from product_parser import ProductParser
from rules import RuleGenerator
from url_builder import UrlBuilder
from helper import requires_login

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# create a file handler

handler = logging.FileHandler('application.log')
handler.setLevel(logging.DEBUG)

# create a logging format

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger

logger.addHandler(handler)

lock = RLock()


class ProductDownloader(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            url, definitions, writer, br = self.queue.get()
            print("Processing the url : {}".format(url))
            print("Definitions: {}".format(definitions))
            parser = ProductParser(br)
            parser.parse(rule_definitions=definitions, url=url, writer=writer)
            self.queue.task_done()


def main(site_url):
    last_processed = None
    try:
        definitions = RuleGenerator.generate(site_url)
        logger.info("Definition received for : {}".format(site_url))
        # print(Color.green(
        #     "> Definitions Received for {}:".format(site_url)))
        print(pprint.pprint(definitions))

        site_id = get_site_id(site_url)

        logger.info("Extracted Site ID: {}".format(site_id))
        # print("> Site URL: {}".format("www.classichome.com"))

        username, password = get_username(site_id), get_password(site_id)

        logger.info("Username : {}, Password: {}".format(username, password))

        login_form = Login("http://{}".format(site_url), username, password)
        br = login_form.do_login()

        if br is False:
            logger.info("Error username/password invalid")
            print(Color.red("Error-Please check your username and password."))
            raise Exception(
                "Invalid username/password found for {} store.".format(site_url))

        product_parser = ProductParser(br)

        output_filename = "classichome-output-{}.csv".format(
            datetime.date.today())
        # input_filename = os.path.join("filtered_product_urls.csv")

        # input_csv_file = open(input_filename, "r")
        final_csv_file = open(output_filename, "a+")
        writer = csv.writer(final_csv_file)
        queue = Queue()

        for row in get_urls_to_scrape(site_id):
            queue.put((row[0], definitions, writer))

        # for rows in csv.reader(input_csv_file):
        #     queue.put((rows.pop(),definitions, writer))

        count = 0
        THREAD_COUNT = 12
        while queue.qsize():
            for i in xrange(THREAD_COUNT):
                if queue.empty():
                    logger.info("Queue Empty. Nothing to process")
                    # print(Color.red("> Queue Empty. Nothing to process.\n"))
                    sys.exit(0)
                else:
                    url, definitions, writer = queue.get()
                    last_processed = url
                    t = threading.Thread(group=None,
                                         target=product_parser.parse, name=i,
                                         args=(definitions, url, writer))
                    t.start()

                    lock.acquire()
                    count += 1
                    lock.release()

            for t in threading.enumerate():
                if t is not threading.currentThread():
                    t.join()

        logger.info("Total products parsed : {}".format(count))
        print(Color.green("\nTotal products parsed : {}".format(count)))
        # print("Total failed rows: {}".format(len(failed)))
    except KeyboardInterrupt as e:
        print(Color.red("Ctrl+C User Interruped."))
        sys.exit(0)
    except Exception as e:
        logger.error("Exception : {}".format(e.message), exc_info=True)
        print(Color.red("Exceptions: {}".format(e.message)))


def insert_sitemap(sitemap_url):
    site = urlparse.urlparse(sitemap_url)
    try:
        sitemap_data = []
        site_id = get_site_id(site.netloc)

        for url in get_sitemap_url(sitemap_url):
            sitemap_data.append((site_id, url, datetime.date.today(),
                                 "samundra", datetime.date.today(), "samundra"))

        insert_sitemap_url(site_id, sitemap_data)
    except Exception as e:
        raise e


#if __name__ == "__main__":
def GetAllLinks(site_url,login_page, username_field_type = "text" , username_field_name = None,
                output_directory = 'OutputData/', skip_patterns = [],login_is_required = 1, no_of_threads_to_use = 10,
                WaitForUrlResponse_InSeconds = 1000, site_specific_url_extender = ''):
    # print(Color.green("Application Started, Please wait..."))
    import time

    try:
        if login_is_required == 1:
            #print('login start')
            br = requires_login(login_page, username_field_type, username_field_name)
            #br = requires_login(login_page)
            #print('login end')
            if br is False:
                print(Color.red("Error-Please check your username and password."))
                raise Exception("Invalid username/password")

        u = UrlBuilder(br, homepage=site_url, login_page_if_different_to_homepage=login_page,
                       timeout=WaitForUrlResponse_InSeconds)
        #print(type(u))
        #print('UrlBuild obj created sucess')
        u.internal_path_regex = site_url  # searches is only made within this domain

        for pattern in skip_patterns:
            u.reg_skip_url_patterns.append(pattern)

        final_filename = "{}output-UrlLinks-{}-{}".format(output_directory, datetime.date.today(), time.time())
        skip_log_file_filename = "{}SkippedUrls-UrlLinks-{}-{}".format(output_directory, datetime.date.today(), time.time())
        u.generate(final_filename,skip_log_file_filename, thread_count= no_of_threads_to_use,site_specific_url_extender= site_specific_url_extender)
    except KeyboardInterrupt as e:
        print "> Ctrl+C detected. Quit Program."
        sys.exit(0)
    except Exception as e:
        print('Error GetAllLinks function')
        print e.message
        #raise e


# GetAllLinks(site_url="http://www.curreycodealers.com/c-151-Floor-Lamps.aspx",
#             login_page="http://www.curreycodealers.com/wholesale_signin.aspx",
#             output_directory='OutputData/PLD/CurreyNCo/',
#             skip_patterns=['logoff', '#', '.jp', '.pdf'],
#             login_is_required=1,
#             no_of_threads_to_use=10,
#             WaitForUrlResponse_InSeconds=1000
#             )