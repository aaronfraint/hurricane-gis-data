from scrape_forecasts import download_zips, extract_zips, cleanup
from import_downloaded_data import import_shapefiles_to_bq
from find_hurricanes_to_scrape import url_for_every_storm

# hurricanes = {
#     # "2012_sandy": "https://www.nhc.noaa.gov/gis/archive_forecast_results.php?id=al18&year=2012&name=Hurricane%20SANDY",
#     # "2017_irma": "https://www.nhc.noaa.gov/gis/archive_forecast_results.php?id=al11&year=2017&name=Hurricane%20IRMA",
#     "2023_idalia": "https://www.nhc.noaa.gov/gis/archive_forecast_results.php?id=al10&year=2023&name=Hurricane%20IDALIA"
# }

if __name__ == "__main__":
    for url in url_for_every_storm():
        print("-" * 40)
        print(url)
        print("-" * 40)

        download_zips(url=url)
        extract_zips()




        # import_shapefiles_to_bq()

    # cleanup()
