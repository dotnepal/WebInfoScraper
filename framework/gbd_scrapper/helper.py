import cookielib

import mechanize

from database import db_configuration
import mysql.connector
from mysql.connector import errorcode

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

'''
Creating Directory
'''

def get_site_id(domain_name):
    try:
        cnx = mysql.connector.connect(**db_configuration)

        cursor = cnx.cursor()
        query = ("SELECT Id, DomainName, SitemapUrl, CreateDate, CreateUser, "
                 "UpdateDate, UpdateUser from Site "
                 "WHERE DomainName Like \"%{}%\"".format(domain_name))

        cursor.execute(query)

        print cursor._executed

        site_id = None
        for (id, domain_name, sitemap_url, create_date, create_user,
             update_date, update_user) in cursor:
            site_id = id
            # cursor.close()
            # cnx.close()
            return site_id
            # print("{}, {}, {}".format(id, domain_name, sitemap_url))

        # cursor.close()
        # cnx.close()
        #
        # if site_id is not None:
        #     return site_id

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cnx.close()


def get_username(site_id):
    try:
        cnx = mysql.connector.connect(**db_configuration)

        cursor = cnx.cursor()
        query = ("SELECT Id, KeyValue, CreateDate, CreateUser, UpdateDate, "
                 "UpdateUser from SiteLogin "
                 "WHERE SiteId in (%(SiteId)s) AND KeyName='username'")

        cursor.execute(query,({"SiteId":site_id}))

        # print cursor._executed

        site_id = None
        for (id, key_value, create_date, create_user, update_date,
             update_user) in cursor:
            return key_value

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cursor.close()
        cnx.close()


def has_authentication(site_id):
    username, password = get_username(site_id), get_password(site_id)
    return bool(username and password)


def get_password(site_id):
    try:
        cnx = mysql.connector.connect(**db_configuration)

        cursor = cnx.cursor()
        query = ("SELECT Id, KeyValue, CreateDate, CreateUser, UpdateDate, "
                 "UpdateUser from SiteLogin "
                 "WHERE SiteId in (%(SiteId)s) AND KeyName='password'")

        cursor.execute(query,({"SiteId": site_id}))

        # print cursor._executed

        site_id = None
        for (id, key_value, create_date, create_user, update_date,
             update_user) in cursor:
            return key_value

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cursor.close()
        cnx.close()


def get_default_browser():
    """
    :return Returns the fresh mechanize browser object
    """
    browser = mechanize.Browser()
    cj = cookielib.LWPCookieJar()
    browser.set_cookiejar(cj)
    browser.set_handle_robots(False)

    # Browser options
    browser.set_handle_equiv(True)
    # browser.set_handle_gzip(True)
    browser.set_handle_redirect(True)
    browser.set_handle_referer(True)
    browser.set_handle_robots(False)
    browser.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(),
                               max_time=1)

    userAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8) ' \
                'AppleWebKit/535.6.2 (KHTML, like Gecko) ' \
                'Version/5.2 Safari/535.6.2'
    browser.addheaders = [('User-Agent', userAgent)]
    return browser


def get_output_filename(site_id):
    try:
        cnx = mysql.connector.connect(**db_configuration)

        cursor = cnx.cursor()
        query = ("SELECT Id, IXCode, SiteId, StartDate, EndDate, Occurance, "
                 "OccuranceType, Active "
                 "from Schedule "
                 "WHERE SiteId in (%(SiteId)s) "
                 "Order by CreateDate, StartDate LIMIT 0, 1")

        cursor.execute(query,({"SiteId":site_id}))
        print cursor._executed

        # print cursor._executed

        for(id, ix_code, site_id, start_date, end_date, occurance,
            occurance_type, active_status) in cursor:
            print(id, site_id, start_date, end_date, occurance,
                  occurance_type, active_status)
            return ix_code
            # return key_value

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cursor.close()
        cnx.close()

def get_urls_to_scrape(site_id):
    try:
        cnx = mysql.connector.connect(**db_configuration)

        cursor = cnx.cursor()
        query = ("SELECT URL "
                 "from SiteScrapeURL "
                 "WHERE SiteId in (%(SiteId)s) ")

        cursor.execute(query,({"SiteId":site_id}))

        # print cursor._executed

        for (url) in cursor:
            yield url
            # return key_value

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cursor.close()
        cnx.close()

def insert_sitemap_url(site_id, data):
    try:
        cnx = mysql.connector.connect(**db_configuration)

        cursor = cnx.cursor()
        # username = "samundra"
        # site_id = get_site_id("www.classichome.com")
        logger.info("Delete sitemap entries for Site ID: {}".format(site_id))
        cursor.execute("DELETE FROM SiteScrapeURL WHERE SiteId in (%(SiteId)s)",
                       ({"SiteId":site_id}))
        logger.info("Completed Sitemap Deleted completed.");
        logger.debug("SQL: {}".format(cursor._executed))

        logger.info("start sitemap insert query.")
        cursor.executemany("INSERT INTO SiteScrapeURL (SiteId, URL, CreateDate, "
                           "CreateUser, UpdateDate, UpdateUser) "
                           "VALUES (%s, %s, %s, %s, %s, %s)", data)
        logger.info("sitemap insert completed.")
        cnx.commit()
        cursor.close()
        cnx.close()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cnx.close()

import urlparse
import sys
from login import Login
def requires_login(login_page, username_field_type = "text",username_field_name = None, see_text="Logout"):
    try:
        login_page_parsed = urlparse.urlparse(login_page)        
        site_id = get_site_id(login_page_parsed.netloc)
        print('site id is ::',site_id, 'login page ::',login_page)
        username, password = get_username(site_id), get_password(site_id)
        print "> username : {}".format(username)
        print "> password : {}".format(password)
        login = Login(homepage=login_page,username=username, password=password, username_field_type = username_field_type, username_field_name = username_field_name )
        print('do login func call starts')
        br = login.do_login()
        print('do login func call starts1')
        return br
        #print('do login func call starts2')
    except:
        print('helper.requires_login1 fails')
        sys.exit()

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