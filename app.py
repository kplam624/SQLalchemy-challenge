# Imported dependancies

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Importing flask and jsonify for api creation.
from flask import Flask, jsonify

# Creating a path to the sql database.
climate_path = "Resources/hawaii.sqlite"

# Creating an engine that connects to the database.
engine = create_engine(f'sqlite:///{climate_path}')

# Creates a base to reflect the tables to create classes.
Base = automap_base()
Base.prepare(engine, reflect=True)

# Creates the classes that are reflected by the tables.
meas = Base.classes.measurement
sta = Base.classes.station

# Starting the app.
app = Flask(__name__)

# Home route.
@app.route("/")
def home():
    """Homepage for the api"""
    # Shows the routes.
    return (
        f"Welcome! Here are the following api routes.<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
        f"<br/> Use the following api route for more information on the the routes themselves.<br/>"
        f"/api/v1.0/help"
    )

# Route for Precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():

    # Create session connecting to the engine.
    session = Session(engine)

    # Query values
    sel = {meas.date, func.avg(meas.prcp)}

    # Session Query
    prcp_val = session.query(*sel).\
        filter(meas.date > '2016-08-23').\
        group_by(meas.date).\
        order_by(meas.date).all()

    # Closing the session
    session.close()

    # Empty list to add the dictionary values to.
    prcp = []
    for date, average in prcp_val:
        prcp_dict = {}
        prcp_dict['Date'] = date
        prcp_dict['Average Precipitation'] = average
        prcp.append(prcp_dict)
    
    # jsonify the results
    return jsonify(prcp)

@app.route("/api/v1.0/stations")
def stations():

     # Create session connecting to the engine.
    session = Session(engine)
    
    # Session Query
    results = session.query(sta.station).all()

    # Closing the session
    session.close()

    # Empty list to add the dictionary values to.
    station = []
    for name in results:
        station_dict = {}
        station_dict['Name'] = name
        station.append(station_dict)
    
    # jsonify the results
    return jsonify(station)

@app.route("/api/v1.0/tobs")
def tobs():
     # Create session connecting to the engine.
    session = Session(engine)

    # Session Query
    sel3 = (meas.date, meas.tobs)
    station_tobs = session.query(*sel3).filter(meas.date > '2016-08-23',meas.station == 'USC00519281').\
        group_by(meas.date).\
        order_by(meas.date).all()

    # Closing the session
    session.close()

    # Empty list to add the dictionary values to.
    tob = []
    for date, temp in station_tobs:
        stat_tobs={}
        stat_tobs['Date'] = date
        stat_tobs['Temperature'] = temp
        tob.append(stat_tobs)

    # jsonify the results
    return jsonify(tob)

@app.route("/api/v1.0/<start>")
def temp(start):
     # Create session connecting to the engine.
    session = Session(engine)

    # Session Query
    temperature = session.query(func.min(meas.tobs),func.max(meas.tobs),func.avg(meas.tobs)).\
        filter(meas.date >= start).all()

    # Closing the session
    session.close()

    # Empty list to add the dictionary values to.
    temp_imp = []
    for min,max,avg in temperature:
        temp_dict = {}
        temp_dict['Min'] = min
        temp_dict['Max'] = max
        temp_dict['Average'] = avg
        temp_imp.append(temp_dict)

    # Error message    
    if temp_imp[0]['Min'] is None:
        return "Oops. Something went wrong. Is your date in the YYYY-MM-DD format?<br/>" \
            "Please try again or go to /api/v1.0/help"

    # jsonify the results
    return jsonify(temp_imp) 

@app.route("/api/v1.0/<start>/<end>")
def temps(start, end):

     # Create session connecting to the engine.
    session = Session(engine)

    # Session Query
    temperatures = session.query(func.min(meas.tobs),func.max(meas.tobs),func.avg(meas.tobs)).\
        filter(meas.date >= start,meas.date <= end).all()

    # Closing the session
    session.close()

    # Empty list to add the dictionary values to.
    temp_s_e = []
    for min,max,avg in temperatures:
        s_e_dict = {}
        s_e_dict['Min'] = min
        s_e_dict['Max'] = max
        s_e_dict['Average'] = avg
        temp_s_e.append(s_e_dict)

    # Error message
    if temp_s_e[0]['Min'] is None:
        return "Oops. Something went wrong. Is your date in the YYYY-MM-DD format?<br/>" \
            "Please try again or go to /api/v1.0/help"

    # jsonify the results
    return jsonify(temp_s_e)    

@app.route("/api/v1.0/help")
def help():
    # Creating a route that holds information on the api.
    return f"Hi, this is a quick rundown on what each route does. <br/>"\
        "<br/> The api will pull from a database that contains the climate data from Hawaii (currently upto 2017). <br/>"\
        "/api/v1.0/precipitation shows the precipitation shows the precipitation data for the past year (2016-2017).<br/>"\
        "/api/v1.0/stations shows how many stations collected data. <br/>"\
        "/api/v1.0/tobs shows the Temperature Observation Data (TOBS) at the most active station (USC00519281)<br/>"\
        "/api/v1.0/start shows the min, max and average temperature after the requested date(Up to 2017-08-23). Replace 'start' with a date in YYYY-MM-DD format.<br/>"\
        "/api/v1.0/start/end shows the min, max and average temperature between the requested dates (Up to 2017-08-23). Replace 'start' and 'end' with a date in YYYY-MM-DD format."\


# Last line of the api. Debugger.
if __name__ == '__main__':
    app.run(debug=True)