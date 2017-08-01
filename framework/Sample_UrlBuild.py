from gbd_scrapper.URLBuildFactory import GetAllLinks
GetAllLinks(site_url="https://www.samplesite.com/wholesale/",
            login_page="https://www.samplesite.com/wholesale/customer/account/login/",
            username_field_name = "login[username]" ,
            output_directory='OutputData/Sample/',
            skip_patterns=['logout','logoff','#','.jp','.pdf'],
            login_is_required=1,
            no_of_threads_to_use=10,
            WaitForUrlResponse_InSeconds=1000
            ,site_specific_url_extender = 'limit=all'
            )