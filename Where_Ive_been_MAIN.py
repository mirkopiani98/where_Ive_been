import os, csv, pandas as pd
from functions import get_image_date, get_DD_lat_long


files_path = input("Paste photos' directory (\"C:\User\...\...\"): ")

# list to store images fns
file_names_list = []
# list to store images
images_to_analyse = []


count = 0
# iterate over your whole directory and subdirectory to find out JPGs
for path, subdirs, files in os.walk(files_path):
    for name in files:
        if name.endswith('.jpg') or name.endswith('.JPG'):
            file_names_list.append(name)
            file_and_path = os.path.join(path, name)
            images_to_analyse.append(file_and_path)
            count = count +1

print("number of images to analyse: ", count)

# create your database
csv_file_name = "Where I've been.csv"
csv_file = open(csv_file_name,"w")
headerList = ["Date", "Lon", "Lat", "Image name"]
dw = csv.DictWriter(csv_file, delimiter= ",", fieldnames=headerList)
dw.writeheader()
csv_file.close()

# add images with GPS metadata to the database
for image in images_to_analyse:
    for name in file_names_list:
        if image.find(name) != -1:  # -1 means no match found, otherwise the int gives the match beginning
            # get image date
	    day = get_image_date(image)
	    # get image GPS coordinates in WGS84 Datum (EPSG: 4326)
            GPScoord = get_DD_lat_long(image)

            if day == None or GPScoord == None:
                pass
            else:
                csv_file = open(csv_file_name,"a")
                csv_file.write(str(day)+","+str(GPScoord[1])+","+str(GPScoord[0])+","+str(name)+"\n")
                csv_file.close()
        else:
            pass

#sort all csv_file images by date

df = pd.read_csv(csv_file_name, names = ["Date","Lon","Lat","Image name"], sep = ",", parse_dates= ["Date"])
df.sort_values(["Date"], inplace = True)
