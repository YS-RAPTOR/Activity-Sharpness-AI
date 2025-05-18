from typing import Dict, Tuple
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from data import DATA
from scipy.stats import linregress
import math

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.set_option("display.width", 1000000000)

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
]

ANALYSIS = True
EDA = False

df = pd.read_csv(DATA)

target = "Activity"
ignore = ["Activity", "Worker", "Job", "Knife Sharpness", "Shift Number"]
features = [c for c in df.columns if c not in ignore]
features = [c for c in features if "SA " in c or "SV " in c]

for feature in drop_list:
    df.drop(columns=feature, inplace=True)
    features.remove(feature)

# Check if there are any features that can be converted to a categorical type
# Check if there are features that are constants
count_threshold = 100
if ANALYSIS:
    for feature in features:
        values_counts = df[feature].value_counts()

        if len(values_counts) < count_threshold:
            print(f"Feature: {feature} Value Counts")
            print(df[feature].value_counts())
            print("")

# Class Distribution

if ANALYSIS:
    class_distribution = df[target].value_counts()
    class_distribution.plot(kind="bar")
    class_weights = class_distribution.sum() / class_distribution
    print("Class Weights: \n\n", class_weights)

df = df[features]
# EDA
if EDA:
    shuffled_df = df.sample(n=10000).reset_index(drop=True)
    already_done: Dict[Tuple[str, str], bool] = {}
    count = 0
    corr = df.corr()
    no_of_subplots = 4

    axs = None
    fig = None

    for f1 in features:
        for f2 in features:
            if f1 == f2:
                continue

            if (f1, f2) in already_done or (f2, f1) in already_done:
                continue

            already_done[(f1, f2)] = True

            try:
                x = shuffled_df[f1]
                y = shuffled_df[f2]

                correlation = corr[f1][f2]

                if abs(correlation) < 0.80 or math.isnan(correlation):
                    continue

                if axs is None or fig is None:
                    fig, axs = plt.subplots(
                        no_of_subplots, no_of_subplots, figsize=(20, 10)
                    )
                    axs = axs.flatten()

                slope, intercept, r_value, p_value, std_err = linregress(x, y)
                line = slope * x + intercept

                ax = axs[count % (no_of_subplots * no_of_subplots)]
                ax.scatter(x, y, label="Data Points")
                ax.plot(x, line, color="red", label=f"Fit Line (r={r_value:.2f})")

                ax.set_xlabel(f1)
                ax.set_ylabel(f2)
                ax.set_title(f"{f1} vs {f2}: {correlation:.2f}")

                count += 1

                if (count) % (no_of_subplots * no_of_subplots) == 0:
                    plt.tight_layout()
                    plt.show()
                    fig = None
                    axs = None

            except Exception:
                continue

    if fig is not None:
        plt.tight_layout()
        plt.show()

if ANALYSIS:
    print("Is Null: ")
    print(df.isnull().sum(), "\n\n")

    print("Is NaN: ")
    print(df.isna().sum(), "\n\n")

    print("Is Inf: ")
    print(np.isinf(df).sum(), "\n\n")

    print("Duplicates: ")
    print(df.duplicated().sum(), "\n\n")
