import pickle
import numpy as np
import pandas as pd
from sklearn.feature_selection import SelectKBest
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.linear_model import SGDClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import train_test_split
from sklearn.utils import class_weight
from data import DATA


df = pd.read_csv(DATA)
# NOTE: Change if you want to train on another target
target = "Activity"

SELECTED_FEATURES = None
NUMBER_OF_SELECTED_FEATURES = 10

drop_list = [
    # Number of occurrences are the same
    "SV Pelvis x",
    "SV Pelvis y",
    "SV Pelvis z",
    "SA Pelvis x",
    "SA Pelvis y",
    "SA Pelvis z",
    # Highly correlated with SV L5 ( > 0.95 )
    "SV L3 x",
    "SV L3 y",
    "SV L3 z",
    "SV T12 x",
    "SV T12 y",
    "SV T12 z",
    # Highly correlated with SV L5 z ( = 1 )
    "SV Neck z",
    # Highly correlated with SV T8 ( > 0.89 )
    "SV Head x",
    "SV Head y",
    "SV Right Shoulder x",
    "SV Right Shoulder y",
    "SV Left Shoulder x",
    "SV Left Shoulder y",
    # Highly correlated with SV Head z ( > 0.85 )
    "SV Right Shoulder z",
    "SV Left Shoulder z",
    # Toe and Foot are highly correlated ( = 1 )
    "SV Right Toe x",
    "SV Right Toe y",
    "SV Right Toe z",
    "SA Right Toe x",
    "SA Right Toe y",
    "SA Right Toe z",
    "SV Left Toe x",
    "SV Left Toe y",
    "SV Left Toe z",
    "SA Left Toe x",
    "SA Left Toe y",
    "SA Left Toe z",
    # Highly correlated with SA L5 ( > 0.95 )
    "SA L3 x",
    "SA L3 y",
    "SA L3 z",
    "SA T12 x",
    "SA T12 y",
    "SA T12 z",
    "SA T8 x",
    "SA T8 y",
    "SA Neck x",
    "SA Neck y",
    "SA Neck z",
    "Activity",
    "Worker",
    "Job",
    "Knife Sharpness",
    "Shift Number",
]


# Print data type of each column
for drop in drop_list:
    if drop == target:
        continue
    df.drop(drop, axis=1, inplace=True)

features = (
    [i for i in df.columns if i != target]
    if SELECTED_FEATURES is None
    else SELECTED_FEATURES
)


X, y = df[features], df[target]
# Feature Selection
if SELECTED_FEATURES is None:
    selector = SelectKBest(k=NUMBER_OF_SELECTED_FEATURES)
    k_best = selector.fit(X, y)
    feature_support = selector.get_support()

    if feature_support is None:
        raise Exception("No features selected")

    selected_features = []

    for check, feature in zip(feature_support, features):
        if check:
            selected_features.append(feature)

    SELECTED_FEATURES = selected_features
    print("Selected Features:")
    for feature in selected_features:
        print(feature)

classes = np.unique(y)
class_weights = dict(
    zip(
        classes,
        class_weight.compute_class_weight(
            class_weight="balanced", classes=classes, y=y
        ),
    )
)

# Model Training and Evaluation
models = [
    SVC(class_weight=class_weights),
    SGDClassifier(class_weight=class_weights),
    RandomForestClassifier(class_weight=class_weights),
    DecisionTreeClassifier(class_weight=class_weights),
    HistGradientBoostingClassifier(class_weight=class_weights),
]


x_train, x_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

for model in models:
    print(f"Training {model.__class__.__name__}...")
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)

    print("Classification Report:")
    print(classification_report(y_test, y_pred, zero_division=0))  # type: ignore
    print()

    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    print()

    print("*" * 80)
    print()

# Save the model
for model in models:
    with open(f"./Model/model_{model.__class__.__name__}.pkl", "wb") as f:
        pickle.dump(model, f)
