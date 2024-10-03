# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>')
def get_earthquake_by_id(id):
    earthquake = Earthquake.query.filter_by(id=id).first()
    if earthquake:
        response = {
            "id": earthquake.id,
            "location": earthquake.location,
            "magnitude": earthquake.magnitude,
            "year": earthquake.year   
        }
        return make_response(response, 200)
    else:
        return jsonify({"message": f"Earthquake {id} not found."}), 404
    
@app.route('/earthquakes/magnitude/<float:magnitude>')
def minimum_magnitude_value(magnitude):
    magnitude_value = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    if magnitude_value:
        response = {
            "count": len(magnitude_value),
            "quakes": [
                {
                    "id": value.id,
                    "location": value.location,
                    "magnitude": value.magnitude,
                    "year": value.year
                } for value in magnitude_value
            ]
        }
    else:
        response = {
            "count": 0,
            "quakes": []
        }
        
    return make_response(response, 200)
    

if __name__ == '__main__':
    app.run(port=5555, debug=True)
