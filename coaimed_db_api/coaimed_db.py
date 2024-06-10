# app.py
from flask import Flask, request, jsonify
from models import db, Activity, Exercise, Sensor, User
import config

app = Flask(__name__)
app.config.from_object(config.Config)
db.init_app(app)

@app.route('/')
def index():
    return "Welcome to the API"

@app.route('/activities', methods=['GET', 'POST'])
def handle_activities():
    if request.method == 'POST':
        data = request.json
        new_activity = Activity(
            user_id=data['user_id'],
            exercise_id=data['exercise_id'],
            sensor_id=data['sensor_id']
        )
        db.session.add(new_activity)
        db.session.commit()
        return jsonify(new_activity.activity_id), 201
    else:
        activities = Activity.query.all()
        return jsonify([{
            'activity_id': a.activity_id,
            'user_id': a.user_id,
            'exercise_id': a.exercise_id,
            'sensor_id': a.sensor_id,
            'activity_time': a.activity_time
        } for a in activities])

@app.route('/exercises', methods=['GET', 'POST'])
def handle_exercises():
    if request.method == 'POST':
        data = request.json
        new_exercise = Exercise(
            exercise_identifier=data['exercise_identifier'],
            exercise_name=data['exercise_name'],
            location=data['location'],
            data_time=data['data_time'],
            message=data.get('message')
        )
        db.session.add(new_exercise)
        db.session.commit()
        return jsonify(new_exercise.exercise_id), 201
    else:
        exercises = Exercise.query.all()
        return jsonify([{
            'exercise_id': e.exercise_id,
            'exercise_identifier': e.exercise_identifier,
            'exercise_name': e.exercise_name,
            'location': e.location,
            'data_time': e.data_time,
            'message': e.message
        } for e in exercises])

@app.route('/sensors', methods=['GET', 'POST'])
def handle_sensors():
    if request.method == 'POST':
        data = request.json
        new_sensor = Sensor(
            sensor_identifier=data['sensor_identifier'],
            location=data['location'],
            sensor_kit=data['sensor_kit'],
            sensor_lh_status=data.get('sensor_lh_status'),
            sensor_rh_status=data.get('sensor_rh_status'),
            sensor_lf_status=data.get('sensor_lf_status'),
            sensor_rf_status=data.get('sensor_rf_status'),
            message=data.get('message')
        )
        db.session.add(new_sensor)
        db.session.commit()
        return jsonify(new_sensor.sensor_id), 201
    else:
        sensors = Sensor.query.all()
        return jsonify([{
            'sensor_id': s.sensor_id,
            'sensor_identifier': s.sensor_identifier,
            'location': s.location,
            'sensor_kit': s.sensor_kit,
            'sensor_lh_status': s.sensor_lh_status,
            'sensor_rh_status': s.sensor_rh_status,
            'sensor_lf_status': s.sensor_lf_status,
            'sensor_rf_status': s.sensor_rf_status,
            'message': s.message
        } for s in sensors])

@app.route('/users', methods=['GET', 'POST'])
def handle_users():
    if request.method == 'POST':
        data = request.json
        new_user = User(
            user_identifier=data['user_identifier'],
            location=data['location']
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.user_id), 201
    else:
        users = User.query.all()
        return jsonify([{
            'user_id': u.user_id,
            'user_identifier': u.user_identifier,
            'location': u.location
        } for u in users])

if __name__ == '__main__':
    app.run(debug=True)

