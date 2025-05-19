import pickle
import time
import numpy as np
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.feature_selection import SelectKBest
from sklearn.linear_model import SGDClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import train_test_split
from sklearn.utils import class_weight
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
NUMBER_OF_SELECTED_FEATURES = 30

X, y = load_dataset(DATA, target, selected_features=SELECTED_FEATURES)

# Feature Selection
if SELECTED_FEATURES is None:
    selector = SelectKBest(k=NUMBER_OF_SELECTED_FEATURES)
    k_best = selector.fit(X, y)
    feature_support = selector.get_support()

    if feature_support is None:
        raise Exception("No features selected")

    selected_features = []

    for check, feature in zip(feature_support, X.columns):
        if check:
            selected_features.append(feature)

    SELECTED_FEATURES = selected_features
    features = selected_features
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

hist_classes = np.unique(y.cat.codes)
hist_class_weights = dict(
    zip(
        hist_classes,
        class_weight.compute_class_weight(
            class_weight="balanced", classes=hist_classes, y=y.cat.codes
        ),
    )
)

# Model Training and Evaluation
models = [
    DecisionTreeClassifier(class_weight=class_weights),
    HistGradientBoostingClassifier(class_weight=hist_class_weights),
    SGDClassifier(class_weight=class_weights, n_jobs=-1),
    RandomForestClassifier(class_weight=class_weights, n_jobs=-1),
]


x_train, x_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

for model in models:
    if model.__class__.__name__ == "HistGradientBoostingClassifier":
        y_tr = y_train.cat.codes
        y_te = y_test.cat.codes
    else:
        y_tr = y_train
        y_te = y_test

    start_time = time.time()
    print(f"Training {model.__class__.__name__}...")
    model.fit(x_train, y_tr)
    y_pred = model.predict(x_test)

    print("Classification Report:")
    print(classification_report(y_te, y_pred, zero_division=0))  # type: ignore
    print()

    print("Confusion Matrix:")
    print(confusion_matrix(y_te, y_pred))
    print()

    # Save the model
    with open(
        f"./models/Models_{target}/model_{model.__class__.__name__}.pkl", "wb"
    ) as f:
        pickle.dump(model, f)

    print(f"Model {model.__class__.__name__} saved.")
    print(f"Time taken: {time.time() - start_time:.2f} seconds")
    print()
    print("*" * 80)
