import pandas as pd
import geopandas as gpd
from _params import LOCAL_EXTRACTED_FOLDER


def merge_shapefiles(shape_type="lin"):
    """
    Merge all shapefiles of a single geometry type
    """

    all_gdfs = []

    polygon_shapes = sorted(list(LOCAL_EXTRACTED_FOLDER.rglob(f"*{shape_type}.shp")))

    total = len(polygon_shapes)
    counter = 0.0

    for shp in polygon_shapes:
        counter += 1
        if counter % 100 == 0:
            print(f"#{counter}, {counter / total * 100}% complete")
        try:
            all_gdfs.append(gpd.read_file(shp))
        except Exception as e:
            print(e)

    print("Merging into one file")
    merged_gdf = gpd.GeoDataFrame(pd.concat(all_gdfs, ignore_index=True))

    merged_gdf.to_file(f"merged_{shape_type}.shp")


if __name__ == "__main__":
    merge_shapefiles()
