import pandas as pd
from pathlib import Path

DATA = "D:\\OneDrive - Swinburne University\\Year 4\\Artificial Intelligence for Engineering\\Project\\Data\\Processed\\data.csv"

df = pd.read_csv(DATA)
sensor_names = [f.replace("SA ", "") for f in df.columns if f.startswith("SA ")]

min_values = df.min()
max_values = df.max()

with open("sensor_data.py", "w") as f:
    f.write("SENSOR_DATA = {\n")

    for sensor in sensor_names:
        f.write(
            f'"    {sensor}": ({min_values[f"SA {sensor}"]},{max_values[f"SA {sensor}"]},{min_values[f"SV {sensor}"]},{max_values[f"SV {sensor}"]}),\n'
        )

    f.write("}\n")

