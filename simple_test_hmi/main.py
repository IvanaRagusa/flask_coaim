from flask import Flask, render_template, jsonify
from flask_cors import CORS
from kafka import KafkaConsumer
import threading
import json
import requests

app = Flask(__name__)
CORS(app)

# Configura i consumer Kafka
KAFKA_BOOTSTRAP_SERVERS = '150.217.17.170:32100' # Inserire ip e porta kafka

sensors_status_consumer = KafkaConsumer(
    'odin-platform-sensors-status',
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='sensors-status-group'
)

sensors_activities_consumer = KafkaConsumer(
    'odin-platform-sensors-activities',
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='sensors-activities-group'
)

# URL del server di database Flask
DATABASE_SERVER_URL = 'http://localhost:5000'
def consume_kafka(consumer, endpoint):
    for message in consumer:
        try:
            if message.value:
                data = json.loads(message.value.decode('utf-8'))
                print(f"Received data from Kafka: {data}")
                response = requests.post(f"{DATABASE_SERVER_URL}/{endpoint}", json=data)
                if response.status_code == 201:
                    print(f"Data sent to {endpoint}: {data}, Response: {response.status_code}")
                else:
                    print(f"Failed to send data to {endpoint}: {data}, Response: {response.status_code}")
            else:
                print("Empty message received.")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")

# Avvia i thread per consumare messaggi da Kafka
status_thread = threading.Thread(target=consume_kafka, args=(sensors_status_consumer, 'sensors'))
activities_thread = threading.Thread(target=consume_kafka, args=(sensors_activities_consumer, 'activities'))

status_thread.start()
activities_thread.start()

# Rotte Flask per la visualizzazione dei dati
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/show_data')
def show_data():
    return render_template('show_sensor_data.html')

@app.route('/sensors_status_data', methods=['GET'])
def get_sensors_status_data():
    response = requests.get(f"{DATABASE_SERVER_URL}/sensors_status_data")
    sensors_status_data = response.json()
    return jsonify(sensors_status_data)

@app.route('/sensors_activities_data', methods=['GET'])
def get_sensors_activities_data():
    response = requests.get(f"{DATABASE_SERVER_URL}/sensors_activities_data")
    sensors_activities_data = response.json()
    return jsonify(sensors_activities_data)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
