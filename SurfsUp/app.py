# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
app = Flask(__name__)

#################################################
# Flask Setup
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        "/api/v1.0/{start}<br/>"
        "/api/v1.0/{start}/{end}<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all precipiration data"""
    # Query all passengers
    precipitation_results = session.query(measurement.date, measurement.prcp).all()

    session.close()
    # print(precipiration_results)

    clean_data = []
    for prcp, date in precipitation_results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["precipitation"] = prcp
        clean_data.append(precipitation_dict)
    
    return jsonify(clean_data)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all precipiration data"""
    # Query all passengers
    stations_results = session.query(measurement.station).all()

    session.close()
    # print(stations_results)

    stations_data= []
    for stations in stations_results:
        # print(stations)
        stations_dict = {}
        stations_dict["stations"] = stations[0]
        stations_data.append(stations_dict)
    
    return jsonify(stations_data)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all precipiration data"""
    # Query all passengers
    tobs_results = session.query(measurement.tobs).filter(measurement.date >= '2016-08-18').filter(measurement.station == 'USC00519281').filter(measurement.date <= '2017-08-18').all()
    session.close()
    # print(tobs_results)

    tobs_data = []
    for tobs in tobs_results:
        # print(tobs)
        tobs_dict = {}
        # tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs[0]
        tobs_data.append(tobs_dict)
    
    return jsonify(tobs_data)

@app.route("/api/v1.0/<start>")
def start_date(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all start data"""
    # Query all passengers
    start_results = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).filter(measurement.date >= start).all()

    session.close()
    # print(tobs_results)

    start_results = list(np.ravel(start_results))   
    return jsonify(start_results)

@app.route("/api/v1.0/<start>/<end>")
def end_date(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all precipiration data"""
    # Query all passengers
    start_end_results = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).filter(measurement.date >= start).filter(measurement.date <=end).all()
    session.close()

    start_end_results = list(np.ravel(start_end_results))   
    return jsonify(start_end_results)


if __name__ == "__main__":
    app.run(debug=True)



#################################################
# Flask Routes
#################################################
