from airflow.decorators import task
import pandas as pd
from italy_geopop.pandas_extension import pandas_activate

pandas_activate(include_geometry=True, data_year=2022)

@task
def merge_data(cities, provinces, regions, meteo_data, **context):
    cities_meteo = cities.merge(meteo_data, left_on=['lat', 'lon'], right_on=['latitude', 'longitude'], how='right')

    provinces['province_name'] = provinces['province_name'].str.replace('Aristanis/Oristano', 'Oristano')
    provinces['province_name'] = provinces['province_name'].str.replace('Bolzano - Bozen', 'Bolzano/Bozen')
    provinces['province_name'] = provinces['province_name'].str.replace('Provincia di Trento', 'Trento')
    provinces['province_name'] = provinces['province_name'].str.replace('Roma Capitale', 'Roma')
    provinces['province_short'] = provinces['province_name'].italy_geopop.from_province()['province_short']
    provinces['region_name'] = provinces['province_name'].italy_geopop.from_province()['region']

    cities_meteo = cities_meteo.merge(provinces, left_on='sigla_provincia', right_on='province_short', how='left')
    cities_meteo = cities_meteo.merge(regions, on='region_name', how='left')
    cities_meteo = cities_meteo.dropna()

    return cities_meteo