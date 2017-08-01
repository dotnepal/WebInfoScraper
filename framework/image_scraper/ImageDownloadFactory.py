#-------------------------------------------------------------------------------------
#-- Object Name         : ImageDownloader 
#-- Project             : 
#-- Business Process    : Downloads the image
#-- REquirements		: 
#--------------------------------------------------------------------------------------
#-- Developer           : Binaya Budathoki
#-- Changed By          : Bikal Basnet
#-- Change Summary      : Wrapped into SPOC (Single Point of Contact + Classes implementation)
#--------------------------------------------------------------------------------------

import os
import thread
from cl_ImageDownloader import ImageDownloader
import csv
import time
import sys

def createDir(dirname):
    if not os.path.exists(dirname):
        try:
            os.makedirs(dirname)
        except:
            print 'Unable to create directory'
            sys.exit(0)


def startImageDownloader(base_dir='../InputData/PLD/CurreyNCo',
                  file_containing_links_of_images_to_dowload = None,
                  image_output_dirname='../OutputData/PLD/CurreyNCo/Images',
                  no_of_threads=10,
                  get_image_size_only=0,
                  NoOfRetries=0,
                  output_file_to_write_image_sizes=None #'../OutputData/GreekGear/GreekGear.com-images-size.csv'
                  ):
        print('call starts')
        dirname = image_output_dirname
        #createDir(image_output_dirname)
        if output_file_to_write_image_sizes == None:
            output_file_to_write_image_sizes = image_output_dirname +'/'+str(time.time()).replace('.','') + 'image-size.csv'
        final_csv_file = open(output_file_to_write_image_sizes,"wb")  # binary mode to not add extra line breaks between rows in windows
        print('file opened')
        writer = csv.writer(final_csv_file)
        log_file_fail = 'log_fail'
        log_file_sucess = 'log_success'
        f_open_sucess = open(log_file_sucess, 'w')
        f_open_fail = open(log_file_fail, 'w')
        print('object initialisation starts')
        img_downloader = ImageDownloader (base_dir = base_dir, #'../InputData/PLD/CurreyNCo',
                                          image_output_dirname=image_output_dirname, #'../OutputData/PLD/CurreyNCo/Images',
                                          no_of_threads = no_of_threads, #10,
                                          get_image_size_only = get_image_size_only, #0,
                                          NoOfRetries= NoOfRetries, #0,
                                          #output_file_to_write_image_sizes = output_file_to_write_image_sizes,  #'../OutputData/GreekGear/GreekGear.com-images-size.csv',
                                          output_file_to_write_image_sizes = output_file_to_write_image_sizes, #'../OutputData/GreekGear/GreekGear.com-images-size.csv',
                                          writer = writer,
                                          log_file_sucess_obj = f_open_sucess,
                                          log_file_fail_obj = f_open_fail
                                          )
        #crosswalkFileName()
        print('object initialisation ends')
        urlList = []
        for path, subdirs, files in os.walk(base_dir):
            print('path ', path,' subdir ', subdirs)
            for name in files:
                fname = os.path.join(path, name)
                print('walkng filename ', name,'. file_containing_links_of_images_to_dowload ', file_containing_links_of_images_to_dowload)
                if name == file_containing_links_of_images_to_dowload or file_containing_links_of_images_to_dowload == None:
                    try:
                        fobj = open(fname)
                        for url in fobj.readlines():
                            print('url is ::',url," ")
                            if not os.path.isfile(dirname+'/'+name):
                                tmp = [url.strip().replace('"', '')]
                                print("temp name is ",tmp)
                                urlList.extend(tmp)
                        fobj.close()
                        print(urlList)
                    except Exception, e:
                        print str(e)
                        print 'Unable to Open File, exiting'
                        exit(0)
                else:
                    print('Escaping reading links from file', name)

        #Creating the home_page directory
        createDir(dirname)

        #Finding the range to distribute the URL's to each of the threads
        urlRange = abs(len(urlList) / no_of_threads)


        for i in range(no_of_threads):
            thread.start_new_thread(img_downloader.assignJob, (i, urlRange, urlList, get_image_size_only, writer))

        img_downloader.check_lock()

        f_open_fail.close()
        f_open_sucess.close()

        final_csv_file.close()

# startImageDownloader (base_dir = '../InputData/PLD/CurreyNCo',
# 			  image_output_dirname='../OutputData/PLD/CurreyNCo/Images',
# 			  no_of_threads = 2,
# 			  get_image_size_only = 0,
# 			  NoOfRetries=0,
# 			  #output_file_to_write_image_sizes = '../OutputData/GreekGear/GreekGear.com-images-size.csv'
# 			  );
# img_downloader.startDownload()