import optuna
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split
import numpy as np
from common import load_dataset
from data import DATA
from sklearn.utils import class_weight
import os


# Load dataset (replace with your own if needed)
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
X, y = load_dataset(DATA, "Activity", SELECTED_FEATURES)

# Split into train/test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

classes = np.unique(y)
class_weights = dict(
    zip(
        classes,
        class_weight.compute_class_weight(
            class_weight="balanced", classes=classes, y=y
        ),
    )
)


# Objective function for Optuna
def objective(trial):
    params = {
        "n_estimators": trial.suggest_int("n_estimators", 50, 500),
        "max_depth": trial.suggest_categorical(
            "max_depth", [None] + list(range(2, 33))
        ),
        "min_samples_split": trial.suggest_int("min_samples_split", 2, 20),
        "min_samples_leaf": trial.suggest_int("min_samples_leaf", 1, 20),
        "max_features": trial.suggest_categorical(
            "max_features", ["sqrt", "log2", None]
        ),
        "bootstrap": trial.suggest_categorical("bootstrap", [True, False]),
        "class_weight": class_weights,
    }

    model = RandomForestClassifier(**params, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    score = f1_score(y_test, y_pred, average="macro")
    print(f"{trial} Finished")
    return score


# Create Optuna study
storage_name = "sqlite:///optuna_random_forest_study_activity.db"
study_name = "rf_activity_study"

study = optuna.create_study(
    study_name=study_name,
    direction="maximize",
    storage=storage_name,
    load_if_exists=True,
)
study.optimize(objective, n_trials=100)

# Output the best parameters and retrain
print("Best trial:")
print(f"  Value: {study.best_trial.value:.4f}")
print("  Params:")
for key, value in study.best_trial.params.items():
    print(f"    {key}: {value}")

# Retrain with best params on the full training data
best_model = RandomForestClassifier(
    **study.best_trial.params, random_state=42, n_jobs=-1
)
best_model.fit(X_train, y_train)
test_acc = accuracy_score(y_test, best_model.predict(X_test))
print(f"\nTest Accuracy: {test_acc:.4f}")
