from image_scraper.ImageDownloadFactory import startImageDownloader; \
startImageDownloader(base_dir = "InputData",\
           image_output_dirname="OutputData/Images",\
           no_of_threads = 3,\
           get_image_size_only = 0,\
           NoOfRetries=10\
           )

