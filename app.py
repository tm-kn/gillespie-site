import csv
import io

from flask import Flask, jsonify, make_response, render_template, request

from gillespie import gillespie

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/data/")
def gillespie_data():
    data = list(
        gillespie(
            population=int(request.args.get("population", 350)),
            maximum_elapsed_time=float(request.args.get("maximum_elapsed_time", 1000)),
            start_time=float(request.args.get("start_time", 0.0)),
            spatial_parameter=float(request.args.get("spatial_parameter", 100.0)),
            rate_of_infection_after_contact=float(
                request.args.get("rate_of_infection_after_contact", 10.0)
            ),
            rate_of_cure=float(request.args.get("rate_of_cure", 0.5)),
            infected_population=int(request.args.get("infected_population", 1)),
        )
    )
    json_data = jsonify([point.as_dict() for point in data])
    return json_data


@app.route("/export-csv/")
def export_csv():
    data = list(
        gillespie(
            population=int(request.args.get("population", 350)),
            maximum_elapsed_time=float(request.args.get("maximum_elapsed_time", 1000)),
            start_time=float(request.args.get("start_time", 0.0)),
            spatial_parameter=float(request.args.get("spatial_parameter", 100.0)),
            rate_of_infection_after_contact=float(
                request.args.get("rate_of_infection_after_contact", 10.0)
            ),
            rate_of_cure=float(request.args.get("rate_of_cure", 0.5)),
            infected_population=int(request.args.get("infected_population", 1)),
        )
    )
    csv_file = io.StringIO()
    dict_writer = csv.DictWriter(
        csv_file, fieldnames=["Time", "Susceptible", "Infected", "Recovered"]
    )
    dict_writer.writeheader()
    for point in data:
        dict_writer.writerow(
            {
                "Time": point.time,
                "Susceptible": point.susceptible_population,
                "Infected": point.infected_population,
                "Recovered": point.recovered_population,
            }
        )
    response = make_response(csv_file.getvalue())
    response.headers["content-type"] = "text/csv"
    response.headers["content-disposition"] = "attachment; filename=gillespie.csv"
    return response
