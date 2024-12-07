from flask import render_template, request
from flask import Flask, jsonify

from pathlib import Path

from mami_crop_project.helper import read_data, plot_for_selected_entity, get_crop_production_year_data, plot_crop_production_for_given_year, plot_for_crop
from mami_crop_project.schema import PredictionRequest
from mami_crop_project.prediction import get_prediction

app = Flask(__name__)

@app.route("/graphs")
def graphs():
    return render_template("GraphList.html")

@app.route("/home")
def home():
    return render_template("HomePage.html")

@app.route("/graph_list")
def graph_list():
    return render_template("GraphList.html")


@app.route("/viz")
def select_entity():
    return render_template("index.html")

@app.route("/pcy")
def production_of_crop_per_year():
    data = get_crop_production_year_data()
    all_years = data["Year"].unique()
    return render_template(
        "crop_production_per_year.html",
        all_years=all_years
    )

@app.route("/ccrop", methods=["POST", "GET"])
def list_all_ccrops():
    data = read_data()
    all_crops = data["Crop"].unique()
    return render_template(
        "draw_ccrop.html",
        all_crops=all_crops,
     )
@app.route("/pcrop", methods=["POST", "GET"])
def list_all_pcrops():
    data = read_data()
    selected_entity ="pcrop" 
    all_crops = data["Crop"].unique()
    return render_template(
        "draw_selected_graph_type.html",
        all_crops=all_crops,
        selected_entity=selected_entity
        
    )
@app.route("/ycrop", methods=["POST", "GET"])
def list_all_ycrops():
    data = read_data()
    all_crops = data["Crop"].unique()
    return render_template(
        "draw_ycrop.html",
        all_crops=all_crops,
    )


@app.route("/choose_entity", methods=["POST"])
def test_endpoint_from_javascript():
    selected_option = request.form.get("selected_option")
    if selected_option == "visualization":
        return render_template("visualization.html")
    elif selected_option == "prediction":
        return render_template("predictor.html")


@app.route("/select_entity", methods=["POST", "GET"])
def selected_value_for_entity():
    selected_entity = request.form.get("selected_entity")
    data = read_data()

    all_values_in_selected_entity = []
    if selected_entity == "state":
        all_values_in_selected_entity = list(data["State"].unique())
    elif selected_entity == "crop":
        all_values_in_selected_entity = list(data["Crop"].unique())
    return render_template(
        "entity_value_selector.html",
        values_in_selected_entity=all_values_in_selected_entity,
        selected_entity=selected_entity,
    )


@app.route("/print-plot", methods=["POST", "GET"])
def plot_png():
    selected_parent_entity = request.form.get("selected_parent_entity")
    selected_value = request.form.get("selected_value")
    file_name = f"{selected_value}.png"
    full_path = Path().absolute() / f"mami_crop_project/static/images/{file_name}"
    if not full_path.exists():
        file_name = save_plt_image(selected_value, selected_parent_entity)

    return render_template(
        "plot.html",
        name=f"Plot for {selected_value}",
        url=f"/static/images/{file_name}",
    )


@app.route("/predict", methods=["POST", "GET"])
def predict():
    request_body = PredictionRequest(**request.form)
    predicted_result = get_prediction(request_body)
    return jsonify({"output": predicted_result})

@app.route("/get_crop_plot", methods=["POST", "GET"])
def get_crop_plot():
    selected_crop = request.form.get("selected_crop")
    selected_entity = "Cost_of_Production_per_Quintal"
    image_name = plot_for_crop(selected_crop=selected_crop, selected_entity=selected_entity)
    return jsonify({"url":f"/static/images/{image_name}"})


@app.route("/get_ccrop_plot", methods=["POST", "GET"])
def get_ccrop_plot():
    selected_crop = request.form.get("selected_crop")
    selected_entity = "Cost_of_Cultivation_Per_Hectare"
    image_name = plot_for_crop(selected_crop=selected_crop, selected_entity=selected_entity)
    return jsonify({"url":f"/static/images/{image_name}"})


@app.route("/get_ycrop_plot", methods=["POST", "GET"])
def get_ycrop_plot():
    selected_crop = request.form.get("selected_crop")
    selected_entity = "Yield_Quintal_Per_Hectare"
    image_name = plot_for_crop(selected_crop=selected_crop, selected_entity=selected_entity)
    return jsonify({"url":f"/static/images/{image_name}"})

@app.route("/get_crop_production_for_year_plot", methods=["POST"])
def get_crop_production_for_year_plot():
    selected_year = request.form.get("selected_year")

    image_name = plot_crop_production_for_given_year(year=selected_year)
    return jsonify({"url":f"/static/images/{image_name}"})


def save_plt_image(selected_value: str, selected_parent_entity: str):
    file_loc = plot_for_selected_entity(
        selected_value=selected_value, selected_parent_entity=selected_parent_entity
    )
    return file_loc

#poetry run  python .\mami_crop_project\main.py

if __name__ == "__main__":
    app.run()
