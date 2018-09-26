import os
import sys
import argparse
import geojson
import json
import numpy as np
from matplotlib import image


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", type=str, default="GoogleSatellite-x215782-y99255-z18.jpg", help="the base map image")
    parser.add_argument("--bounds", type=str, default="[[39.98553841480973, 116.33148193359375], [39.98659063142852, 116.33285522460938]]", help="the latitude-longitude bounds of the base map image")
    parser.add_argument("--input", type=str, default="input.txt", help="the input file")
    parser.add_argument("--output", type=str, default="output.json", help="the output file")
    parser.add_argument("--input-is-percent", action="store_true", help="whether the input coordinate is percent (or int)")
    args = parser.parse_args()

    image_ = image.imread(args.image)
    image_height, image_width = image_.shape[0], image_.shape[1]
    bounds = json.loads(args.bounds)
    lat_min, lon_min, lat_max, lon_max, lat_span, lon_span = bounds[0][0], bounds[0][1], bounds[1][0], bounds[1][1], (bounds[1][0] - bounds[0][0]), (bounds[1][1] - bounds[0][1])
    input_lines = open(args.input).readlines()  # image coordinate system origin: top left corner, coordinate order: x,y

    feature_collection = geojson.FeatureCollection([geojson.Feature(id=str(i), geometry=geojson.MultiPolygon(json.loads(line))) for i, line in enumerate(input_lines)])
    if args.input_is_percent:
        feature_collection = geojson.utils.map_tuples(lambda c: (lon_min + lon_span * c[0], lat_min + lat_span * (1.0 - c[1])), feature_collection)
    else:
        feature_collection = geojson.utils.map_tuples(lambda c: (lon_min + lon_span * (c[0] / image_width), lat_min + lat_span * (1.0 - c[1] / image_height)), feature_collection)
    open(args.output, "wt").write(geojson.dumps(feature_collection, indent=2))


if __name__ == "__main__":
    main()
