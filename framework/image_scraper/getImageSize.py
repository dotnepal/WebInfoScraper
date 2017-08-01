import os
from PIL import Image
import csv

base_dir = '../OutputData/GreekGear/Images'

output_file = "".join(["../OutputData/GreekGear/",'GreekGear.com-images-at-amazon-size.csv'])
final_csv_file = open(output_file, "wb")  # binary mode to not add extra line breaks between rows in windows  
writer = csv.writer(final_csv_file)

for path, subdirs, files in os.walk(base_dir):
	for name in files:
		fname = os.path.join(path, name)
		img = Image.open(fname);
		row = str(img.size)+","+fname
		print(row)
		#print(type(row))
		writer.writerow([img.size,name])
		
		#print img.size
		#print fname
final_csv_file.close()