import datetime
import logging
import os

import pandas as pd
import json

from airflow.decorators import task
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select, MetaData
from model.model_db import City, MeteoData, HourlyData, Region, Province
from italy_geopop.pandas_extension import pandas_activate


metadata_obj = MetaData()
Base = declarative_base()
pandas_activate(include_geometry=True, data_year=2022)

DIGITRAILS_DB_HOST = os.getenv('AIRFLOW_VAR_DIGITRAILS_DB_HOST')
DIGITRAILS_DB_PORT = int(os.getenv('AIRFLOW_VAR_DIGITRAILS_DB_PORT'))
DIGITRAILS_DB_USER = os.getenv('AIRFLOW_VAR_DIGITRAILS_DB_USER')
DIGITRAILS_DB_PASSWORD = os.getenv('AIRFLOW_VAR_DIGITRAILS_DB_PASSWORD')
DIGITRAILS_DB_NAME = os.getenv('AIRFLOW_VAR_DIGITRAILS_DB_NAME')

engine = create_engine(f"postgresql://{DIGITRAILS_DB_USER}:{DIGITRAILS_DB_PASSWORD}@{DIGITRAILS_DB_HOST}:{DIGITRAILS_DB_PORT}/{DIGITRAILS_DB_NAME}")

@task
def create_tables():
    Region.metadata.create_all(engine)
    Province.metadata.create_all(engine)
    City.metadata.create_all(engine)
    MeteoData.metadata.create_all(engine)
    HourlyData.metadata.create_all(engine)
    logging.info("Tables created")



def get_province(session, province_data):
    query = select(Province).where(Province.province_name == province_data['province_name'])
    q_result = session.execute(query).first()

    if q_result:
        province = q_result[0]
    else:
        province = Province(
            province_name=province_data['province_name'],
            province_istat_code=province_data['province_istat_code'],
            province_boundaries=province_data['province_boundaries']
        )

    return province



def get_region(session, region_data):
    query = select(Region).where(Region.region_name == region_data['region_name'])
    q_result = session.execute(query).first()

    if q_result:
        region = q_result[0]
    else:
        region = Region(
            region_name=region_data['region_name'],
            region_istat_code=region_data['region_istat'],
            region_boundaries=region_data['region_boundaries']
        )

    return region


def get_city(session, city_data):
    query = select(City).where(City.denominazione_ita == city_data['denominazione_ita'])
    q_result = session.execute(query).first()

    if q_result:
        city = q_result[0]
    else:
        city = City(
            sigla_provincia=city_data['sigla_provincia'],
            codice_istat=city_data['codice_istat'],
            denominazione_ita=city_data['denominazione_ita'],
            lat=city_data['lat'],
            lon=city_data['lon'],
            superficie_kmq=city_data['superficie_kmq']
        )

    return city


@task
def insert_data(cities_meteo, **context):
    session = Session(engine)
    duplicate_check = []
    dict_city = {}

    for index, row in cities_meteo.iterrows():

        if row['hourly']:
            hourly_data = row['hourly']['data']
        else:
            hourly_data = []
        if row['denominazione_ita'] not in duplicate_check:

            duplicate_check.append(row['denominazione_ita'])

            dict_city[row['denominazione_ita']] = {
                'denominazione_ita': row['denominazione_ita'],
                'sigla_provincia': row['sigla_provincia'],
                'codice_istat': row['codice_istat'],
                'lat': row['lat'],
                'lon': row['lon'],
                'superficie_kmq': row['superficie_kmq'],
                'latitude': row['latitude'],
                'longitude': row['longitude'],
                'timezone': row['timezone'],
                'offset': row['offset'],
                'elevation': row['elevation'],
                'hourly': hourly_data,
                'province_name': row['province_name'],
                'province_istat_code': row['province_istat_code'],
                'province_boundaries': row['province_boundaries'],
                'region_name': row['region_name'],
                'region_istat': row['region_istat'],
                'region_boundaries': row['region_boundaries']
            }
        else:
            dict_city[row['denominazione_ita']]['hourly'].extend(hourly_data)

    for key, value in dict_city.items():
        region = get_region(session, value)
        province = get_province(session, value)
        city = get_city(session, value)

        if value['latitude'] != '' or value['longitude'] != '' or value['timezone'] != '' or value['offset'] != '' or value['elevation'] != '':

            meteo_data = MeteoData(
                latitude=value['latitude'],
                longitude=value['longitude'],
                timezone=value['timezone'],
                offset=value['offset'],
                elevation=value['elevation']
            )

            if value['hourly'] != '':
                hourly_data_list = value['hourly']
                for item in hourly_data_list:
                    hourly_data = HourlyData(
                        time=datetime.datetime.fromtimestamp(item['time']),
                        icon=item['icon'],
                        summary=item['summary'],
                        precipIntensity=item['precipIntensity'],
                        temperature=item['temperature']
                    )
                    meteo_data.hourly_data.append(hourly_data)

            city.meteo_data.append(meteo_data)

        province.cities.append(city)
        region.provinces.append(province)

        session.add(region)
        session.add(province)
        session.add(city)

    session.flush()
    session.commit()
    session.close()
