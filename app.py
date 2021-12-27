from flask import Flask, render_template, jsonify, request
import pandas as pd
import numpy as np
from modelHelper import ModelHelper

# Create an instance of Flask
app = Flask(__name__)

# Route to render index.html template
@app.route("/")
def home():
    # Return template and data
    return render_template("index.html")

@app.route("/predict")
def about():
    # Return template and data
    return render_template("predict.html")

@app.route("/explorer")
def effects():
    # Return template and data
    #change this to dictionary
    #call function
    return render_template("explorer.html")

@app.route("/team")
def dashboard():
    # Return template and data
    return render_template("team.html")

@app.route("/makePredictions", methods=["POST"])
def makePredictions():
    print('postrequest')
    content = request.json["data"]
    print(content)
    # parse
    
    age_group = content["age_group"]
    sex = content["sex"]
    other_meds = int(content["other_meds"])
    history = int(content["history"])
    prior_vax = int(content["prior_vax"])
    allergies = int(content["allergies"])
    vax_name = content["vax_name"]
    vax_dose = content["vax_dose"]

    predict = ModelHelper.makePredictions(age_group, sex, other_meds, history, prior_vax, allergies, vax_name, vax_dose)
    print(type(predict))
    print(predict)
    pred = predict[0]
    if pred[0] == 0:
        severity = "Mild"
    elif pred[0] == 1:
        severity = "Moderate"
    else:
        severity =  "Severe"

    print(severity)

    pred_words = predict[1]
    print(pred_words)

    # print(type(pred))
    # prediction = dict(predict)

    word = predict[1]
    print(word[0])
    print(word[1])
    print(type(word))

    pred_dict = {"prediction": severity, "symptoms": pred_words}

    # word.append(pred_dict)
    
    # for i in word:
    #     print(i)

    # return_dict = {"return": word}
    
    print(pred_dict)


    # return(jsonify({"ok": True, "prediction": predict}))

    return pred_dict

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    return r

#main
if __name__ == "__main__":
    app.run(debug=True)