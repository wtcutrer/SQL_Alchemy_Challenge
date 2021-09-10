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
    return (f"Surfs Up, bro! Welcome to my SQLAlchemy Challenge API!<br/>"
            f"----------------------------------------------------<br/>"
            f"Available Routes for you to explore!<br/>"
            f"----------------------------------------------------<br/>"
            f"Precipation Data = /api/v1.0/precipitaton<br/>"
            f"----------------------------------------------------<br/>"
            f" Weather Observation stations list = /api/v1.0/stations<br/>"
            f"----------------------------------------------------<br/>"
            f"Temperature Data = /api/v1.0/temperature<br/>"
            f"----------------------------------------------------<br/>"
            f"Lists the average, maximum, and minimum tobs for date given = /api/v1.0/<start>(yyyy-mm-dd)<br/>"
            f"----------------------------------------------------<br/>"
            f"Lists the average, maximum, and minimum tobs for date range given = /api/v1.0/<start>/<end>(yyyy-mm-dd/yyyy-mm-dd)<br/>")

@app.route("/api/v1.0/precipitaton")
def precipitation():
      #Create a queries that filters for only the last year of Precipitation Data
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= "2016-08-23").all()
    results_json = [results]
    session.close()   
    
    return jsonify(results_json)

@app.route("/api/v1.0/stations")
def stations():
     #Return a list of the stations
    results = session.query(Station.name).all()
    stations_json = list(np.ravel(results))
    session.close()   
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
    session.close()   
    return jsonify(temps)         
                   
@app.route("/api/v1.0/<start>")
def start_date(start):
    start_date_results = session.query(func.avg(Measurement.tobs), func.max(Measurement.tobs),func.min(Measurement.tobs)).\
        filter(Measurement.date >= start).all()    
    session.close()            
      
    start_data = []
    for min, max, avg in start_date_results:
        start_dict = {}
        start_dict['MIN'] = min
        start_dict['MAX'] = max
        start_dict['AVG'] = avg
        start_data.append(start_dict)
    return jsonify(start_data)              
                   
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):                   
    range_results = session.query(func.avg(Measurement.tobs), func.max(Measurement.tobs), func.min(Measurement.tobs)).\
        filter(Measurement.date >= start, Measurement.date <= end).all()
    session.close()
       
    range_data = []
    for min, max, avg in range_results:
        start_end_dict = {}
        start_end_dict['MIN'] = min
        start_end_dict['MAX'] = max
        start_end_dict['AVG'] = avg
        range_data.append(start_end_dict)
    return jsonify(range_data)
        
if __name__ == '__main__':
    app.run(debug=True) 
    