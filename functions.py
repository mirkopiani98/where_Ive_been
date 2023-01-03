from fractions import Fraction
import piexif
from datetime import datetime
from PIL import Image
from PIL.ExifTags import GPSTAGS
from PIL.ExifTags import TAGS


def get_DD_lat_long(filename):
    '''
    :param filename: image path filename
    :return: latitude and longitude
    '''

    def get_exif(filename):
        try:
            image = Image.open(filename)
            image.verify()  # verify that it is, in fact an image
            exif = image._getexif()
            if exif == None:
                pass
                # raise ValueError("No EXIF metadata found")
            else:
                return image._getexif()
        except (IOError, SyntaxError) as e:
            print('Bad file:', filename)  # print out the names of corrupt files
            pass

    def get_labeled_exif(exif):
        labeled = {}
        for (key, val) in exif.items():
            labeled[TAGS.get(key)] = val
        return labeled

    def get_geotagging(exif):
        if exif == None:
            pass
            #raise ValueError("No EXIF metadata found")
        else:
            geotagging = {}
            for (idx, tag) in TAGS.items():
                if tag == 'GPSInfo':
                    if idx not in exif:
                        continue
                        #raise ValueError("No EXIF geotagging found")
                    for (key, val) in GPSTAGS.items():
                        if key in exif[idx]:
                            geotagging[val] = exif[idx][key]
            return geotagging

    def get_decimal_from_dms(dms, ref):
        degrees = dms[0]
        minutes = dms[1]/ 60.0
        seconds = dms[2]/ 3600.0
        if ref in ['S', 'W']:
            degrees = -degrees
            minutes = -minutes
            seconds = -seconds
        return round(degrees + minutes + seconds, 5)

    def get_coordinates(geotags):
        if geotags == None or geotags == {}:
            pass
        else:
            if 'GPSLatitude' in geotags and 'GPSLongitude' in geotags:
                lat = get_decimal_from_dms(geotags['GPSLatitude'], geotags['GPSLatitudeRef'])
                lon = get_decimal_from_dms(geotags['GPSLongitude'], geotags['GPSLongitudeRef'])
                return (lat, lon)
            else:
                pass

    exif = get_exif(filename)
    geotags = get_geotagging(exif)
    #print(get_coordinates(geotags))
    coord = get_coordinates(geotags)
    if coord == None:
        pass
    else:
        lat = coord[0]
        long = coord[1]
        return lat,long



def get_image_date(path):
    '''
    :param path: image path filename
    :return: day and time when image was taken
    '''
    try:
        image = Image.open(path)
        image.verify()  # verify that it is, in fact an image
        exif = image._getexif()
        if exif == None:
            pass
            # raise ValueError("No EXIF metadata found")
        else:
            for (idx, tag) in TAGS.items():
                if tag == 'DateTimeOriginal':
                    if idx not in exif:
                        continue
                        # raise ValueError("No EXIF geotagging found")
                    else:
                        day_time = Image.open(path)._getexif()[36867]
                        datetime_obj = datetime.strptime(day_time, '%Y:%m:%d %H:%M:%S')
                        return datetime_obj
    except (IOError, SyntaxError) as e:
        print('Bad file:', path)  # print out the names of corrupt files
        pass