import pickle
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report
from data import DATA
from common import load_dataset


target = "Activity"
SELECTED_FEATURES = [
    "SV L5 x",
    "SV L5 y",
    "SV L5 z",
    "SV Neck x",
    "SV Neck y",
    "SV Right Forearm y",
    "SV Right Forearm z",
    "SV Right Hand y",
    "SV Right Hand z",
    "SV Left Upper Arm x",
    "SV Left Forearm y",
    "SV Left Hand x",
    "SV Left Hand y",
    "SV Left Hand z",
    "SV Left Lower Leg x",
    "SV Left Foot x",
]

X, y = load_dataset(DATA, target, selected_features=SELECTED_FEATURES)
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
    with open(f"./models/Models_{target}/model_{model_name}.pkl", "rb") as f:
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
