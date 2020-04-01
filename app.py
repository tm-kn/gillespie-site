import csv
import io
import tempfile

from flask import (
    abort,
    Flask,
    jsonify,
    make_response,
    render_template,
    request,
    redirect,
    url_for,
)
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from gillespie import gillespie

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/export-json/")
def export_json():
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
    csv_file = tempfile.TemporaryFile(mode="r+")
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
    csv_file.seek(0)
    response = make_response(csv_file.read())
    csv_file.close()
    response.headers["content-type"] = "text/csv"
    response.headers["content-disposition"] = "attachment; filename=gillespie.csv"
    return response


@app.route("/export-graph/")
def default_graph_export():
    return redirect(url_for("export_graph", format="svg"))


@app.route("/export-graph/<format>/")
def export_graph(format="svg"):
    if format not in ("svg", "png"):
        return abort(400, "Invalid format requested")
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
    plt.cfl()
    plt.plot(
        [x.time for x in data],
        [x.susceptible_population for x in data],
        "b",
        label="Susceptible",
    )
    plt.plot(
        [x.time for x in data],
        [x.infected_population for x in data],
        "r",
        label="Infected",
    )
    plt.plot(
        [x.time for x in data],
        [x.recovered_population for x in data],
        "g",
        label="Recovered",
    )
    plt.xlabel("Tme units (generic) log scale")
    plt.ylabel("Cases from 1 index case")
    plt.title("Susceptible, Infected and Recovered - cases vs. log (time)")
    plt.legend()
    file_object = tempfile.TemporaryFile()
    plt.savefig(file_object, dpi=300, format=format, orientation="landscape")
    plt.clf()
    file_object.seek(0)
    response = make_response(file_object.read())
    file_object.close()
    if format == "png":
        response.headers["content-type"] = "image/png"
    elif format == "svg":
        response.headers["content-type"] = "image/svg+xml"
    return response
