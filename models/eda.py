import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from data import DATA

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.set_option("display.width", 1000000000)

ANALYSIS = True
EDA = False

df = pd.read_csv(DATA)

target = "Activity"
ignore = ["Activity", "Worker", "Job", "Knife Sharpness", "Shift Number"]
features = [c for c in df.columns if c not in ignore]

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
shuffled_df = df.sample(n=500).reset_index(drop=True)

print(len(shuffled_df))

# EDA
if ANALYSIS and EDA:
    sns.pairplot(shuffled_df, diag_kind="kde", corner=True)

if ANALYSIS and EDA:
    sns.pairplot(shuffled_df, kind="reg", corner=True)

if ANALYSIS and EDA:
    corr = round(abs(df.corr()), 2)  # correlation matrix
    lower_triangle = np.tril(
        corr, k=-1
    )  # select only the lower triangle of the correlation matrix
    mask = lower_triangle == 0  # to mask the upper triangle in the following heatmap

    print("Correlation Matrix: ")
    print(corr, "\n\n")

    sns.heatmap(
        lower_triangle,
        center=0.5,
        cmap="coolwarm",
        annot=True,
        xticklabels=corr.index,  # type: ignore
        yticklabels=corr.columns,  # type: ignore
        cbar=True,
        linewidths=1,
        mask=mask,
    )  # Da Heatmap

if ANALYSIS and EDA:
    plt.show()

print("Is Null: ")
print(df.isnull().sum(), "\n\n")

print("Is NaN: ")
print(df.isna().sum(), "\n\n")

print("Is Inf: ")
print(np.isinf(df).sum(), "\n\n")

print("Duplicates: ")
print(df.duplicated().sum(), "\n\n")
