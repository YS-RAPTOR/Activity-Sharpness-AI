import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report
from data import DATA

df = pd.read_csv(DATA)
target = "Activity"

SELECTED_FEATURES = [
    "SV L5 x",
    "SV L5 y",
    "SV L5 z",
    "SV T8 x",
    "SV Neck x",
    "SV Neck y",
    "SV Right Upper Arm x",
    "SV Right Forearm y",
    "SV Right Forearm z",
    "SV Right Hand y",
    "SV Right Hand z",
    "SV Left Upper Arm x",
    "SV Left Forearm x",
    "SV Left Forearm y",
    "SV Left Forearm z",
    "SV Left Hand x",
    "SV Left Hand y",
    "SV Left Hand z",
    "SV Right Upper Leg x",
    "SV Right Upper Leg y",
    "SV Right Lower Leg x",
    "SV Left Upper Leg x",
    "SV Left Upper Leg y",
    "SV Left Lower Leg x",
    "SV Left Foot x",
    "SA Left Shoulder z",
    "SA Right Upper Leg z",
    "SA Right Lower Leg z",
    "SA Left Upper Leg z",
    "SA Left Lower Leg z",
]

X, y = df[SELECTED_FEATURES], df[target].astype("category")

models = [
    "RandomForestClassifier",
    "DecisionTreeClassifier",
    "SGDClassifier",
    "HistGradientBoostingClassifier",
]


x_train, x_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


for model_name in models:
    model = None
    with open(f"./models/Models/model_{model_name}.pkl", "rb") as f:
        model = pickle.load(f)

    if model.__class__.__name__ == "HistGradientBoostingClassifier":
        y_te = y_test.cat.codes
    else:
        y_te = y_test

    y_pred = model.predict(x_test)

    print(f"Model: {model_name}")
    print("Classification Report:")
    print(classification_report(y_te, y_pred, zero_division=0))  # type: ignore
    print()

    print("Confusion Matrix:")
    print(confusion_matrix(y_te, y_pred))
    print()

    print("*" * 80)
    print()
