from image_scraper.ImageDownloadFactory import startImageDownloader
startImageDownloader (base_dir = 'InputData/PLD/SampleSite/ImagesLinks',
			  image_output_dirname='OutputData/PLD/SampleSite/Images',
			  no_of_threads = 10,
			  get_image_size_only = 0,
			  NoOfRetries=0 ,			  
			  );