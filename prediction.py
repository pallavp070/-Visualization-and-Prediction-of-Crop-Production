import pandas as pd

from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import LabelEncoder

from mami_crop_project.read_data import read_csv, load_model
from mami_crop_project.schema import PredictionRequest


def get_prediction(input_data: PredictionRequest):
    # load model
    label_encoder: LabelEncoder = load_model(
        "./mami_crop_project/saved_models/GaussianNB_label_encoder.sav"
    )
    model: GaussianNB = load_model("./mami_crop_project/saved_models/GaussianNB.sav")

    # prepare data
    input = pd.DataFrame({k: [v] for k, v in input_data.dict().items()})

    # predict
    y_predict = model.predict(input)
    predicted_label = label_encoder.inverse_transform(y_predict)
    return predicted_label[0]
