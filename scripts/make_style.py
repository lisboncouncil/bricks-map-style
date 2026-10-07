"""Build the BRICKS MapLibre style.

Usage: python3 scripts/make_style.py [GLYPHS_URL_TEMPLATE] [OUTPUT]
Style design: CC BY 4.0, The Lisbon Council 2026. Script: MIT.
"""
import json, sys

GLYPHS = sys.argv[1] if len(sys.argv) > 1 else 'https://lisboncouncil.github.io/bricks-map-style/fonts/{fontstack}/{range}.pbf'
OUT = sys.argv[2] if len(sys.argv) > 2 else 'style/bricks-style.json'

C = {
    'bg': '#fbf8fd',          # land
    'land2': '#f6f0fa',       # residential tint
    'park': '#e2f6e9',        # green tint of #34ea82
    'wood': '#d8f1e1',
    'water': '#e6d9f6',       # lilac water
    'water_line': '#d3bdf0',
    'building': '#f2eaf8',
    'building_line': '#e8dcf1',
    'road': '#ffffff',
    'road_casing': '#e4d7ef',
    'major_casing': '#cdb8e8',
    'path': '#d9c9ea',
    'rail': '#cbb7e3',
    'boundary': '#b8a3dc',
    'ink': '#1d1d1b',
    'text': '#3a3640',
    'text_soft': '#6d6577',
    'water_text': '#5a4fd6',
    'violet': '#4935ea',
    'halo': '#fbf8fd',
}
SANS = ['Source Sans 3 Regular']
SANS_B = ['Source Sans 3 SemiBold']
VIOLET_SOFT = '#7a6ae6'
ARC_B = ['Archivo Bold']
ARC_XB = ['Archivo ExtraBold']
NAME = ['coalesce', ['get', 'name:en'], ['get', 'name:latin'], ['get', 'name']]
LOCAL = ['coalesce', ['get', 'name:latin'], ['get', 'name']]


def z(*stops):
    out = ['interpolate', ['exponential', 1.4], ['zoom']]
    for a, b in stops:
        out += [a, b]
    return out


def cls(*names):
    return ['match', ['get', 'class'], list(names), True, False]


not_brunnel_tunnel = ['!=', ['get', 'brunnel'], 'tunnel']
L = []
L.append({'id': 'background', 'type': 'background', 'paint': {'background-color': C['bg']}})
L.append({'id': 'landuse-residential', 'type': 'fill', 'source': 'omt', 'source-layer': 'landuse', 'filter': cls('residential', 'suburb', 'neighbourhood'), 'paint': {'fill-color': C['land2'], 'fill-opacity': z((10, 0), (13, 1))}})
L.append({'id': 'landcover-wood', 'type': 'fill', 'source': 'omt', 'source-layer': 'landcover', 'filter': cls('wood', 'forest'), 'paint': {'fill-color': C['wood'], 'fill-opacity': 0.8}})
L.append({'id': 'landcover-grass', 'type': 'fill', 'source': 'omt', 'source-layer': 'landcover', 'filter': cls('grass', 'farmland', 'wetland'), 'paint': {'fill-color': C['park'], 'fill-opacity': 0.55}})
L.append({'id': 'park', 'type': 'fill', 'source': 'omt', 'source-layer': 'park', 'paint': {'fill-color': C['park']}})
L.append({'id': 'landuse-green', 'type': 'fill', 'source': 'omt', 'source-layer': 'landuse', 'filter': cls('cemetery', 'pitch', 'stadium', 'playground', 'garden'), 'paint': {'fill-color': C['park']}})
L.append({'id': 'water', 'type': 'fill', 'source': 'omt', 'source-layer': 'water', 'filter': not_brunnel_tunnel, 'paint': {'fill-color': C['water']}})
L.append({'id': 'waterway', 'type': 'line', 'source': 'omt', 'source-layer': 'waterway', 'filter': not_brunnel_tunnel, 'paint': {'line-color': C['water_line'], 'line-width': z((8, 0.5), (14, 2), (18, 6))}})
L.append({'id': 'aeroway', 'type': 'fill', 'source': 'omt', 'source-layer': 'aeroway', 'minzoom': 11, 'filter': ['match', ['geometry-type'], ['Polygon', 'MultiPolygon'], True, False], 'paint': {'fill-color': C['land2']}})

