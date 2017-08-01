#!/usr/bin/python
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

'''
getURL reads URL from a external File sends a http
request and writes the response inside the home_page folder which
is created at the current active directory.
NOTE: Set MAXTHREADS to the number of CPU cores that your machine has for optimal performance
'''

import urllib2
import os
import thread
import os.path
import time
import requests
from PIL import Image
from io import BytesIO
import csv



class ImageDownloader():
    def __init__(self, base_dir = '../InputData/GreekGear/GreekGearProductImages',
              image_output_dirname='../OutputData/GreekGear/GreekGearWebsiteImages',
              no_of_threads = 10,
              get_image_size_only = 0,
              NoOfRetries=0,
              output_file_to_write_image_sizes = None,
              writer = None,
              log_file_sucess_obj = None,
              log_file_fail_obj = None
                 ):
        if output_file_to_write_image_sizes == None:
            output_file_to_write_image_sizes = image_output_dirname + '/' + str(time.time()).replace('.','') + 'image-size.csv'

        global dirname
        self.base_dir = base_dir;
        #fname = 'greekgear_images.txt' #File name which stores various URL's
        dirname = image_output_dirname # '../OutputData/GreekGear/GreekGearWebsiteImages' #Name of the directory to be created, to store the downloaded images
        #crosswalk = 'greekgear_images.txt' #Crosswalk file to track the updated id

        self.MAXTHREADS = no_of_threads # 10 #Max number of threads to be created
        self.NoOfRetries = NoOfRetries
        self.get_image_size_only = get_image_size_only
        if writer == None:
            self.output_file = output_file_to_write_image_sizes #"".join(["../OutputData/GreekGear/",'GreekGear.com-images-size.csv'])
            self.final_csv_file = open(self.output_file, "wb")  # binary mode to not add extra line breaks between rows in windows
            self.writer = csv.writer(self.final_csv_file)
        self.cw_lookup = dict()
        self.writelock = thread.allocate_lock()
        self.exitlock = [thread.allocate_lock() for i in range(self.MAXTHREADS)]
        self.f_open_sucess = log_file_sucess_obj #open(log_file_sucess, 'w')
        self.f_open_fail = log_file_fail_obj #open(log_file_fail, 'w')
        #print('init sucess')


    '''
    #Making sure the parent thread runs as long as the child threads are running
    '''

    def check_lock(self):
        # type: () -> object
        for mutex in self.exitlock:
            while not mutex.locked(): pass

    '''
    Assigns Job to the threads that are created
    '''
    def assignJob(self, i, urlRange, urlList, get_image_size_only, writer):
        #1. Split the urls into the range
        #2. Download the content for that range
        #3. If i is MAXTHREADS have to reconsider the last remaining URL's as well

        startPos = i * urlRange
        endPos = startPos + urlRange

        for pos in range(startPos, endPos):
            #Get the url and pass it to fetchContent()
            self.fetchContent(urlList[pos],0,get_image_size_only, writer,i)

        if(i == self.MAXTHREADS-1):
            for pos in range(endPos, len(urlList)):
                self.fetchContent(urlList[pos],0,get_image_size_only, writer,i)


        self.exitlock[i].acquire()


    '''
    Fetch the content of the individual URL's
    '''
    def fetchContent(self, url,try_attempt = 1, get_image_size_only = 0,writer= None, i = None):
        self.writelock.acquire()
        print 'Thread ->'+str(i)+' Fetching => ' + url+' get image size only =>'+str(get_image_size_only)
        self.writelock.release()
        try:
            if get_image_size_only == 1:
                self.writeResponseToFile(None, url,get_image_size_only ,writer)
            else:
                if 'http://' not in url:
                    url = 'http://'+url
                #print('1row is')
                req = urllib2.Request(url)
                #print('2row is')
                response = urllib2.urlopen(req)
                #time.sleep(1)
                #img = Image.open(url)
                #row = str(img.size)+","+self.fname
                #print('3row is')
                self.writeResponseToFile(response, url,get_image_size_only ,writer)
        except:
            if(try_attempt < self.NoOfRetries+1):
                print('Failed Attempt ::',try_attempt,"Failed fetching images  {}".format(url))
                # increase the sleep as the number of retries increases
                time.sleep(try_attempt*2)
                try_attempt += 1
                self.fetchContent(url,try_attempt,get_image_size_only,writer,i)
            else:
                self.writelock.acquire()
                print 'Unable to Fetch => ' + url
                self.f_open_fail.write(url + '\n')
                self.writelock.release()

    '''
    Get the correct id from the crosswalk file
    '''
    def crosswalkFileName(self):
        try:
            fobj = open(self.crosswalk)

            for cw_line in [line.strip() for line in fobj.readlines()]:
                new_id, old_id = cw_line.split('\t')
                self.cw_lookup[old_id] = new_id

            fobj.close()
        except Exception, e:
            print e
            print 'Unable to Open File, exiting'
            exit(0)


    def writeImageToFile(self, response, url):
        print("writing Image")
        #print(url.split('/').pop().split('.jpg'))
        #id = url.split('/').pop().split('.')[0]
        id = url.split('/').pop()
        #filename = cw_lookup[id]
        filename = id #+ '.jpg'
        self.writelock.acquire()
        try:
            fobj = open(os.path.join(dirname, filename), 'wb')
            fobj.write(response.read())
            fobj.close
            self.f_open_sucess.write(url + '\n')
        except:
            print 'Unable to Write to File'
        self.writelock.release()

    def writeImageSizeToFile(self, url, get_image_size_only, writer):
        try:
            data = BytesIO(requests.get(url).content)
            img = Image.open(data)
            self.writelock.acquire()
            writer.writerow([img.size,url])
            self.writelock.release()
        except:
            print 'Unable to Write image size of the Image', url


    '''
    Writing the HTTP response to the file
    '''
    def writeResponseToFile(self, response, url, get_image_size_only, writer):
        if get_image_size_only == 1:
            self.writeImageSizeToFile(url, get_image_size_only, writer)
        else :
            self.writeImageToFile(response, url)






