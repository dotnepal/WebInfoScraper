import cookielib
import logging
import os

import mechanize
import sys

from helpers.color import Color
from helpers.logger import AppLogger


class StaticPageMissingError(Exception):
    pass


class Login:
    def __init__(self, homepage, username, password, username_field_type = "text",username_field_name = None):
        self.logger = AppLogger(homepage).get_logger(logging.INFO)
        # self.logger
        self.homepage = homepage
        self.username = username
        self.password = password
        self.username_field_type = username_field_type
        self.username_field_name = username_field_name
        self.login_success_page_static_html = os.path.join("static", "_login_success.html")

        if not os.path.exists(self.login_success_page_static_html):
            f = open(self.login_success_page_static_html, "w")
            f.close()
            print "> Create file : {}".format(self.login_success_page_static_html)
            raise StaticPageMissingError(self.login_success_page_static_html)

        self.homepage_static_html = os.path.join("static", "_homepage.html")

        if not os.path.exists(self.homepage_static_html):
            f = open(self.homepage_static_html, "w")
            f.close()
            print "> Create file : {}".format(self.homepage_static_html)
            raise StaticPageMissingError(self.homepage_static_html)

        self.logout_selector = "div.block-content ul li.logout > a"
        print('login obj created sucessfully')

    def create_html(self, page, contents):
        self.logger.info("Page saved to - {}".format(Color.yellow(page)))
        #w = open("{}".format(page), "w+")
        #w.write(contents)
        #w.close()

    def do_login(self):
        # AppLogger.log("Try to login inside {}".format(self.homepage))
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
        browser.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

        userAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8) AppleWebKit/535.6.2 (KHTML, like Gecko) Version/5.2 Safari/535.6.2'
        browser.addheaders = [('User-Agent', userAgent)]
        # username, password = self.config.get_login_params()

        try:
            print self.homepage
            response = browser.open(self.homepage, timeout=300)
            response_html = response.read()

            self.create_html(self.homepage_static_html, response_html)
            print('login status page written to ',self.homepage_static_html)

            if response.code is 200:
                #login_form = list(browser.forms())[0]
                ## Iterate over all the forms available in the page, to get the right form which has the username_field_name
                login_form = None
                for CurForm in list(browser.forms()):
                    cur_login_form = CurForm
                    for control in cur_login_form.controls:
                        if control.name == self.username_field_name:
                            login_form = cur_login_form

               # print('Login form is',login_form)
                #print(list(browser.forms()))
                if login_form == None:
                    login_form = list(browser.forms())[0]

                login_field_name, password_field_name = None, None

                for control in login_form.controls:
                    field_type = control.type
                    field_name = control.name

                    #print('a',self.username_field_type, self.username_field_name)
                    #if field_type == "text":                    
                    if ( field_type == self.username_field_type  and self.username_field_name == None  ) or (  field_type == self.username_field_type and field_name == self.username_field_name ):
                        #print ("found name text field login_field_name ",login_field_name,' field_name ',field_name)
                        login_field_name = field_name

                    if field_type == "password":
                        #print "found password field"
                        password_field_name = field_name

                    #print ("login_field_name ", login_field_name, ' field_name ', field_name)

                #browser.select_form(nr=0)
                #browser.form = list(browser.forms())[0]

                #browser.select_form(nr=2)
                #browser.form = list(browser.forms())[2]
                browser.form = login_form
                #print(browser)
                #print('browser.form is', browser.form)
                #print('hello1 login_field_name ',login_field_name,' password_field_name ', password_field_name)
                browser.form[login_field_name] = self.username
                browser.form[password_field_name] = self.password

                browser.method = "POST"
                browser.action = login_form.action

                status = browser.submit()

                response_info = response.info()
                #print response_info

                doc = status.read()

                self.create_html(self.login_success_page_static_html, doc)

                # AppLogger.log("title_success_login={}".format(title_success_login))
                # AppLogger.log("Login Complete")

                if browser is not None:
                    print('SUCESS : LOGIN SUCESS')
                    return browser
                else:
                    print('ERROR : LOGIN FAILED')
                    return False
                    # self.log_to_file("Did not received good response during login")

        except Exception as e:
            # self.log_to_file("Exception Occurred during login with message {}".format(e.message))
            raise e

    @staticmethod
    def verify_login(html, title_text):
        AppLogger.log("Inside the login module verify_login")
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, "lxml")

        for anchor in soup.select("div.header-top-right li.first > a"):
            title = anchor.get("title")
            expected_message = str(title).strip()
            actual_message = str(title_text)

            return bool(expected_message == actual_message)
