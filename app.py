import numpy as np
import datetime as dt
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
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>" 
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a dictionary of all dates and their precipitation value"""
    # Query 
    results = session.query(Measurement.date, Measurement.prcp).all()

    # Convert list of tuples into normal list
    dates_prcp = []
    for date, precipitation in results:
        dates_prcp_dict={}
        dates_prcp_dict['date']= date
        dates_prcp_dict['pricipitation']=prcp
        dates_prcp.append(dates_prcp_dict)

    return jsonify(dates_prcp)


@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all stations"""
    # Query all stations
    results = session.query(Station.station).all()
    all_stations=list(np.ravel(results))
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of dates and temperature observations"""
    # Query dates and temperature observations from a year from the last data point
    query = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= dt.date(2017,8,23)-dt.timedelta(days=365)).all()    
    last_year_tobs=list(np.ravel(query))
    return jsonify(last_year_tobs)

@app.route("/api/v1.0/start")
def start_date():
    """Return a list of total min, avg, and max for all dates equal to and greater than the start date"""
    # Create function
    def calc_temps(start_date):
        query=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date>=start_date).all()
        start_date_list=list(np.ravel(query))
        return jsonify(start_date_list)


@app.route("/api/v1.0/start/end")
def end_date():
    """Return a list of total min, avg, and max for all dates between the start and end date"""
    # Create function
    def calc_temps(start_date):
        query=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
        start_end_list=list(np.ravel(query))
        return jsonify(start_end_list)

if __name__ == '__main__':
    app.run(debug=True)
