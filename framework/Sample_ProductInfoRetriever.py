 from gbd_scrapper.ProductInfoRetrieverFactory import GetAllProductInformation
GetAllProductInformation(NoOfUrlsToParse=200,
                         thread_count=10,
                         site_url_as_in_db='www.samplesite.com',
                         login_page="https://www.samplesite.com/wholesale/customer/account/login",
                         #username_field_type="email",
                         username_field_name='login[username]' ,
                         no_of_retries_to_scrape_a_product=0,
                         file_containing_product_links="OutputData/ProductsToScrape.csv",
                         output_file_path="OutputData/Output-ProductDetails"
                         )