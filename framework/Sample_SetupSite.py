from Source.framework.gbd_scrapper.helper import SetupSite; \
SetupSite(site = "www.SampleSite.com", \
username = "None", \
password =  "None")

from Source.framework.gbd_scrapper.URLBuildFactory import GetAllLinks;
GetAllLinks(site_url="http://www.SampleSite.com", \
            login_page="http://www.SampleSite.com", \
            username_field_type=None, \
            username_field_name=None, \
            output_directory="../../OutputData/Chad/SampleSite",  \
            skip_patterns=["logoff","#",".jp",".pdf"], \
            login_is_required=0, \
no_of_threads_to_use=10, \
WaitForUrlResponse_InSeconds=1000, \
site_specific_url_extender = "" \
)




from Source.framework.gbd_scrapper.helper import insert_scrape_key; \
insert_scrape_key(site = "www.SampleSite.com", \
                  Key_Alias = "First_Level_Category", \
                  Key_Name = ".//*[@id=\"c21714\"]/div/div/div/div[1]/div/div[1]/div[1]/a[2]/text()", \
                  Key_DefaultValue = "NA", \
                  Scrape_Scheme = "xpath" );\
insert_scrape_key(site = "www.SampleSite.com", \
                  Key_Alias = "Second_Level_Category", \
                  Key_Name = ".//*[@id=\"c21714\"]/div/div/div/div[1]/div/div[1]/div[1]/a[3]/text()", \
                  Key_DefaultValue = "NA", \
                  Scrape_Scheme = "xpath" );\



from Source.framework.gbd_scrapper.ProductInfoRetrieverFactory import GetAllProductInformation; \
GetAllProductInformation(NoOfUrlsToParse=10000, \
                         thread_count=10, \
                         site_url_as_in_db="www.SampleSite.com", \
                         login_page=None, \
                         username_field_type= None, \
                         username_field_name=None , \
                         no_of_retries_to_scrape_a_product=0, \
                         file_containing_product_links="../../OutputData/Chad/SampleSiteoutput-UrlLinks-2016-06-14-1465905926.92", \
                         output_file_path="../../OutputData/Chad/SampleSite/Data/Output-SampleSite-Simple-SAMPLE.csv" \
                         )


#Image Downloader

# python -c'from image_scraper.ImageDownloadFactory import startImageDownloader; \
# startImageDownloader(base_dir = "InputData/Chad/SampleSite/ImageLinks",\
#            image_output_dirname="OutputData/Chad/SampleSite/Images",\
#            no_of_threads = 10,\
#            get_image_size_only = 0,\
#            NoOfRetries=0\
#            );

