from matplotlib import pyplot as plt
import numpy as np
from mami_crop_project.read_data import read_csv


def get_matching_state(state, all_states):
    for full_state_name in all_states:
        if state == full_state_name or state in full_state_name:
            return full_state_name


def read_data():
    csv_path = "./mami_crop_project/data/CostOfPro.csv"
    data = read_csv(csv_path)
    return data


def plot_for_selected_entity(selected_value: str, selected_parent_entity: str) -> str:
    data = read_data()

    if selected_parent_entity == "state":
        state_name = get_matching_state(
            state=selected_value, all_states=data["State"].unique()
        )

        if state_name is None:
            raise ValueError(f"Invalid state provided: {selected_value}")

    cols_to_plot = [
        "Cost_of_Cultivation_Per_Hectare",
        "Cost_of_Production_per_Quintal",
        "Yield_Quintal_Per_Hectare",
    ]

    if selected_parent_entity == "state":
        df_to_plot = data[data["State"] == state_name]
        df_to_plot = df_to_plot.set_index("Crop")
    elif selected_parent_entity == "crop":
        df_to_plot = data[data["Crop"] == selected_value]
        df_to_plot = df_to_plot.set_index("State")

    fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(20, 20))
    plt.subplots_adjust(hspace=0.3)
    for i, col in enumerate(cols_to_plot):
        df_to_plot[[col]].plot(kind='bar', ax=axes[i])
 
    file_name = f"{selected_value}.png"
    plt.savefig(f"mami_crop_project/static/images/{file_name}")
    return file_name


def get_crop_production_year_data():
    file_path = "./mami_crop_project/data/CropProductionYear.csv"
    df = read_csv(file_path=file_path)
    return df

def plot_for_crop(selected_crop: str, selected_entity: str):
    data = read_data()
    df_to_plot = data[data["Crop"] == selected_crop]
    df_to_plot = df_to_plot.set_index("State")
    
    
    
    if selected_entity =="Cost_of_Production_per_Quintal":
        df_to_plot[["Cost_of_Production_per_Quintal"]].plot(kind="bar", figsize=(10, 8), rot=0)
        file_name=f"{selected_crop}_Crop_Cost_of_production_per_quintal.png"
    

    if selected_entity =="Cost_of_Cultivation_Per_Hectare":
        df_to_plot[["Cost_of_Cultivation_Per_Hectare"]].plot(kind="bar", figsize=(10, 8), rot=0)
        file_name=f"{selected_crop}_Crop_Cost_of_Cultivation_Per_Hectare.png"

    if selected_entity =="Yield_Quintal_Per_Hectare":
        df_to_plot[["Yield_Quintal_Per_Hectare"]].plot(kind="line", figsize=(10, 8), rot=0)
        file_name=f"{selected_crop}_Crop_Yield_Quintal_Per_Hectare.png"
        plt.ylabel ("Quintal pe Hectare")  

    plt.savefig(f"mami_crop_project/static/images/{file_name}")
    return file_name


def plot_crop_production_for_given_year(year: str):
    data = get_crop_production_year_data()
    select_row = data[data["Year"]==year]
    x_axis = select_row.drop(columns=["Year"])
    x_axis = x_axis.squeeze()
    plt.figure(figsize=(12, 13))
    x_axis.plot(kind="bar")
    file_name=f"{year}.png"
    plt.savefig(f"mami_crop_project/static/images/{file_name}")
    return file_name
