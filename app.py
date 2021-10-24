from pathlib import Path
from datetime import datetime

import streamlit as st
from streamlit_folium import folium_static
from pydantic.error_wrappers import ValidationError

from data_models import Step
from map import create_marker, build_map
from image_utils import extract_meta, save_image


_IMG_SRC = Path('static/img_raw')

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

for var_name in ['step_title', 'step_coords', 'step_date', 'step_desc']:
    if var_name not in st.session_state:
        st.session_state[var_name] = '' if var_name != 'step_date' else None

image_file = st.sidebar.file_uploader("Upload Image", type=['png', 'jpeg', 'jpg'])
if image_file is not None:
    meta = extract_meta(image_file)
    st.session_state.step_coords = meta['coordinates']
    st.session_state.step_date = meta['date_time']


st.session_state.step_title = st.sidebar.text_input('Title', st.session_state.step_title)
st.session_state.step_coords = st.sidebar.text_input('Longitude, Latitude (e.g.: "52.5207, 13.3751"',
                                                     st.session_state.step_coords)
st.session_state.step_date = st.sidebar.date_input('Date', st.session_state.step_date)
st.session_state.step_desc = st.sidebar.text_area("Comment", st.session_state.step_desc)


def save_step(title, coordinates, date_time, desc):
    # Mock function write to DB instead
    long, lat = coordinates.split(', ')
    step = Step(title=title, long=long, lat=lat, date_time=datetime.combine(date_time, datetime.min.time()),
                description=desc)
    print(step.dict())


if st.sidebar.button("Save Step"):
    try:
        save_image(image_file, _IMG_SRC)

        save_step(st.session_state.step_title,
                  st.session_state.step_coords,
                  st.session_state.step_date,
                  st.session_state.step_desc)
        st.write('Success')
    except (ValidationError, ValueError) as e:
        print(repr(e))
        st.sidebar.warning("Please Enter Coordinates!")

