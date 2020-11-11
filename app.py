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


if __name__ == '__main__':
    app.run(debug=True)