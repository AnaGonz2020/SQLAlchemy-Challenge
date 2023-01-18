import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import pandas as pd
import datetime as dt

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)
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
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("api/v1.0/precipitation")
def precipitation():

    """Return a list of all recent date in the last 12 months"""
    # Convert the query results from your precipitation analysis 
    # (i.e. retrieve only the last 12 months of data) 
    # to a dictionary using date as the key and prcp as the value.
    recent_date = engine.execute('SELECT max(date) FROM measurement').fetchall()
    rain_data = session.query(measurement.date, measurement.prcp).filter(measurement.date >= "2016-08-23").\
    filter(measurement.date <= "2017-08-23").all()

    session.close()

    precipitation = {date:prcp for date, prcp in rain_data}

    return jsonify(precipitation)


@app.route("/api/v1.0/stations")
def stations():

    """Return a list of station data """
    # Query all passengers
    station_names = session.query(station.id, station.name).all()

    session.close()

    return jsonify(station_names)

@app.route("/api/v1.0/tobs")
def tob():

    """Return a list of all dates and temperature observations of the most active station for the previous year"""
    #Query the dates and temperature observations of the most-active 
    # station for the previous year of data.
    .


    session.close()

    # Return a JSON list of temperature observations for the previous year.
    return jsonify(precipitation)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def start():

    """Return a list of all recent date in the last 12 months"""
    # Convert the query results from your precipitation analysis 
    # (i.e. retrieve only the last 12 months of data) 
    # to a dictionary using date as the key and prcp as the value.
    recent_date = engine.execute('SELECT max(date) FROM measurement').fetchall()
    rain_data = session.query(measurement.date, measurement.prcp).filter(measurement.date >= "2016-08-23").\
    filter(measurement.date <= "2017-08-23").all()

    session.close()

    precipitation = {date:prcp for date, prcp in rain_data}

    return jsonify(precipitation)   
 

if __name__ == '__main__':
    app.run(debug=True)