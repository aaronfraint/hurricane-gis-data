import sys

from _scrape_forecasts import download_zips, extract_all_zip_files
from _import_downloaded_data import import_shapefile_to_bq
from _find_hurricanes_to_scrape import url_for_every_storm
from _merge_shapefiles import merge_shapefiles


def main(args):
    process = args[1]

    if process == "download":
        for url in url_for_every_storm():
            print("-" * 40)
            print(url)
            print("-" * 40)

            download_zips(url=url)

    elif process == "extract":
        extract_all_zip_files()

    elif process == "merge":
        merge_shapefiles(shape_type=args[2])

    elif process == "bq":
        import_shapefile_to_bq("merged_pgn.shp")


if __name__ == "__main__":
    main(sys.argv)
