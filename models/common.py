import pandas as pd

DROP_LIST = [
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


def load_dataset(path, target, selected_features=None):
    df = pd.read_csv(path)
    # NOTE: Change if you want to train on another target

    # Print data type of each column
    for drop in DROP_LIST:
        if drop == target:
            continue
        df.drop(columns=drop, inplace=True)

    features = (
        [i for i in df.columns if i != target]
        if selected_features is None
        else selected_features
    )
    features = [f for f in features if "SA " in f or "SV " in f]

    X, y = df[features], df[target].astype("category")
    return X, y
