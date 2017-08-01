import threading
from Queue import Queue
import time


def ParseAndWrite(url, thread_id):
	time.sleep(1)
	print("Running Thread ::",thread_id," UrlId::",url)	

q = Queue()
NoOfUrlsToParse = 3 #9999999999
thread_count = 2
urlId =500
for rows in  range(1,1000):
    if NoOfUrlsToParse > 0:            
         NoOfUrlsToParse -=1
         urlId += 1
         q.put(urlId)
    else:
        pass

lock = threading.Lock()
print(q.qsize())


try:            
    while not q.empty():        
        threads = []
        for i in range(thread_count):
        	if q.qsize() > 0:
	            url = q.get()
	            print(url, q.qsize())            
	            t = threading.Thread(name="ParserAndWriter{}".format(i), target = ParseAndWrite, args = (url, i))                
	            threads.append(t)
	            t.start()
	            print("Starting thread ::", t.getName())
	            print('in lopp',q.qsize())
	        else:
	        	print("q is empty. no thread started")

            #t.join()     
        

        main_thread = threading.currentThread()   
        # Wait for all threads to complete before stopping execution
        print(" main thread in called thread",main_thread )
        for t in threading.enumerate():
          	if t is not main_thread:
          		t.join(1) # waits for all child threads to terminate
          		#print("joining thread :: ", t.getName())

        print(threading.activeCount())  		

                
    print("Main Thread destroyed")

except KeyboardInterrupt as e:
    print "\n> Ctrl+C detected. Quit Program."
    sys.exit(0)
except Exception as e:
    print("\n> Exception occured: {}".format(e.message))