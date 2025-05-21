from data import DATA
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

IS_HORIZONTAL = True

df = pd.read_csv(DATA)

Graphs = {
    "SV L5 x": ["SV L3 x", "SV T12 x"],
    "SV L5 y": ["SV L3 y", "SV T12 y"],
    "SV L5 z": ["SV L3 z", "SV T12 z", "SV Neck z"],
    "SV T8 x": ["SV Head x", "SV Right Shoulder x", "SV Left Shoulder x"],
    "SV T8 y": ["SV Head y", "SV Right Shoulder y", "SV Left Shoulder y"],
    "SV Head z": ["SV Right Shoulder z", "SV Left Shoulder z"],
    "SV Right Foot x": ["SV Right Toe x"],
    "SV Right Foot y": ["SV Right Toe y"],
    "SV Right Foot z": ["SV Right Toe z"],
    "SV Left Foot x": ["SV Left Toe x"],
    "SV Left Foot y": ["SV Left Toe y"],
    "SV Left Foot z": ["SV Left Toe z"],
    "SA Right Foot x": ["SA Right Toe x"],
    "SA Right Foot y": ["SA Right Toe y"],
    "SA Right Foot z": ["SA Right Toe z"],
    "SA Left Foot x": ["SA Left Toe x"],
    "SA Left Foot y": ["SA Left Toe y"],
    "SA Left Foot z": ["SA Left Toe z"],
    "SA L5 x": ["SA L3 x", "SA T12 x", "SA Neck x", "SA T8 x"],
    "SA L5 y": ["SA L3 y", "SA T12 y", "SA Neck y", "SA T8 y"],
    "SA L5 z": ["SA L3 z", "SA T12 z", "SA Neck z"],
}

path = Path("models/Data/EDA_Graphs")
if IS_HORIZONTAL:
    path /= "Horizontal"
else:
    path /= "Vertical"

path.mkdir(parents=True, exist_ok=True)

for y_feature, x_features in Graphs.items():
    if len(x_features) == 1:
        x_feature = x_features[0]
        fig, ax = plt.subplots(figsize=(10, 10))
        if IS_HORIZONTAL:
            x, y = df[x_feature], df[y_feature]

            slope, intercept, r_value, p_value, std_err = linregress(x, y)
            line = slope * x + intercept
            ax.plot(x, line, color="red", label=f"Fit Line (r={r_value:.2f})")

            ax.scatter(x, y, alpha=0.5)
            ax.set_xlabel(x_feature)
            ax.set_ylabel(y_feature)
        else:
            x, y = df[y_feature], df[x_feature]

            slope, intercept, r_value, p_value, std_err = linregress(x, y)
            line = slope * x + intercept
            ax.plot(x, line, color="red", label=f"Fit Line (r={r_value:.2f})")

            ax.scatter(x, y, alpha=0.5)
            ax.set_ylabel(x_feature)
            ax.set_xlabel(y_feature)
    else:
        if IS_HORIZONTAL:
            fig, axs = plt.subplots(
                1, len(x_features), figsize=(10 * len(x_features), 10)
            )
            axs = axs.flatten()
        else:
            fig, axs = plt.subplots(
                len(x_features), 1, figsize=(10, 10 * len(x_features))
            )
            axs = axs.flatten()

        for i, (ax, x_feature) in enumerate(zip(axs, x_features)):
            if IS_HORIZONTAL:
                x, y = df[x_feature], df[y_feature]

                slope, intercept, r_value, p_value, std_err = linregress(x, y)
                line = slope * x + intercept
                ax.plot(x, line, color="red", label=f"Fit Line (r={r_value:.2f})")

                ax.scatter(x, y, alpha=0.5)
                ax.set_xlabel(x_feature)
                if i == 0:
                    ax.set_ylabel(y_feature)
            else:
                x, y = df[y_feature], df[x_feature]

                slope, intercept, r_value, p_value, std_err = linregress(x, y)
                line = slope * x + intercept
                ax.plot(x, line, color="red", label=f"Fit Line (r={r_value:.2f})")

                ax.scatter(x, y, alpha=0.5)
                ax.set_ylabel(x_feature)
                if i == len(x_features) - 1:
                    ax.set_xlabel(y_feature)

    fig.suptitle(f"Correlations for {y_feature}")
    plt.tight_layout()
    plt.savefig(path / f"{y_feature}.png", bbox_inches="tight", transparent=True)
