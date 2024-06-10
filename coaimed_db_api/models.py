# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Activity(db.Model):
    __tablename__ = 'activities'
    activity_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.exercise_id'), nullable=False)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensors.sensor_id'), nullable=False)
    activity_time = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())

class Exercise(db.Model):
    __tablename__ = 'exercises'
    exercise_id = db.Column(db.Integer, primary_key=True)
    exercise_identifier = db.Column(db.String(50), nullable=False)
    exercise_name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    data_time = db.Column(db.TIMESTAMP, nullable=False)
    message = db.Column(db.Text)

class Sensor(db.Model):
    __tablename__ = 'sensors'
    sensor_id = db.Column(db.Integer, primary_key=True)
    sensor_identifier = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    sensor_kit = db.Column(db.String(50), nullable=False)
    sensor_lh_status = db.Column(db.String(50))
    sensor_rh_status = db.Column(db.String(50))
    sensor_lf_status = db.Column(db.String(50))
    sensor_rf_status = db.Column(db.String(50))
    message = db.Column(db.Text)

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    user_identifier = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50), nullable=False)
