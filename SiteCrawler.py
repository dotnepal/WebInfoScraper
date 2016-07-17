from gbd_scrapper.helper import SetupSite; \
SetupSite(site = "www.knixxxxx.com", \
username = "None", \
password =  "None")

from gbd_scrapper.URLBuildFactory import GetAllLinks;
GetAllLinks(site_url="http://www.knixxxxx.com", \
            login_page="http://www.knixxxxx.com", \
            username_field_type=None, \
            username_field_name=None, \
            output_directory="OutputData/Chad/knixxxxx",  \
            skip_patterns=["logoff","#",".jp",".pdf"], \
            login_is_required=0, \
no_of_threads_to_use=10, \
WaitForUrlResponse_InSeconds=1000, \
site_specific_url_extender = "" \
)