# roads
groups = [
    ('path', ['path', 'pedestrian', 'track'], 14, (14, 0.6), (18, 2.5), None),
    ('service', ['service'], 14, (14, 1), (18, 7), (14, 1.6)),
    ('minor', ['minor', 'street', 'street_limited'], 12, (12, 0.6), (18, 14), (12, 1.2)),
    ('secondary', ['secondary', 'tertiary'], 9, (9, 0.6), (18, 20), (9, 1.4)),
    ('primary', ['primary', 'trunk'], 7, (7, 0.8), (18, 24), (7, 1.6)),
    ('motorway', ['motorway'], 5, (5, 0.8), (18, 26), (5, 1.8)),
]
for name, classes, mz, w0, w1, c0 in groups:
    if c0 is None:
        continue
    casing = C['major_casing'] if name in ('primary', 'motorway') else C['road_casing']
    L.append({'id': f'road-{name}-casing', 'type': 'line', 'source': 'omt', 'source-layer': 'transportation', 'minzoom': mz,
              'filter': ['all', not_brunnel_tunnel, cls(*classes)], 'layout': {'line-cap': 'round', 'line-join': 'round'},
              'paint': {'line-color': casing, 'line-width': z(c0, (w1[0], w1[1] + 3))}})
L.append({'id': 'rail', 'type': 'line', 'source': 'omt', 'source-layer': 'transportation', 'minzoom': 11,
          'filter': ['all', not_brunnel_tunnel, cls('rail', 'transit')], 'paint': {'line-color': C['rail'], 'line-width': z((11, 0.6), (18, 2)), 'line-dasharray': [3, 2]}})
for name, classes, mz, w0, w1, c0 in groups:
    paint = {'line-color': C['path'] if name == 'path' else C['road'], 'line-width': z(w0, w1)}
    if name == 'path':
        paint['line-dasharray'] = [1.5, 1.5]
    L.append({'id': f'road-{name}', 'type': 'line', 'source': 'omt', 'source-layer': 'transportation', 'minzoom': mz,
              'filter': ['all', not_brunnel_tunnel, cls(*classes)], 'layout': {'line-cap': 'round', 'line-join': 'round'}, 'paint': paint})

L.append({'id': 'building', 'type': 'fill', 'source': 'omt', 'source-layer': 'building', 'minzoom': 14,
          'paint': {'fill-color': C['building'], 'fill-outline-color': C['building_line'], 'fill-opacity': z((14, 0), (15, 1))}})
L.append({'id': 'boundary-admin', 'type': 'line', 'source': 'omt', 'source-layer': 'boundary', 'filter': ['all', ['>=', ['get', 'admin_level'], 3], ['<=', ['get', 'admin_level'], 4], ['!=', ['get', 'maritime'], 1]],
          'paint': {'line-color': C['boundary'], 'line-opacity': 0.5, 'line-width': z((4, 0.4), (10, 1)), 'line-dasharray': [2, 2]}})
L.append({'id': 'boundary-country', 'type': 'line', 'source': 'omt', 'source-layer': 'boundary', 'filter': ['all', ['==', ['get', 'admin_level'], 2], ['!=', ['get', 'maritime'], 1], ['!=', ['get', 'disputed'], 1]],
          'paint': {'line-color': C['boundary'], 'line-width': z((2, 0.6), (8, 1.6)), 'line-dasharray': [4, 2]}})

