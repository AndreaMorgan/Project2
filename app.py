import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template

app = Flask(__name__)


#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///data/BOTULISM.db")

Base = automap_base()
Base.prepare(engine, reflect=True)

# Save reference to Botulism table
bot_data = Base.classes.BOTULISM


#################################################
# Flask Routes
#################################################

@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")

@app.route("/data")
def datatable():
    """Return the data page."""
    return render_template("data.html")

@app.route("/cleanup")
def cleanup():
    """Return the data cleanup page."""
    return render_template("cleanup.html")

@app.route("/about")
def about():
    """Return the about page."""
    return render_template("about.html")

@app.route("/botulism")
def botulism():
    """Return the botulism page."""
    return render_template("botulism.html")

@app.route("/history")
def history():
    """Return the history page."""
    return render_template("history.html")

@app.route("/types")
def types():
    """Return the history page."""
    return render_template("types.html")

@app.route("/safety")
def safety():
    """Return the history page."""
    return render_template("safety.html")


@app.route("/allresults")
#Route retuns json of all records in dataset
def all():

    session = Session(engine)

    all_results = session.query(bot_data.state_name, 
                                bot_data.record_year, 
                                bot_data.BotType,
                                bot_data.ToxinType,
                                bot_data.record_count,
                                bot_data.BotId).all()

    session.close()

    all_records = []

    for state, year, botType, toxType, count, botID in all_results:
        results_dict = {}
        results_dict["state"] = state
        results_dict["year"] = year
        results_dict["botType"] = botType
        results_dict["toxType"] = toxType
        results_dict["count"] = count
        results_dict["botID"] = botID
        all_records.append(results_dict)

    return jsonify(all_records)

@app.route("/states")
#Route returns list of unique state names
def statenames():

    session = Session(engine)

    all_states = session.query(bot_data.state_name).distinct().all()

    session.close()

    state_names = []

    for i in all_states:
        for state in i:
            #create dict here if necessary to work in app
            state_names.append(state)

    return jsonify(state_names)

@app.route("/bottypes")
#Route returns list of unique Botulism types
def botTypes():

    session = Session(engine)

    all_botTypes = session.query(bot_data.BotType).distinct().all()

    session.close()

    bot_types = []

    for i in all_botTypes:
        for kind in i:
            #create dict here if necessary to work in app
            bot_types.append(kind)
     
    return jsonify(bot_types)  

@app.route("/toxtypes")
#Route returns list of unique toxin types
def toxTypes():

    session = Session(engine)

    all_toxTypes = session.query(bot_data.ToxinType).distinct().all()

    session.close()

    tox_types = []

    for i in all_toxTypes:
        for kind in i:
            #create dict here if necessary to work in app
            tox_types.append(kind)

    return jsonify(tox_types)

@app.route("/years")
#Returns list of unique years

def record_years():

    session = Session(engine)

    all_years = session.query(bot_data.record_year).order_by(bot_data.record_year).distinct().all()

    session.close()

    years = []

    for i in all_years:
        for year in i:
            #create dict here if necessary to work in app
            years.append(year)


    return jsonify(years)


@app.route("/stacey")
#Route retuns json of all records in dataset
def f_stacey():
    session = Session(engine)

    all_results = session.query(bot_data.state_name, 
                                bot_data.record_year, 
                                bot_data.BotType,
                                bot_data.ToxinType,
                                bot_data.record_count,
                                bot_data.BotId).all()

    session.close()

    all_records = []

    for state, year, botType, toxType, count, botID in all_results:
        results_dict = {}
        results_dict["state"] = state
        results_dict["year"] = year
        results_dict["botType"] = botType
        results_dict["toxType"] = toxType
        results_dict["count"] = count
        results_dict["botID"] = botID
        all_records.append(results_dict)

    
    df = pd.DataFrame(all_records)
    table = pd.pivot_table(df, values='count', index=['toxType'], columns=['botType'], aggfunc=np.sum).fillna(0).to_json()

    return jsonify(table)




if __name__ == "__main__":
    app.run()
