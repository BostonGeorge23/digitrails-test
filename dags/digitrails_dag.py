from datetime import timedelta, datetime, timezone

from airflow.decorators import dag, task_group
from core.get_data import get_cities, get_provinces, get_regions, get_meteo_data
from core.map_data import insert_data
from core.merge_data import merge_data
import logging

@dag(
     dag_id='digitrails_dag',
     catchup=False,
     is_paused_upon_creation=False,
     dagrun_timeout=timedelta(minutes=10)
)
def digitrails_dag():

    @task_group
    def get_data():
        cities = get_cities()
        provinces = get_provinces()
        regions = get_regions()
        meteo_data = get_meteo_data()

        return cities, provinces, regions, meteo_data

    cities, provinces, regions, meteo_data = get_data()
    logging.info(f'Cities: {cities}')
    logging.info(f'Provinces: {provinces}')
    logging.info(f'Regions: {regions}')
    logging.info(f'Meteo data: {meteo_data}')
    merged_data = merge_data(cities, provinces, regions, meteo_data)
    insert_data(merged_data)

digitrails_dag()



