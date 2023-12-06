import pandas as pd
import geopandas as gpd
import json
import shapely
from shapely.validation import make_valid
from google.cloud import bigquery

from _params import LOCAL_EXTRACTED_FOLDER

BQ_DATASET = "hackathon_workflows_2023"

SHAPE_TYPES = ["lin", "pts", "pgn", "wwlin"]


def _shapefiles_to_convert():
    """
    Get a dictionary of all shapefiles to be imported, organized by geometry type
    """

    shapefiles = {x: [] for x in SHAPE_TYPES}

    for shp in sorted(list(LOCAL_EXTRACTED_FOLDER.rglob("*.shp"))):
        data_type = shp.stem.split("_")[-1]

        # Some dates have two files, one ending in 'A'. Let's omit those
        if "A" not in shp.stem.split("_")[-1].upper():
            shapefiles[data_type].append(shp)

    return shapefiles


def _get_schema(df):
    """
    Convert dataframe schema to BQ schema
    """
    type_dict = {
        "b": "BOOLEAN",
        "i": "INTEGER",
        "f": "FLOAT",
        "O": "STRING",
        "S": "STRING",
        "U": "STRING",
    }
    schema = [
        {
            "name": col_name,
            "type": "GEOGRAPHY"
            if col_name == "geometry"
            else type_dict.get(col_type.kind, "STRING"),
        }
        for (col_name, col_type) in df.dtypes.items()
    ]
    return schema


def _convert_gdf_to_json(df):
    """
    Convert geodataframe to JSON representation
    """
    return pd.DataFrame(
        {
            col: (
                df[col]
                if col != "geometry"
                else df[col].map(
                    lambda x: json.dumps(shapely.geometry.mapping(make_valid(x)))
                )
            )
            for col in df
        }
    )


def import_shapefiles_to_bq():
    """
    Import the polygon, point, and line shapefiles to BQ
    """
    client = bigquery.Client()

    shapefiles = _shapefiles_to_convert()

    for shape_type in SHAPE_TYPES:
        if shape_type == "wwlin":
            break

        print("-" * 40)
        print(shape_type)
        print("-" * 40)

        table_id = f"{BQ_DATASET}.noaa_advisory_{shape_type}"

        for shp in shapefiles[shape_type]:
            print(shp)

            try:
                df = gpd.read_file(shp)

                schema = _get_schema(df)

                df_json = _convert_gdf_to_json(df)

                job_config = bigquery.LoadJobConfig(schema=schema)

                job = client.load_table_from_dataframe(
                    df_json, table_id, job_config=job_config
                )
                job.result()

            except Exception as e:
                print(e)
