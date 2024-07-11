from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

# Configurazione dei database per le attività e i sensori
app.config['SQLALCHEMY_BINDS'] = {
    'activities': 'sqlite:///'+ os.path.join(basedir,'activities_db.db'),
    'sensors': 'sqlite:///'+ os.path.join(basedir,'sensors_db.db')
}

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Modello per le attività
class ActivitiesData(db.Model):
    __bind_key__ = 'activities'
    __tablename__ = 'activities_data'
    User_ID = db.Column(db.String, primary_key=True)
    Location = db.Column(db.String)
    data_time = db.Column(db.String)
    Exercise_ID = db.Column(db.String)
    Exercise_name = db.Column(db.String)
    Message = db.Column(db.String)

# Schema Marshmallow per le attività
class ActivitiesDataSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ActivitiesData

# Modello per i sensori
class SensorsData(db.Model):
    __bind_key__ = 'sensors'
    __tablename__ = 'sensors_data'
    Sensor_ID = db.Column(db.String, primary_key=True)
    Location = db.Column(db.String)
    Sensor_Kit = db.Column(db.String)
    Sensor_LH = db.Column(db.String)
    Sensor_RH = db.Column(db.String)
    Sensor_LF = db.Column(db.String)
    Sensor_RF = db.Column(db.String)
    Message = db.Column(db.String)

# Schema Marshmallow per i sensori
class SensorsDataSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SensorsData

# Schema per la lista di attività
activities_schema = ActivitiesDataSchema()
activities_list_schema = ActivitiesDataSchema(many=True)

# Schema per la lista di sensori
sensors_schema = SensorsDataSchema()
sensors_list_schema = SensorsDataSchema(many=True)

# Rotte per le API dei sensori
@app.route('/sensors', methods=['GET'])
def get_sensors():
    sensors = SensorsData.query.all()
    return sensors_list_schema.jsonify(sensors)

@app.route('/sensors/<id>', methods=['GET'])
def get_sensor(id):
    sensor = SensorsData.query.get(id)
    if sensor is None:
        return jsonify({'message': 'Sensor not found'}), 404
    return sensors_schema.jsonify(sensor)

@app.route('/sensors', methods=['POST'])
def add_sensor():
    new_sensor = SensorsData(
        Sensor_ID=request.json['Sensor_ID'],
        Location=request.json['Location'],
        Sensor_Kit=request.json['Sensor_Kit'],
        Sensor_LH=request.json['Sensor_LH'],
        Sensor_RH=request.json['Sensor_RH'],
        Sensor_LF=request.json['Sensor_LF'],
        Sensor_RF=request.json['Sensor_RF'],
        Message=request.json['Message']
    )
    db.session.add(new_sensor)
    db.session.commit()
    return sensors_schema.jsonify(new_sensor), 201

@app.route('/sensors/<id>', methods=['PUT'])
def update_sensor(id):
    sensor = SensorsData.query.get(id)
    if sensor is None:
        return jsonify({'message': 'Sensor not found'}), 404
    sensor.Location = request.json.get('Location', sensor.Location)
    sensor.Sensor_Kit = request.json.get('Sensor_Kit', sensor.Sensor_Kit)
    sensor.Sensor_LH = request.json.get('Sensor_LH', sensor.Sensor_LH)
    sensor.Sensor_RH = request.json.get('Sensor_RH', sensor.Sensor_RH)
    sensor.Sensor_LF = request.json.get('Sensor_LF', sensor.Sensor_LF)
    sensor.Sensor_RF = request.json.get('Sensor_RF', sensor.Sensor_RF)
    sensor.Message = request.json.get('Message', sensor.Message)
    db.session.commit()
    return sensors_schema.jsonify(sensor)

@app.route('/sensors/<id>', methods=['DELETE'])
def delete_sensor(id):
    sensor = SensorsData.query.get(id)
    if sensor is None:
        return jsonify({'message': 'Sensor not found'}), 404
    db.session.delete(sensor)
    db.session.commit()
    return jsonify({'message': 'Sensor deleted'})

# Rotte per le API delle attività
@app.route('/activities', methods=['GET'])
def get_activities():
    activities = ActivitiesData.query.all()
    return activities_list_schema.jsonify(activities)

@app.route('/activities/<id>', methods=['GET'])
def get_activity(id):
    activity = ActivitiesData.query.get(id)
    if activity is None:
        return jsonify({'message': 'Activity not found'}), 404
    return activities_schema.jsonify(activity)

@app.route('/activities', methods=['POST'])
def add_activity():
    new_activity = ActivitiesData(
        User_ID=request.json['User_ID'],
        Location=request.json['Location'],
        data_time=request.json['data_time'],
        Exercise_ID=request.json['Exercise_ID'],
        Exercise_name=request.json['Exercise_name'],
        Message=request.json['Message']
    )
    db.session.add(new_activity)
    db.session.commit()
    return activities_schema.jsonify(new_activity), 201

@app.route('/activities/<id>', methods=['PUT'])
def update_activity(id):
    activity = ActivitiesData.query.get(id)
    if activity is None:
        return jsonify({'message': 'Activity not found'}), 404
    activity.Location = request.json.get('Location', activity.Location)
    activity.data_time = request.json.get('data_time', activity.data_time)
    activity.Exercise_ID = request.json.get('Exercise_ID', activity.Exercise_ID)
    activity.Exercise_name = request.json.get('Exercise_name', activity.Exercise_name)
    activity.Message = request.json.get('Message', activity.Message)
    db.session.commit()
    return activities_schema.jsonify(activity)

@app.route('/activities/<id>', methods=['DELETE'])
def delete_activity(id):
    activity = ActivitiesData.query.get(id)
    if activity is None:
        return jsonify({'message': 'Activity not found'}), 404
    db.session.delete(activity)
    db.session.commit()
    return jsonify({'message': 'Activity deleted'})

if __name__ == '__main__':
    app.run(debug=True)
