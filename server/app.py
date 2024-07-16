from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, Camper, Activity, Signup

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/campers', methods=['GET'])
def get_campers():
    campers = Camper.query.all()
    return jsonify([camper.to_dict() for camper in campers]), 200

@app.route('/campers/<int:id>', methods=['GET'])
def get_camper(id):
    camper = Camper.query.get_or_404(id)
    return jsonify(camper.to_dict()), 200

@app.route('/campers', methods=['POST'])
def create_camper():
    data = request.get_json()
    try:
        if 'name' not in data or 'age' not in data:
            raise KeyError("Name and age are required.")
        
        new_camper = Camper(name=data['name'], age=data['age'])
        db.session.add(new_camper)
        db.session.commit()
        return jsonify(new_camper.to_dict()), 201
    except KeyError as e:
        return jsonify(errors=[str(e)]), 400
    except ValueError as e:
        return jsonify(errors=[str(e)]), 400

@app.route('/campers/<int:id>', methods=['PATCH'])
def update_camper(id):
    camper = Camper.query.get_or_404(id)
    data = request.get_json()
    try:
        if 'name' in data:
            camper.name = data['name']
        if 'age' in data:
            camper.age = data['age']
        db.session.commit()
        return jsonify(camper.to_dict()), 200
    except KeyError as e:
        return jsonify(errors=[str(e)]), 400
    except ValueError as e:
        return jsonify(errors=[str(e)]), 400

@app.route('/activities', methods=['GET'])
def get_activities():
    activities = Activity.query.all()
    return jsonify([activity.to_dict() for activity in activities]), 200

@app.route('/activities/<int:id>', methods=['DELETE'])
def delete_activity(id):
    activity = Activity.query.get_or_404(id)
    db.session.delete(activity)
    db.session.commit()
    return '', 204

@app.route('/signups', methods=['POST'])
def create_signup():
    data = request.get_json()
    try:
        if 'camper_id' not in data or 'activity_id' not in data or 'time' not in data:
            raise KeyError("Camper ID, activity ID, and time are required.")
        
        new_signup = Signup(camper_id=data['camper_id'], activity_id=data['activity_id'], time=data['time'])
        db.session.add(new_signup)
        db.session.commit()
        return jsonify(new_signup.to_dict()), 201
    except KeyError as e:
        return jsonify(errors=[str(e)]), 400
    except ValueError as e:
        return jsonify(errors=[str(e)]), 400

if __name__ == '__main__':
    app.run(port=5555, debug=True)