# labels
def sym(id, src, flt, font, size, color, extra_layout=None, extra_paint=None, minzoom=None, maxzoom=None):
    lay = {'text-field': NAME, 'text-font': font, 'text-size': size}
    if extra_layout:
        lay.update(extra_layout)
    paint = {'text-color': color, 'text-halo-color': C['halo'], 'text-halo-width': 1.6, 'text-halo-blur': 0.4}
    if extra_paint:
        paint.update(extra_paint)
    d = {'id': id, 'type': 'symbol', 'source': 'omt', 'source-layer': src, 'layout': lay, 'paint': paint}
    if flt is not None:
        d['filter'] = flt
    if minzoom is not None:
        d['minzoom'] = minzoom
    if maxzoom is not None:
        d['maxzoom'] = maxzoom
    return d

L.append(sym('waterway-label', 'waterway', ['match', ['geometry-type'], ['LineString', 'MultiLineString'], True, False], SANS, z((12, 11), (18, 15)), C['water_text'], {'symbol-placement': 'line', 'text-letter-spacing': 0.1}, minzoom=12))
L.append(sym('water-label', 'water_name', None, SANS, z((4, 11), (14, 15)), C['water_text'], {'text-letter-spacing': 0.12, 'text-max-width': 6}))
L.append(sym('street-label', 'transportation_name', cls('minor', 'street', 'secondary', 'tertiary', 'primary', 'trunk'), SANS, z((13, 11), (18, 15)), C['text_soft'],
             {'symbol-placement': 'line', 'text-rotation-alignment': 'map', 'text-field': LOCAL}, minzoom=13))
L.append(sym('park-label', 'poi', cls('park'), SANS, 12.5, '#2c7a4b', {'text-max-width': 8}, minzoom=15))
L.append(sym('place-neighbourhood', 'place', cls('neighbourhood', 'quarter', 'suburb'), SANS_B, z((11, 10.5), (16, 13)), C['text_soft'],
             {'text-transform': 'uppercase', 'text-letter-spacing': 0.14, 'text-max-width': 7}, minzoom=11, maxzoom=17))
L.append(sym('place-village', 'place', cls('village', 'hamlet'), SANS_B, z((9, 11), (14, 14)), C['text'], {'text-max-width': 8}, minzoom=9))
L.append(sym('place-town', 'place', cls('town'), SANS_B, z((7, 11.5), (13, 16)), C['text'], {'text-max-width': 8}, minzoom=7))
L.append(sym('place-city', 'place', cls('city'), ARC_B, z((4, 12), (8, 16), (13, 22)), C['ink'], {'text-max-width': 8, 'symbol-sort-key': ['get', 'rank']}, maxzoom=15))
L.append(sym('place-country', 'place', cls('country'), ARC_B, z((2, 9.5), (6, 13)), VIOLET_SOFT, {'text-transform': 'uppercase', 'text-letter-spacing': 0.18, 'text-max-width': 6}, {'text-opacity': 0.85}, maxzoom=8))

style = {
    'version': 8,
    'name': 'BRICKS',
    'metadata': {'bricks:palette': 'Lilac #dec0f1, Violet #7161ef, Pink #ff285e, Green #34ea82, Yellow #fff35e', 'bricks:schema': 'OpenMapTiles', 'license': 'CC BY 4.0, The Lisbon Council 2026 (https://creativecommons.org/licenses/by/4.0/)'},
    'glyphs': GLYPHS,
    'sources': {'omt': {'type': 'vector', 'url': 'https://tiles.openfreemap.org/planet', 'attribution': '<a href="https://openfreemap.org" target="_blank">OpenFreeMap</a> © <a href="https://www.openmaptiles.org/" target="_blank">OpenMapTiles</a> Data from <a href="https://www.openstreetmap.org/copyright" target="_blank">OpenStreetMap</a>'}},
    'layers': L,
}
json.dump(style, open(OUT, 'w'), indent=1, ensure_ascii=False)
print(OUT, len(L), 'layers')
