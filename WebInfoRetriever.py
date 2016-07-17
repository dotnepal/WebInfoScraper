from gbd_scrapper.helper import insert_scrape_key; \
insert_scrape_key(site = "www.knixxxxx.com", \
                  Key_Alias = "First_Level_Category", \
                  Key_Name = ".//*[@id=\"c21714\"]/div/div/div/div[1]/div/div[1]/div[1]/a[2]/text()", \
                  Key_DefaultValue = "NA", \
                  Scrape_Scheme = "xpath" );\
insert_scrape_key(site = "www.knixxxxx.com", \
                  Key_Alias = "Second_Level_Category", \
                  Key_Name = ".//*[@id=\"c21714\"]/div/div/div/div[1]/div/div[1]/div[1]/a[3]/text()", \
                  Key_DefaultValue = "NA", \
                  Scrape_Scheme = "xpath" );\
insert_scrape_key(site = "www.knixxxxx.com", \
                  Key_Alias = "Product Name1_Grouped", \
                  Key_Name = ".//*[@id=\"View-PL\"]/div[1]/strong[1]/text()", \
                  Key_DefaultValue = "NA", \
                  Scrape_Scheme = "xpath" );\
insert_scrape_key(site = "www.knixxxxx.com", \
                  Key_Alias = "Product Name2_Grouped", \
                  Key_Name = ".//*[@id=\"View-PL\"]/div[1]/strong[2]/text()", \
                  Key_DefaultValue = "NA", \
                  Scrape_Scheme = "xpath" );\

				  
from gbd_scrapper.ProductInfoRetrieverFactory import GetAllProductInformation; \
GetAllProductInformation(NoOfUrlsToParse=10000, \
                          thread_count=10, \
                          site_url_as_in_db="www.knixxxxx.com", \
                          login_page=None, \
                          username_field_type= None, \
                          username_field_name=None , \
                          no_of_retries_to_scrape_a_product=0, \
                          file_containing_product_links="ds_scrapper/InputData/Chad/knixxxxx/URL/dupdataurls.csv", \
                          output_file_path="OutputData/Chad/knixxxxx/Data/Output-knixxxxx-Simple-Dup-datas-push-2016-05-30.csv" \
                          )


