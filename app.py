import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={'check_same_thread': False})


Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)


@app.route("/")
def home():
    return (f"Surfs Up! Welcom to my SQLAlchemy Challenge API!<br/>"
            f"----------------------------------------------------<br/>"
            f"Here are the Available Routes:<br/>"
            f"----------------------------------------------------<br/>"
            f"/api/v1.0/precipitaton -- This Route gives Data on Preceipitation data<br/>"
            f"----------------------------------------------------<br/>"
            f"/api/v1.0/stations ------ This Route gives Data on Weather observation stations<br/>"
            f"----------------------------------------------------<br/>"
            f"/api/v1.0/temperature --- This Route gives Data on Temperature Observation Data (TOBS) with the Most Active Station<br/>"
            f"----------------------------------------------------<br/>"
            f"/api/v1.0/start---------- Datesearch (yyyy-mm-dd)--- This Route lists the minimum temperature, the average temperature, and the max temperature for date given.<br/>"
            f"----------------------------------------------------<br/>"
            f"/api/v1.0/start/end-------Datesearch (yyyy-mm-dd/yyyy-mm-dd)-- This Route lists the minimum temperature, the average temperature, and the max temperature for date range given.<br/>")

@app.route("/api/v1.0/precipitation")
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
                   
@app.route("/api/v1.0/tobs")
def temp_obs():                   
   #Return TOBS from last year and filter them down by msot active station
    results = session.query(Station.name, Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= "2016-08-23").filter(Measurement.station == 'USC00519281').all()
    obs_json = list(np.ravel(results))
    return jsonify(obs_json)      
                                
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