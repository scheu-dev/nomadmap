import folium

from PIL import Image as PILImage
import base64

from image_utils import resize_image, image_to_byte_array


def create_marker(image_meta: dict, target_width=250) -> folium.Marker:
    with PILImage.open(image_meta['file_path']) as img:
        _format = img.format
        img = resize_image(img, target_width)
        img_byte_arr = image_to_byte_array(img, _format)
        encoded = base64.b64encode(img_byte_arr)

    html = '<img src="data:image/JPG;base64,{}">'.format
    iframe = folium.IFrame(html(encoded.decode("UTF-8")), width=target_width +20, height=target_width +20)
    popup = folium.Popup(iframe, max_width=2000, show=False)

    icon = folium.Icon(color="blue", icon="truck", prefix='fa')
    marker = folium.Marker(location=image_meta['coords'], popup=popup, icon=icon)
    return marker


def build_map(markers):
    route_lats_longs = [marker.location for marker in markers]

    lats = [coord[0] for coord in route_lats_longs]
    longs = [coord[1] for coord in route_lats_longs]
    #     lat_center = sum([coord[0] for coord in route_lats_longs])/len(route_lats_longs)
    #     long_center = sum([coord[1] for coord in route_lats_longs])/len(route_lats_longs)
    lat_center = (max(lats) + min(lats)) / 2
    long_center = (max(longs) + min(longs)) / 2

    m = folium.Map(location=(lat_center, long_center),
                   zoom_start=6, width=1200, height=675, control_scale=True,
                   tiles='Stamen Watercolor')
    for marker in markers:
        m.add_child(marker)

    folium.plugins.AntPath(route_lats_longs, paused=True).add_to(m)
    return m

