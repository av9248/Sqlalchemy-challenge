# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import desc

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# Declare a Base using `automap_base()`
Base = automap_base()
# Use the Base class to reflect the database tables
Base.prepare(engine, reflect=True)

# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session
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
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Calculate the date one year from the last date in data set.
    previous_year = dt.date(2017,8,23) - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    precipitation_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= previous_year).order_by(Measurement.date).all()

    session.close()

    #dictionary using date as the key and prcp as the value
    precip = {date: prcp for date, prcp in precipitation_data}

    return jsonify(precip)


@app.route("/api/v1.0/stations")
def station():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query stations
    results = session.query(Station.station).all()

    session.close()

    # Return a JSON list of stations from the dataset
    stations = list(np.ravel(results))

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Calculate the date one year from the last date in data set.
    previous_year = dt.date(2017,8,23) - dt.timedelta(days=365)

    temperature_data = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == "USC00519281",Measurement.date >= previous_year).all()

    session.close()

    # Return a JSON list of stations from the dataset
    temp = list(np.ravel(temperature_data))

    return jsonify(temp)


@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    """Return TMIN, TAVG, TMAX."""
    # Select statement
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    if not end:
        # start = dt.datetime.strptime(start, "%m/%d/%Y")
        # # calculate TMIN, TAVG, TMAX for dates greater than start
        # results = session.query(*sel).\
        #     filter(Measurement.date >= start).all()
        # # Unravel results into a 1D array and convert to a list
        # temps = list(np.ravel(results))
        # return jsonify(temps)
        start = dt.datetime.strptime(start, "%m%d%Y")
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        session.close()
        temps = list(np.ravel(results))
        return jsonify(temps)
    # calculate TMIN, TAVG, TMAX with start and stop
    start = dt.datetime.strptime(start, "%m%d%Y")
    end = dt.datetime.strptime(end, "%m%d%Y")
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    session.close()
    # Unravel results into a 1D array and convert to a list
    temps = list(np.ravel(results))
    return jsonify(temps=temps)
if __name__ == '__main__':
    app.run()












