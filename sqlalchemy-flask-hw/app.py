import numpy as np
import pandas as pd
import datetime as dt

from dateutil.relativedelta import relativedelta

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
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

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
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs</br>"
        f"/api/v1.0/&ltstart&gt</br>"
        f"/api/v1.0/&ltstart&gt/&ltend&gt</br>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a JSON object with preciptiation levels by date."""
    
    # Pull query result from DB
    data = session.query(Measurement.date, Measurement.prcp).all()

    # Prepare an output dictionary to be JSONified
    out = []
    for row in data:
        out_dict = {}
        out_dict["date"] = row[0]
        out_dict["precipitation"] = row[1]
        out.append(out_dict)

    return jsonify(out)

@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON object with a list of stations."""
    
    # Pull query result from DB
    data = session.query(Measurement.station).group_by(Measurement.station).all()

    # Prepare an output dictionary to be JSONified
    out = []
    for row in data:
        out_dict = {}
        out_dict["station"] = row[0]
        out.append(out_dict)

    return jsonify(out)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a JSON object with temperatures over the last year."""
    
    # Calculate the date 1 year ago from the last data point in the database
    s = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    max_date = dt.date(int(s[0:4]), int(s[5:7]), int(s[8:10]))
    min_date = max_date - relativedelta(years=1)

    # Perform a query to retrieve the temperatures and dates
    data = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date>=min_date).all()

    # Prepare an output dictionary to be JSONified
    out = []
    for row in data:
        out_dict = {}
        out_dict["date"] = row[0]
        out_dict["temperature"] = row[1]
        out.append(out_dict)

    return jsonify(out)


@app.route("/api/v1.0/<s>")
def temp_start_only(s):
    """Return a JSON object with temperatures since the provided start date s, a string in format 'YYYY-MM-DD'"""
    
    # Parse user input, assumed 'YYYY-MM-DD' format
    start_date = dt.date(int(s[0:4]), int(s[5:7]), int(s[8:10]))

    # Query for low/avg/high temperatures from start_date through most recent available date
    data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).\
        all()[0]

    # Create a dictionary to store the output to be JSONified
    out = []
    out_dict = {}
    out_dict["low"] = data[0]
    out_dict["avg"] = data[1]
    out_dict["high"] = data[2]
    out.append(out_dict)

    return jsonify(out)


@app.route("/api/v1.0/<s>/<e>")
def temp_start_end(s, e):
    """Return a JSON object with temperatures between the provided dates (strings in format 'YYYY-MM-DD')"""

    # Parse user input, assumed 'YYYY-MM-DD' format
    start_date = dt.date(int(s[0:4]), int(s[5:7]), int(s[8:10]))
    end_date = dt.date(int(e[0:4]), int(e[5:7]), int(e[8:10]))

    # Query for low/avg/high temperatures from start_date through most recent available date
    data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= end_date).\
        all()[0]

   # Create a dictionary to store the output to be JSONified
    out = []
    out_dict = {}
    out_dict["low"] = data[0]
    out_dict["avg"] = data[1]
    out_dict["high"] = data[2]
    out.append(out_dict)

    return jsonify(out)

if __name__ == '__main__':
    app.run(debug=True)
