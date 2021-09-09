import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#Create engine and start session
engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={'check_same_thread': False})

#Create automap
Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)


@app.route("/")
def home():
    return (f"Welcome<br/>"
            f"----------------------------------------------------<br/>"
            f"Available Routes:<br/>"
            f"----------------------------------------------------<br/>"
            f"/api/v1.0/precipitaton -- Preceipitation data<br/>"
            f"----------------------------------------------------<br/>"
            f"/api/v1.0/stations ------ Weather observation stations<br/>"
            f"----------------------------------------------------<br/>"
            f"/api/v1.0/temperature --- Temperature data<br/>"
            f"----------------------------------------------------<br/>"
            f"/api/v1.0/start---------- Datesearch (yyyy-mm-dd)--- Lists the minimum temperature, the average temperature, and the max temperature for date given.<br/>"
            f"----------------------------------------------------<br/>"
            f"/api/v1.0/start/end-------Datesearch (yyyy-mm-dd/yyyy-mm-dd)-- Lists the minimum temperature, the average temperature, and the max temperature for date range given.<br/>")

@app.route("/api/v1.0/precipitaton")
def precipitation():
      #Create a queries that filters for only the last year of Precipitation Data
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= "2016-08-23").all()
    results_json = [results]
    return jsonify(results_json)

@app.route("/api/v1.0/stations")
def stations():
     #Return a list of the stations
    results = session.query(Station.name).all()
    stations_json = list(np.ravel(results))
    return jsonify(stations_json) 
                   
@app.route("/api/v1.0/temperature")   
    #Return TOBS from last year and filter them down by msot active station         
def temp_monthly():
    # Calculate the year
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    #create query
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps)         
                   
@app.route("/api/v1.0/<start>")
def start_date(start):
    results = session.query(Measurement.date, func.avg(Measurement.tobs), func.max(Measurement.tobs),func.min(Measurement.tobs)).\
        filter(Measurement.date >= start).all()               
    start_json = list(np.ravel(results))
    return jsonify(start_json)               
                   
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):                   
    results = session.query(func.avg(Measurement.tobs), func.max(Measurement.tobs), func.min(Measurement.tobs)).\
        filter(Measurement.date >= start, Measurement.date <= end).all()
    end_json = list(np.ravel(results))
    return jsonify(end_json)
        
if __name__ == '__main__':
    app.run(debug=True) 