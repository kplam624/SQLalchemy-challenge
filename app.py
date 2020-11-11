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


if __name__ == '__main__':
    app.run(debug=True)