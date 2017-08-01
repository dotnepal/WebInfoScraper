import requests
from pillow import Image
from io import BytesIO
import csv

url = 'http://www.yswhosting.com/sandbox/don/images/padded/phi-delta-theta-tablecloth.jpg'
data = BytesIO(requests.get(url).content)
img = Image.open(data)
print 'a',img.size
output_file = "".join(["../OutputData/GreekGear/",'GreekGear.com-images-size.csv'])
print("output file is ",output_file)
final_csv_file = open(output_file, "wb")  # binary mode to not add extra line breaks between rows in windows  
writer = csv.writer(final_csv_file)
writer.writerow([img.size,url])


# import urllib, cStringIO
# from PIL import Image

# # given an object called 'link'

# #SITE_URL = "http://www.targetsite.com"
# #URL = SITE_URL + link['src']
# # Here's a sample url that works for demo purposes
# URL = "http://www.yswhosting.com/sandbox/don/images/padded/phi-delta-theta-tablecloth.jpg"
# file = cStringIO.StringIO(urllib.urlopen(URL).read())
# im=Image.open(file)
# print(im.size)
#width, height = im.size
