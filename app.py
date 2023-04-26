from flask import Flask, render_template, request
from main import fmi_method, handle_inputs

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("form.html")


@app.route("/result", methods=["GET", "POST"])
def result():
    inputs = {}
    for key, value in request.form.items():
        inputs[key] = value
    handled_inputs = handle_inputs(inputs)
    result = fmi_method(handled_inputs)
    return render_template(
        "result.html",
        fmi=result["indexes"]["fmi"],
        di=result["indexes"]["di"],
        divi=result["indexes"]["divi"],
        pi=result["indexes"]["pi"],
    )


@app.route("/map", methods=["GET"])
def map():
    return render_template("map.html")


if __name__ == "__main__":
    app.run(debug=True)
