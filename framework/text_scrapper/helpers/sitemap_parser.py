import urllib
import urllib2

from bs4 import BeautifulSoup

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

def get_sitemap_url(url, default_timeout=300):
    logger.info("Get the Sitemap of {}".format(url))
    try:
        opener = urllib2.urlopen(url=url, data=None, timeout=default_timeout)
        xml = opener.read()
        # fp = open("../../static/sitemap.xml", "r")
        # xml = fp.read()

        soup = BeautifulSoup(markup=xml,features="lxml")

        for tag in soup.find_all("url"):
            for child in tag.children:
                if child.name == "changefreq" and child.text=="daily":
                    loc = child.findPrevious().findPrevious()
                    yield loc.text
    except Exception as e:
        raise e

if __name__=="__main__":
    for url in get_sitemap_url("http://www.classichome.com/sitemap.xml"):
        print url