import numpy as np
import pandas as pd
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
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )

#################################################
# Precipitation
#################################################

@app.route("/api/v1.0/precipitation")
def precipitation():
    last_twelve = dt.date(2017, 8, 23) - dt.timedelta(days= 365)
    prcp_scores = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= last_twelve).all()

    precipitation = []
    for date, prcp in prcp_scores:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        precipitation.append(precipitation_dict)

    return jsonify(precipitation)

#################################################
# Stations
#################################################

@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(Station.station, Station.name)

    return jsonify(stations)

#################################################
# Tobs
#################################################

@app.route("/api/v1.0/tobs")
def tobs():
    last_twelve = dt.date(2017, 8, 23) - dt.timedelta(days= 365)
    twelve_temp_data = session.query(Measurement.tobs).filter(Measurement.date >= last_twelve, Measurement.station == "USC00519281").order_by(Measurement.tobs).all()

    return jsonify(twelve_temp_data)

#################################################
# Start
#################################################

@app.route("/api/v1.0/<start>")
def start():
    start_date = Measurement.date <= "2010-01-01"
    end_date = Measurement.date >= "2017-08-23"
    temp_data_start = session.query(Measurement.tobs).filter(Measurement.date >= start_date).all()
    temp_start_df = pd.DataFrame(temp_data_start)

    tmins = temp_start_df["tobs"].min()
    tavgs = temp_start_df["tobs"].mean()
    tmaxs = temp_start_df["tobs"].max()

    return jsonify(tmins, tavgs, tmaxs)

#################################################
# Start & End
#################################################

@app.route("/api/v1.0/<start>/<end>")
def startend():
    start_date = Measurement.date <= "2010-01-01"
    end_date = Measurement.date >= "2017-08-23"
    temp_data_ = session.query(Measurement.tobs).filter(Measurement.date.between(start_date, end_date)).all()
    temp_data_df = pd.DataFrame(temp_data)

    tmin = temp_data_df["tobs"].min()
    tavg = temp_data_df["tobs"].mean()
    tmax = temp_data_df["tobs"].max()

    return jsonify(tmin, tavg, tmax)

if __name__ == '__main__':
    app.run(debug=True)

