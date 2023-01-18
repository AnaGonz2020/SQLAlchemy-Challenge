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
        f"<h2><b>Welcome to the Climate App API!</b></h2><br/>"
        f"<h3><b>Ana Gonzalez<br/>"
        f"<br/>"
        f"Thank you for visitng! Here are your available routes:<br/><h3/><br/>"
        f"<b>For an analysis of precipitation in a .json file, use this route:</b><br/>"
        f"<br/><font size=5>"
        f"/api/v1.0/precipitation<br/>"
        f"<br/></font size=5>"
        f"<b>For a list of stations in the dataset, in .json fitle, use this route:</b><br/>"
        f"<br/><font size=5>"
        f"/api/v1.0/stations<br/>"
        f"<br/></font size=5>"
        f"<b>For a list of temperature observations for the previous year for the most active station, in .json file, use this route:</b><br/>"
        f"<br/><font size=5>"
        f"/api/v1.0/tobs<br/>"
        f"<br/></font size=5>"
        f"<b>For a list of the minimum temperature, the average temperature, and the maximum temperature, for a specified start date for each station in a .json file, adjust a start date to the route in the format yyyy-mm-dd</b><br/>"
        f"<br/><font size=5>"
        f"<b>For a list of the minimum temperature, the average temperature, and the maximum temperature, for a specified start date for each station, in a .json file, adjust a start date to the route in the format yyyy-mm-dd</b><br/>"
        f"<br/><font size=5>"
        f"/api/v1.0/start<br/>"
        f"<br/></font size=5>"
        f"<b>For a list of the minimum temperature, the average temperature, and the maximum temperature for a specified date range, in .json file, adjust a start and end date in the format yyyy-mm-dd/yyyy-mm-dd</b><br/>"
        f"<br/><font size=5>"
        f"/api/v1.0/start/end<br/>"
        f"<br/></font size=5>"
    )


@app.route("/api/v1.0/precipitation")
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
    
    current = dt.date(2017, 8, 23)
    prior_year = current - dt.timedelta(days=365)

    most_act_temp = session.query(*measurement.date, measurement.tobs).\
        filter(measurement.station == 'USC00519281').\
        filter(measurement.date >= prior_year).\
        filter(measurement.date <= current).\
        order_by(measurement.date).all()


    session.close()

    # Return a JSON list of temperature observations for the previous year.
    most_active_tob = dict(most_act_temp)
    return jsonify(most_active_tob)

@app.route("/api/v1.0/<start>")
def start(start=None):

    # Return a JSON list of the minimum temperature,
    # the average temperature, and the maximum temperature 
    # for a specified start or start-end range.
    # For a specified start, calculate TMIN, TAVG,
    # and TMAX for all the dates greater than or equal to the start date.
    
    temp_start = session.query(func.min(measurement.tobs)\
        , func.max(measurement.tobs)\
        , func.round(func.avg(measurement.tobs),2), station.name).\
        filter(measurement.station == station.station).\
        filter(measurement.date >= start).\
        group_by(measurement.station).all()

    session.close()

    start_data = []
    for tmin, tmax, tavg, name in temp_start:
        start_dict = {}
        start_dict['tmin'] = tmin
        start_dict['tmax'] = tmax
        start_dict['tavg'] = tavg
        start_dict['name'] = name
        start_data.append(start_dict)

    return jsonify(start_data)


   
 
@app.route("/api/v1.0/<start>/<end>")
def range(start=None, end=None):
    # For a specified start date and end date, calculate TMIN, TAVG,
    # and TMAX for the dates from the start date to the end date, inclusive.
    
    temp_range = session.query(func.min(measurement.tobs)\
        , func.max(measurement.tobs)\
        , func.round(func.avg(measurement.tobs),2), station.name).\
        filter(measurement.station == station.station).\
        filter(measurement.date >= start).\
        filter(measurement.date <= end).\
        group_by(measurement.station).all()

    session.close()

    range_data = []
    for tmin, tmax, tavg, name in temp_range:
        range_dict = {}
        range_dict['tmin'] = tmin
        range_dict['tmax'] = tmax
        range_dict['tavg'] = tavg
        range_dict['name'] = name
        range_data.append(range_dict)

    return jsonify(range_data) 

if __name__ == '__main__':
    app.run(debug=True)