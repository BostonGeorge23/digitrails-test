from sqlalchemy import ForeignKey, Float, Integer, DateTime, Column
from sqlalchemy import String
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base


Base = declarative_base()

class Region(Base):
    __tablename__ = "region"
    id = Column(Integer, primary_key=True)
    region_name = Column(String)
    region_istat_code = Column(String)
    region_boundaries = Column(String)

    provinces = relationship("Province")
    cities = relationship("City")


class Province(Base):
    __tablename__ = "province"
    id = Column(Integer, primary_key=True)
    region_id = Column(Integer, ForeignKey("region.id"))
    province_name = Column(String)
    province_istat_code = Column(String)
    province_boundaries = Column(String)

    cities = relationship("City")


class City(Base):
    __tablename__ = "city"
    id = Column(Integer, primary_key=True)
    province_id = Column(Integer, ForeignKey("province.id"))
    region_id = Column(Integer, ForeignKey("region.id"))
    sigla_provincia = Column(String)
    codice_istat = Column(String)
    denominazione_ita = Column(String)
    lat = Column(Float)
    lon = Column(Float)
    superficie_kmq = Column(Float)

    meteo_data = relationship("MeteoData")



class MeteoData(Base):
    __tablename__ = "meteo_data"
    id = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey("city.id"))
    latitude = Column(Float)
    longitude = Column(Float)
    timezone = Column(String)
    offset = Column(Float)
    elevation = Column(Integer)

    hourly_data = relationship("HourlyData")


class HourlyData(Base):
    __tablename__ = "hourly_data"
    id = Column(Integer, primary_key=True)
    meteo_data_id = Column(Integer, ForeignKey("meteo_data.id"))
    time = Column(DateTime)
    icon = Column(String)
    summary = Column(String)
    precipIntensity = Column(Float)
    temperature = Column(Float)
