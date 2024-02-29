# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################

#create engine to hawaii.sqlite
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# 1. /
# Start at the homepage.
# List all the available routes.
@app.route("/")
def home():
    return(
        f"Welcome to the Hawaii Climiate API<br/><br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start>YYYY-MM-DD (input start date)<br/>"
        f"/api/v1.0/<start>/<end> YYYY-MM-DD/YYYY-MM-DD (input start/end dates)"
    )


# 2. /api/v1.0/precipitation
# Convert the query results from your precipitation analysis
# (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
# Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    one_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    last_year = dt.date(one_year.year, one_year.month, one_year.day)
    
    scores = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= last_year).\
    order_by(Measurement.date).all()

    prep_dict = dict(scores)

    return jsonify(prep_dict)


# 3. /api/v1.0/stations
# Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    session.query(Measurement.station).distinct().count()

    active = session.query(Measurement.station,
                       func.count(Measurement.station)).\
                        group_by(Measurement.station).\
                        order_by(func.count(Measurement.station).desc()).all()
    
    station_dict = dict(active)

    return jsonify(station_dict)


# 4. /api/v1.0/tobs
# Query the dates and temperature observations of the most-active station for the previous year of data.
# Return a JSON list of temperature observations for the previous year.
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    one_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    result_temp = session.query(Measurement.date, Measurement.tobs).\
                filter(Measurement.station == 'USC00519281').\
                filter(Measurement.date >= one_year).all()
    
    # create a loop to look through data
    # source 04 to use for loop with two variables
    tobs_list = []
    for d,t in result_temp:
        tobs_dict = {}
        tobs_dict['date'] = d
        tobs_dict['tobs'] = t
        tobs_list.append(tobs_dict)

    return jsonify(tobs_list)


# 5. /api/v1.0/<start> and /api/v1.0/<start>/<end>
# Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
# For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
# For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.

@app.route("/api/v1.0/<start>")
def start_temp(start):
    session = Session(engine)

    temp = session.query(func.min(Measurement.tobs),
                     func.avg(Measurement.tobs),
                     func.max(Measurement.tobs)).\
                    filter(Measurement.date >= start).all()

    temp_list = []
    for tmin, tavg, tmax in temp:
        temps_dict = {}
        temps_dict['minimum temperature'] = tmin
        temps_dict['average temperature'] = tavg
        temps_dict['maximum temperature'] = tmax
        temp_list.append(temps_dict)

    return jsonify(temp_list)

# /api/v1.0/<start>/<end>
# For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
@app.route("/api/v1.0/<start>/<end>")
def start_end_temp(start, end):
    session = Session(engine)

    temp2 = session.query(func.min(Measurement.tobs),
                     func.avg(Measurement.tobs),
                     func.max(Measurement.tobs)).\
                    filter(Measurement.date >= start).\
                    filter(Measurement.date <= end).all()
    
    temp2_list = []
    temps2_dict = {}
    for tmin, tavg, tmax in temp2:
        temps2_dict['minimum temperature'] = tmin
        temps2_dict['average temperature'] = tavg
        temps2_dict['maximum temperature'] = tmax
        temp2_list.append(temps2_dict)

    return jsonify(temp2_list)



# creating app.run statement
if __name__ == "__main__":
    app.run(debug=True)