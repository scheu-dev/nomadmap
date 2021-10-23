from exif import Image as EXIFImage
from PIL import Image as PILImage
import io

def resize_image(img: PILImage, basewidth: int=250, target_path: str='img_resized'):
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth,hsize), PILImage.ANTIALIAS)
    return img

def image_to_byte_array(image:PILImage, _format):
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format=_format)
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr

def extract_meta(image_file):
    img = EXIFImage(image_file)
    meta = {
        'date_time': image_datetime(img),
        'coordinates': image_coordinates(img)
    }
    return meta

def decimal_coords(coords, ref):
    decimal_degrees = coords[0] + coords[1] / 60 + coords[2] / 3600
    if ref == "S" or ref == "W":
        decimal_degrees = -decimal_degrees
    return decimal_degrees

def image_coordinates(img):
    coords = None, None
    if img.has_exif:
        try:
            coords = (decimal_coords(img.gps_latitude, img.gps_latitude_ref),
                      decimal_coords(img.gps_longitude, img.gps_longitude_ref))
        except AttributeError:
            print('No Coordinates')
    else:
        print('The Image has no EXIF information')
    return coords

def image_datetime(img):
    dt = None
    if img.has_exif:
        try:
            dt = img.datetime_original
        except AttributeError:
            print('No Datetime')
    else:
        print('The Image has no EXIF information')
    return dt