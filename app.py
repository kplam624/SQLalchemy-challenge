import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

climate_path = "Resources/hawaii.sqlite"
engine = create_engine(f'sqlite:///{climate_path}')

Base = automap_base()
Base.prepare(engine, reflect=True)

meas = Base.classes.measurement
sta = Base.classes.station

app = Flask(__name__)

@app.route("/")
def home():
    """Homepage for the api"""

    return (
        f"Welcome! Here are the following api routes.<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
        f"Use the following api route for more information on the the routes themselves.<br/>"
        f"/api/v1.0/help"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    sel = {meas.date, func.avg(meas.prcp)}

    prcp_val = session.query(*sel).\
        filter(meas.date > '2016-08-23').\
        group_by(meas.date).\
        order_by(meas.date).all()
    
    session.close()

    prcp = []
    for date, average in prcp_val:
        prcp_dict = {}
        prcp_dict['Date'] = date
        prcp_dict['Average Precipitation'] = average
        prcp.append(prcp_dict)
    
    return jsonify(prcp)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    results = session.query(sta.station).all()

    session.close()

    station = []
    for name in results:
        station_dict = {}
        station_dict['Name'] = name
        station.append(station_dict)
    
    return jsonify(station)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    sel3 = (meas.date, meas.tobs)
    station_tobs = session.query(*sel3).filter(meas.date > '2016-08-23',meas.station == 'USC00519281').\
        group_by(meas.date).\
        order_by(meas.date).all()
    
    session.close()

    tob = []
    for date, temp in station_tobs:
        stat_tobs={}
        stat_tobs['Date'] = date
        stat_tobs['Temperature'] = temp
        tob.append(stat_tobs)

    return jsonify(tob)

@app.route("/api/v1.0/<start>")
def temp(start):
    session = Session(engine)
    temperature = session.query(func.min(meas.tobs),func.max(meas.tobs),func.avg(meas.tobs)).\
        filter(meas.date >= start).all()
    session.close()

    temp_imp = []
    for min,max,avg in temperature:
        temp_dict = {}
        temp_dict['Min'] = min
        temp_dict['Max'] = max
        temp_dict['Average'] = avg
        temp_imp.append(temp_dict)
    
    if temp_imp[0]['Min'] is None:
        return "Oops. Something went wrong. Is your date in the YYYY-MM-DD format?<br/>" \
            "Please try again or go to /api/v1.0/help"

    return jsonify(temp_imp) 

@app.route("/api/v1.0/<start>/<end>")
def temps(start, end):
    session = Session(engine)
    temperatures = session.query(func.min(meas.tobs),func.max(meas.tobs),func.avg(meas.tobs)).\
        filter(meas.date >= start,meas.date <= end).all()
    session.close()

    temp_s_e = []
    for min,max,avg in temperatures:
        s_e_dict = {}
        s_e_dict['Min'] = min
        s_e_dict['Max'] = max
        s_e_dict['Average'] = avg
        temp_s_e.append(s_e_dict)

    return jsonify(temp_s_e)    

if __name__ == '__main__':
    app.run(debug=True)