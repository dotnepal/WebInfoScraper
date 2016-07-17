# WebInfoScraper

Implemetation codes only included. Core codes, priorietary to the org and hence is excluded.

1. SiteCrawler : Crawl the site and get all the links in the site. Handles pagination, login, threads with skip patterns that can be  customised during the call.

2. WebInfoRetrriever : Retrieve the product information from the products urls.

          a. Configuration driven information extractor.

          b. Multiple thread support

          c. Can retrieve product information from login required websites.

          d. Login field type and name  can be explicitly supplied, to  uniqiely identify the login forms


3. BulkImageRetriver : Provided a list of images links, download all the images to the destination folder.



