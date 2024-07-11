from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Configurazione dei database
activities_db_uri = 'sqlite:///activities_db.db'
sensors_db_uri = 'sqlite:///sensors_db.db'

# Creazione delle istanze di motore e sessione per entrambi i database
activities_engine = create_engine(activities_db_uri)
activities_Session = sessionmaker(bind=activities_engine)
activities_session = activities_Session()

sensors_engine = create_engine(sensors_db_uri)
sensors_Session = sessionmaker(bind=sensors_engine)
sensors_session = sensors_Session()

# Base per la dichiarazione dei modelli SQLAlchemy
Base = declarative_base()

# Definizione dei modelli per le attività
class ActivitiesData(Base):
    __tablename__ = 'activities_data'
    User_ID = Column(String, primary_key=True)
    Location = Column(String)
    data_time = Column(String)
    Exercise_ID = Column(String)
    Exercise_name = Column(String)
    Message = Column(String)

# Definizione dei modelli per i sensori
class SensorsData(Base):
    __tablename__ = 'sensors_data'
    Sensor_ID = Column(String, primary_key=True)
    Location = Column(String)
    Sensor_Kit = Column(String)
    Sensor_LH = Column(String)
    Sensor_RH = Column(String)
    Sensor_LF = Column(String)
    Sensor_RF = Column(String)
    Message = Column(String)

# Creazione dei database e delle tabelle
Base.metadata.create_all(activities_engine)
Base.metadata.create_all(sensors_engine)

# Inserimento di dati di esempio per i sensori
example_sensors = [
    SensorsData(
        Sensor_ID='S123',
        Location='Room 101',
        Sensor_Kit='KitA',
        Sensor_LH='LH123',
        Sensor_RH='RH123',
        Sensor_LF='LF123',
        Sensor_RF='RF123',
        Message='All sensors operational.'
    ),
    SensorsData(
        Sensor_ID='S124',
        Location='Room 102',
        Sensor_Kit='KitB',
        Sensor_LH='LH124',
        Sensor_RH='RH124',
        Sensor_LF='LF124',
        Sensor_RF='RF124',
        Message='All sensors operational.'
    )
]

sensors_session.add_all(example_sensors)
sensors_session.commit()

# Inserimento di dati di esempio per le attività
example_activities = [
    ActivitiesData(
        User_ID='U123',
        Location='Gym',
        data_time='2024-07-09 10:00:00',
        Exercise_ID='E123',
        Exercise_name='Running',
        Message='Good performance.'
    ),
    ActivitiesData(
        User_ID='U124',
        Location='Park',
        data_time='2024-07-09 11:00:00',
        Exercise_ID='E124',
        Exercise_name='Cycling',
        Message='Excellent performance.'
    )
]

activities_session.add_all(example_activities)
activities_session.commit()

print("Databases and tables created successfully.")
