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
Base.prepare(engine, reflect=True)

# Save reference to the table
Station = Base.classes.station
Measurement = Base.classes.measurement



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
        f"Welcome to the Stations API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a tuple of dates and precipitation"""
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all passengers
    results = session.query(Measurement.date,Measurement.prcp).limit(5)

    # Convert list of tuples into normal list
    #results = list(np.ravel(results))
    all_dates = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_dates.append(prcp_dict)

    return jsonify(all_dates)


@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations"""
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Query all stations
    results = session.query(Station.name).all()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def temperature():
    """Display date and temp for last year."""
    # Create our session (link) from Python to the DB
    session = Session(engine)

    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > '04-23-2019').all()

    start_temps = []
    for date, tobs in results:
        temps_dict = {}
        temps_dict["date"] = date
        temps_dict["tobs"] = tobs
        start_temps.append(temps_dict)

    return jsonify(start_temps)


@app.route("/api/v1.0/<start>")
def max_temp_start(start):
    """calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date."""
    # Create our session (link) from Python to the DB
    session = Session(engine)

    start_date = start
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date > start_date).all()

    start_temps = []
    for tmin, tavg, tmax in results:
        temps_dict = {}
        temps_dict["tmin"] = tmin
        temps_dict["tavg"] = tavg
        temps_dict["tmax"] = tmax
        start_temps.append(temps_dict)

    return jsonify(start_temps)

@app.route("/api/v1.0/<start>/<end>")
def max_temp_start_end(start,end):
    """calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date."""
    # Create our session (link) from Python to the DB
    session = Session(engine)

    start_date = start
    end_date = end
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date > start_date).filter(Measurement.date < end_date).all()

    start_end_temps = []
    for tmin, tavg, tmax in results:
        temps1_dict = {}
        temps1_dict["tmin"] = tmin
        temps1_dict["tavg"] = tavg
        temps1_dict["tmax"] = tmax
        start_end_temps.append(temps1_dict)

    return jsonify(start_end_temps)

if __name__ == '__main__':
    app.run(debug=True)

