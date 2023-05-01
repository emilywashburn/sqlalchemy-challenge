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
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Base.classes.keys()
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB


#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/<start>/<end><br>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all precepitation data"""
    # Query for the dates and precipitation values
    results = session.query(Measurement.date, Measurement.prcp).order_by(Measurement.date).all()

    # Convert to list of dictionaries to jsonify
    prcp_list = []

    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
               
        prcp-list.append(prcp_dict)
    session.close()

    return jsonify(prcp_list)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all Stations
    results = session.query(Station.station).order_by(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all TOBs"""
    # Query all tobs

    results = session.query(Measurement.date, Measurement.tobs, Measurement.prcp).\
                filter(Measurement.date >= '2016-08-23').\
                filter(Measurement.station=='USC00519281').\
                order_by(Measurement.date).all()

    session.close()

    # Convert the list to Dictionary
    tobs_list = []
    for prcp, date,tobs in results:
        tobs_dict = {}
        tobs_dict["prcp"] = prcp
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        
        tobs_list.append(tobs_dict)

    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def Start(start_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of min, avg and max tobs for a start date"""
    # Query all tobs

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).all()

    session.close()

    # Create a dictionary from the row data and append to a list of start_date_tobs
    starting_tobs = []
    for min, avg, max in results:
        starting_tobs_dict = {}
        starting_tobs_dict["min_temp"] = min
        starting_tobs_dict["avg_temp"] = avg
        starting_tobs_dict["max_temp"] = max
        starting_tobs_dict.append(starting_tobs_dict) 
    return jsonify(starting_tobs)

@app.route("/api/v1.0/<start>/<end>")
def Start_end(start_date, end_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of min, avg and max tobs for start and end dates"""
    # Query all tobs

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    session.close()
  
    # Create a dictionary from the row data and append to a list of start_end_date_tobs
    ending_tobs = []
    for min, avg, max in results:
        ending_tobs_dict = {}
        ending_tobs_dict["min_temp"] = min
        ending_tobs_dict["avg_temp"] = avg
        ending_tobs_dict["max_temp"] = max
        ending_tobs.append(ending_tobs_dict) 
    

    return jsonify(ending_tobs)

if __name__ == "__main__":
    app.run(debug=True)
