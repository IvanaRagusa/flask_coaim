from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
import logging
import uuid

app = Flask(__name__)

# Configurazione del database PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myuser:mypass@localhost:5432/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Configura il logging
logging.basicConfig(level=logging.DEBUG)

# Modello per le attività
class ActivitiesData(db.Model):
    __tablename__ = 'activities_data'
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    User_ID = db.Column(db.String, nullable=False)
    Location = db.Column(db.String)
    Data_time = db.Column(db.String)
    Exercise_ID = db.Column(db.String)
    Exercise_name = db.Column(db.String)
    Message = db.Column(db.String)

# Modello per i sensori
class SensorsData(db.Model):
    __tablename__ = 'sensors_data'
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    Sensor_ID = db.Column(db.String, nullable=False)
    Location = db.Column(db.String)
    Sensor_Kit = db.Column(db.String)
    Sensor_LH = db.Column(db.String)
    Sensor_RH = db.Column(db.String)
    Sensor_LF = db.Column(db.String)
    Sensor_RF = db.Column(db.String)
    Data_time = db.Column(db.String)
    Message = db.Column(db.String)

@app.route('/initdb', methods=['GET'])
def init_db():
    try:
        # Crea le tabelle nel database se non esistono già
        db.create_all()
        return 'Database initialized successfully.'
    except Exception as e:
        app.logger.error(f'Error initializing database: {str(e)}')
        return f'Error initializing database: {str(e)}'

# Rotte per gestire i dati provenienti da Kafka
@app.route('/sensors', methods=['POST'])
def add_sensor_data():
    try:
        data = request.json
        if not data:
            app.logger.error('Empty request or invalid JSON format')
            return jsonify({'error': 'Empty request or invalid JSON format'}), 400
        
        # Assicurati che data sia una lista di dizionari
        if not isinstance(data, list):
            data = [data]
        
        for sensor_data in data:
            if 'Sensor_ID' not in sensor_data:
                app.logger.error('Sensor_ID is required')
                return jsonify({'error': 'Sensor_ID is required'}), 400
            
            new_sensor_data = SensorsData(
                Sensor_ID=sensor_data['Sensor_ID'],
                Location=sensor_data.get('Location', ''),
                Sensor_Kit=sensor_data.get('Sensor_Kit', ''),
                Sensor_LH=sensor_data.get('Sensor_LH', ''),
                Sensor_RH=sensor_data.get('Sensor_RH', ''),
                Sensor_LF=sensor_data.get('Sensor_LF', ''),
                Sensor_RF=sensor_data.get('Sensor_RF', ''),
                Data_time=sensor_data.get('Data_time', ''),
                Message=sensor_data.get('Message', '')
            )
            db.session.add(new_sensor_data)
        
        db.session.commit()
        return jsonify({'message': 'Sensor data added successfully'}), 201

    except Exception as e:
        db.session.rollback()
        app.logger.error(f'Error adding sensor data: {str(e)}')
        return jsonify({'error': str(e)}), 500

@app.route('/activities', methods=['POST'])
def add_activities_data():
    try:
        data = request.get_json()
        app.logger.debug("Received data: %s", data)
        
        if not data:
            app.logger.error('Empty request or invalid JSON format')
            return jsonify({'error': 'Empty request or invalid JSON format'}), 400
        
        # Assuming data is a list of dictionaries
        for activity in data:
            new_activity = ActivitiesData(
                User_ID=activity.get('User_ID'),
                Location=activity.get('Location'),
                Data_time=activity.get('Data_time'),
                Exercise_ID=activity.get('Exercise_ID'),
                Exercise_name=activity.get('Exercise_name'),
                Message=activity.get('Message')
            )
            db.session.add(new_activity)

        db.session.commit()

        return jsonify({'message': 'Activities data received and saved successfully'}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        app.logger.error(f'Database error: {str(e)}')
        return jsonify({'error': 'Database error'}), 500
    
    except Exception as e:
        app.logger.error(f'Error: {str(e)}')
        return jsonify({'error': str(e)}), 400
    
@app.route('/sensors_status_data')
def get_sensors_status_data():
    sensors_status = SensorsData.query.all()
    return jsonify([{
        'Sensor_ID': sensor.Sensor_ID,
        'Location': sensor.Location,
        'Sensor_Kit': sensor.Sensor_Kit,
        'Sensor_LH': sensor.Sensor_LH,
        'Sensor_RH': sensor.Sensor_RH,
        'Sensor_LF': sensor.Sensor_LF,
        'Sensor_RF': sensor.Sensor_RF,
        'Data_time': sensor.Data_time,
        'Message': sensor.Message
    } for sensor in sensors_status])

@app.route('/sensors_activities_data')
def get_activities_data():
    activities = ActivitiesData.query.all()
    return jsonify([{
        'User_ID': activity.User_ID,
        'Location': activity.Location,
        'Data_time': activity.Data_time,
        'Exercise_ID': activity.Exercise_ID,
        'Exercise_name': activity.Exercise_name,
        'Message': activity.Message
    } for activity in activities])

if __name__ == '__main__':
    app.run(debug=True, port=5000)
