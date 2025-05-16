from typing import Dict, Tuple
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from data import DATA
from scipy.stats import linregress

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.set_option("display.width", 1000000000)

ANALYSIS = True
EDA = True

df = pd.read_csv(DATA)

target = "Activity"
ignore = ["Activity", "Worker", "Job", "Knife Sharpness", "Shift Number"]
features = [c for c in df.columns if c not in ignore]
features = [c for c in features if "SA " in c or "SV " in c]
print(features)

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
class_distribution = df[target].value_counts()
print("Class Distribution: ")
print(class_distribution, "\n\n")
if ANALYSIS:
    class_distribution.plot(kind="bar")

# Adjust class weights
class_weights = class_distribution.sum() / class_distribution
print(class_weights)

# Shuffled dataframe slice
df = df[features]
shuffled_df = df.sample(n=10000).reset_index(drop=True)

print(len(shuffled_df))

# EDA
already_done: Dict[Tuple[str, str], bool] = {}
count = 0
for f1 in features:
    for f2 in features:
        if f1 == f2:
            continue

        if (f1, f2) in already_done or (f2, f1) in already_done:
            continue

        already_done[(f1, f2)] = True
        title = "{f1} vs {f2}"

        try:
            x = shuffled_df[f1]
            y = shuffled_df[f2]
            slope, intercept, r_value, p_value, std_err = linregress(x, y)
            line = slope * x + intercept

            if abs(slope) < 0.75 and abs(slope) > 2:
                continue

            plt.figure(figsize=(10, 6))
            plt.scatter(x, y, label="Data Points")
            plt.plot(x, line, color="red", label=f"Fit Line (r={r_value:.2f})")
            plt.xlabel(f1)
            plt.ylabel(f2)
            plt.title(title.format(f1=f1, f2=f2))
            plt.tight_layout()
            plt.show()
            input("Press Enter to continue...")
        except Exception as e:
            continue

print("Total number of correlated plots: ", count)
print("Total number of plots: ", len(already_done))

print("Is Null: ")
print(df.isnull().sum(), "\n\n")

print("Is NaN: ")
print(df.isna().sum(), "\n\n")

print("Is Inf: ")
print(np.isinf(df).sum(), "\n\n")

print("Duplicates: ")
print(df.duplicated().sum(), "\n\n")
