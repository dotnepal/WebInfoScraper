from helper import *
from helper import get_browser_object
from helper import requires_login
from rules import RuleGenerator
import gbd_scrapper.product_parser
#from gbd_scrapper.product_parser_Bikal  import ParseAndWrite
from gbd_scrapper.product_parser import ProductParser
#from login import Login
from Queue import Queue
from time import gmtime, strftime
import sys
import csv
import threading

#if __name__=="__main__":
def GetAllProductInformation(NoOfUrlsToParse = 2, thread_count = 4, site_url_as_in_db = 'www.arteriorshome.com' , login_page = None ,
                             username_field_type = "text" , username_field_name = None
                                , no_of_retries_to_scrape_a_product = 0 , file_containing_product_links = "InputData/PLD/Arteriors/LinksToParse_Arteriors.txt",
                             output_file_path = "OutputData/PLD/Arteriors/Output-Arteriors-ProductDetails"   ):

    NoOfUrlsToParse = NoOfUrlsToParse #99999
    thread_count = thread_count #10

    br = get_browser_object()
    main_url = site_url_as_in_db #"www.arteriorshome.com"
    definitions = RuleGenerator.generate(main_url)
    print('definitions is', definitions);
    if login_page != None:
        br = requires_login(login_page, username_field_type, username_field_name )
    if br is False:
            print("Error-Please check your username and password.")
            raise Exception("Invalid username/password found")

    product_parser = ProductParser(br,no_of_retries_to_scrape_a_product)
    csv_file = open(file_containing_product_links,"rb")
    output_file = "".join([output_file_path,main_url,"-",strftime("%Y-%m-%d_%H-%M-%S", gmtime()),".csv"])
    final_csv_file = open(output_file, "wb")  # binary mode to not add extra line breaks between rows in windows  
    
    writer = csv.writer(final_csv_file)

    ## Writing header to output file
    header = write_header(definitions)    
    writer.writerow(header)
    #sys.exit(0)
    q = Queue()
    failed = []
    unique_lines = []
    for line in csv_file: #csv.reader(csv_file):
        if line in unique_lines:
            pass
        else:                        
            unique_lines.append(line)
            if NoOfUrlsToParse > 0:            
                NoOfUrlsToParse -=1
                #print(line)
                if line: 
                   #outFile.write(line)
                   q.put(line)      
            else:
                pass

    #outFile.close()
    #sys.exit()

    lock = threading.Lock()
    print(q.qsize())

    try:       
        while not q.empty():            
            threads = []
            for i in range(thread_count):
                if q.qsize() > 0:        
                    #print("sleep starts", strftime("%Y-%m-%d %H:%M:%S", gmtime()))
                    #time.sleep(2)
                    #print("sleep ends", strftime("%Y-%m-%d %H:%M:%S", gmtime()))                                 
                    url = q.get()
                    t = threading.Thread(name="ParserAndWriter{}".format(i), 
                                    target = product_parser.ParseAndWrite, 
                                    args = (writer,definitions,url,i,1))                
                    threads.append(t)
                    t.start()
                    print("Starting thread ::", t.getName())
                    print('in lopp',q.qsize())                    
                else:
                    print("q is empty. no thread started")           
            

            main_thread = threading.currentThread()   
            # Wait for all threads to complete except for the main thread
            for t in threading.enumerate():
              if t is not main_thread:
                   t.join()
                
        print("Main Thread  exits here")

    except KeyboardInterrupt as e:
        print "\n> Ctrl+C detected. Quit Program."
        sys.exit(0)
    except Exception as e:
        print("\n> Exception occured: {}".format(e.message))


