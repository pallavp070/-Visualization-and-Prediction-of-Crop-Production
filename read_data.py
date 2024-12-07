import pandas as pd
import pickle


def read_csv(file_path: str):
    df = pd.read_csv(file_path)
    return df


def load_model(file_path: str):
    return pickle.load(open(file_path, "rb"))
