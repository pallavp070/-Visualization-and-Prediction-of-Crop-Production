import numpy as np
import pickle

from sklearn import preprocessing
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from mami_crop_project.read_data import read_csv

from sklearn.linear_model import LogisticRegression
def train_model():
    # read data
    data = read_csv("./mami_crop_project/data/SoilEnvForCrop.csv")

    # separate features and label columns
    feature_columns = data.columns[:-1]
    features = data[feature_columns]
    features = features.rename(
        columns={"N": "nitrogen", "P": "phosphorus", "K": "potassium", "ph": "ph_level"}
    )

    label = data["label"]

    # convert labels to encodings
    label_encoder = preprocessing.LabelEncoder()
    label = label_encoder.fit_transform(label)

    # split data into train and test set
    x_train, x_test, y_train, y_test = train_test_split(
        features, label, test_size=0.3, random_state=99
    )

    # train Gaussian Naive Bayes model
    #model = GaussianNB()
    #model=SVC()
    model=RandomForestClassifier()
    #model=LogisticRegression()
    #model = DecisionTreeClassifier()
    model.fit(x_train, y_train)

    # evaluate
    y_pred = model.predict(x_test)
    print("")
    print("Accuracy as per RandomForestClassifier" ,model.score(x_test, y_test))
    print("")
    print(classification_report(np.array(y_test), np.array(y_pred)))

    # save model
    pickle.dump(
        label_encoder,

        #open("./mami_crop_project/saved_models/DecisionTreeClassifier_label_encoder.sav", "wb")
        #open("./mami_crop_project/saved_models/LogisticRegression_label_encoder.sav", "wb")
        #open("./mami_crop_project/saved_models/SVC_label_encoder.sav", "wb")
        #open("./mami_crop_project/saved_models/GaussianNB_label_encoder.sav", "wb"),

       open("./mami_crop_project/saved_models/RandomForestClassifier_encoder.sav", "wb"),
    )
    #pickle.dump(model, open("./mami_crop_project/saved_models/LogisticRegression.sav", "wb"))
    #pickle.dump(model, open("./mami_crop_project/saved_models/SVC.sav", "wb"))
    #pickle.dump(model, open("./mami_crop_project/saved_models/GaussianNB.sav", "wb"))
    pickle.dump(model, open("./mami_crop_project/saved_models/RandomForest.sav", "wb"))
    #pickle.dump(model, open("./mami_crop_project/saved_models/DecisionTreeClassifier.sav", "wb"))
    print("")
    


if __name__ == "__main__":
    train_model()
