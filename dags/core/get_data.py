
import os
import pandas as pd
from airflow.decorators import task
import os


CITIES_DATA_PATH = os.getenv('AIRFLOW_VAR_CITIES_DATA_PATH')
PROVINCES_DATA_PATH = os.getenv('AIRFLOW_VAR_PROVINCES_DATA_PATH')
REGIONS_DATA_PATH = os.getenv('AIRFLOW_VAR_REGIONS_DATA_PATH')
METEO_DATA_PATH = os.getenv('AIRFLOW_VAR_METEO_DATA_PATH')

@task
def get_cities():
    df_cities = pd.read_csv(CITIES_DATA_PATH, sep=';')
    df_cities = df_cities.drop_duplicates()
    df_cities = df_cities.fillna('')
    df_cities['lat'] = df_cities['lat'].str.replace(',', '.').astype(float)
    df_cities['lon'] = df_cities['lon'].str.replace(',', '.').astype(float)
    df_cities['superficie_kmq'] = df_cities['superficie_kmq'].str.replace(',', '.').astype(float)

    return df_cities


@task
def get_provinces():
    df_province = pd.read_json(PROVINCES_DATA_PATH, lines=True)
    df_province = df_province.drop_duplicates()
    df_province = df_province.fillna('')

    return df_province


@task
def get_regions():
    df_regions = pd.read_json(REGIONS_DATA_PATH, lines=True)
    df_regions = df_regions.drop_duplicates()
    df_regions = df_regions.fillna('')

    return df_regions


@task
def get_meteo_data():
    meteo_data_array = []
    os.chdir(METEO_DATA_PATH)
    for element in os.listdir("."):
        if element.endswith('.gz'):
            df_meteo_data = pd.read_json(element, compression='gzip')
            df_meteo_data = df_meteo_data.fillna('')
            df_meteo_data = df_meteo_data.drop(columns=['flags'])

            meteo_data_array.append(df_meteo_data)

    df_data_concat = pd.concat(meteo_data_array)

    return df_data_concat
