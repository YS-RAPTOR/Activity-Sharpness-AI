import time
from data import DATA
from common import load_dataset
import numpy as np
from sklearn.feature_selection import SelectKBest
from sklearn.utils import class_weight
from sklearn.metrics import f1_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

X, y = load_dataset(DATA, "Activity", None)

classes = np.unique(y)
class_weights = dict(
    zip(
        classes,
        class_weight.compute_class_weight(
            class_weight="balanced", classes=classes, y=y
        ),
    )
)

best_score = 0
best_no_of_selections = 0
best_features = []

x_train, x_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

for no_of_selections in range(15, 18):
    start_time = time.time()
    print(f"Testing number of selections: {no_of_selections}")

    selector = SelectKBest(k=no_of_selections)
    k_best = selector.fit(X, y)
    feature_support = selector.get_support()

    if feature_support is None:
        raise Exception("No features selected")

    selected_features = []

    for check, feature in zip(feature_support, X.columns):
        if check:
            selected_features.append(feature)

    model = RandomForestClassifier(class_weight=class_weights, n_jobs=-1)
    model.fit(x_train[selected_features], y_train)
    y_pred = model.predict(x_test[selected_features])
    score = f1_score(y_test, y_pred, average="macro")

    if score > best_score:
        best_score = score
        best_no_of_selections = no_of_selections
        best_features = selected_features

    print(f"Score: {score:.4f}")
    print(f"Time taken: {time.time() - start_time:.2f} seconds\n")

print(f"Best number of selections: {best_no_of_selections}")
print(f"Best score: {best_score:.4f}")
print("Best features:")

for feature in best_features:
    print(f'"{feature}",')
