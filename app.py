import streamlit as st
import folium
from pathlib import Path
import base64
from folium import plugins
from streamlit_folium import folium_static
from PIL import Image
from map import create_marker, build_map

image_metas = [{'name': 'IMG_20211010_073341857.jpg',
  'file_path': Path('static/img_raw/IMG_20211010_073341857.jpg'),
  'date_time': '2021:10:10 07:33:42',
  'coords': (46.53272076953131, 10.4564773259075)},
 {'name': 'IMG_20210808_180600573_HDR.jpg',
  'file_path': Path('static/img_raw/IMG_20210808_180600573_HDR.jpg'),
  'date_time': '2021:08:08 18:06:01',
  'coords': (52.50884144964325, 13.315151544679624)},
 {'name': 'IMG_20211012_153240955_HDR.jpg',
  'file_path': Path('static/img_raw/IMG_20211012_153240955_HDR.jpg'),
  'date_time': '2021:10:12 15:32:42',
  'coords': (45.06943700016987, 3.8560897329403305)},
 {'name': 'IMG_20211004_172556086_HDR.jpg',
  'file_path': Path('static/img_raw/IMG_20211004_172556086_HDR.jpg'),
  'date_time': '2021:10:04 17:25:57',
  'coords': (51.38657248001801, 9.453412013471558)},
 {'name': 'IMG_20211010_183748956_HDR.jpg',
  'file_path': Path('static/img_raw/IMG_20211010_183748956_HDR.jpg'),
  'date_time': '2021:10:10 18:37:50',
  'coords': (44.926597, 6.693246)},
 {'name': 'IMG_20211009_115723871_HDR.jpg',
  'file_path': Path('static/img_raw/IMG_20211009_115723871_HDR.jpg'),
  'date_time': '2021:10:09 11:57:25',
  'coords': (47.340200458524414, 10.202968583188209)},
 {'name': 'IMG_20211010_073954163.jpg',
  'file_path': Path('static/img_raw/IMG_20211010_073954163.jpg'),
  'date_time': '2021:10:10 07:39:54',
  'coords': (46.63272076953131, 10.5564773259075)}]

sorted_image_metas = sorted(image_metas, key=lambda x: x['date_time'])

st.set_page_config(layout="wide")

# @st.cache
# def load_image(image_file):
# 	img = Image.open(image_file)
# 	return img

st.title('Nomad Tracks')

markers = [create_marker(image_meta) for image_meta in sorted_image_metas]
m = build_map(markers)
folium_static(m, width=m.width[0], height=m.height[0])
st.sidebar.title('Add Step')
st.sidebar.text_input('Title')
st.sidebar.text_input('Longitude, Latitude (e.g.: "52.5207, 13.3751"')
st.sidebar.date_input('Date')

st.sidebar.text_area("Comment")
# st.sidebar.multiselect("Tags")

image_file = st.sidebar.file_uploader("Upload Image", type=['png', 'jpeg', 'jpg'])
if image_file is not None:
    import exif

    img = exif.Image(image_file)
    st.sidebar.write(img.datetime)
    st.sidebar.write(img.gps_latitude)
    st.sidebar.write(img.gps_longitude)