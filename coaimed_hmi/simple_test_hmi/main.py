from flask import Flask, render_template, jsonify
from kafka import KafkaConsumer
import threading
import json
import requests

app = Flask(__name__)

# Configura i consumer Kafka
KAFKA_BOOTSTRAP_SERVERS = '192.168.112.115:30005'#Inserire ip e porta kafka

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

# Configura l'URL del database
DATABASE_URL = 'http://localhost:5000'

# Liste per memorizzare temporaneamente i dati ricevuti
sensors_status_data = []
sensors_activities_data = []

def consume_kafka(consumer, data_list, endpoint):
    for message in consumer:
        data = json.loads(message.value.decode('utf-8'))
        data_list.append(data)
        # Invia i dati al database
        response = requests.post(f"{DATABASE_URL}/{endpoint}", json=data)
        print(f"Data sent to {endpoint}: {data}, Response: {response.status_code}")

# Avvia i thread per consumare messaggi da Kafka
status_thread = threading.Thread(target=consume_kafka, args=(sensors_status_consumer, sensors_status_data, 'sensors'))
activities_thread = threading.Thread(target=consume_kafka, args=(sensors_activities_consumer, sensors_activities_data, 'exercises'))

status_thread.start()
activities_thread.start()

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/show_data')
def index():
    return render_template('show_data.html', sensors_status_data=sensors_status_data, sensors_activities_data=sensors_activities_data)

@app.route('/sensors_status_data')
def get_sensors_status_data():
    return jsonify(sensors_status_data)

@app.route('/sensors_activities_data')
def get_sensors_activities_data():
    return jsonify(sensors_activities_data)

if __name__ == '__main__':
    app.run(debug=True, port=5001)

