import pandas as pd
import json
import os

# File Paths
csv_file = '/Users/adamhorvath/Downloads/data.csv'  # Update path if needed
output_dir = '/Users/adamhorvath/Downloads/worker_bodyparts'  # Output directory
os.makedirs(output_dir, exist_ok=True)

# Configuration
omit_columns = ['Activity', 'Worker', 'Job', 'Knife Sharpness']
segment_prefixes = {
    "Segment Orientation - Euler": "SO",
    "Segment Position": "SP",
    "Segment Velocity": "SV",
    "Segment Acceleration": "SA",
    "Segment Angular Velocity": "SAV",
    "Segment Angular Acceleration": "SAA"
}
prefix_to_label = {v: k for k, v in segment_prefixes.items()}

# Load Data
df = pd.read_csv(csv_file)
workers = df['Worker'].dropna().unique()

# Drop metadata columns for logic
metric_df = df.drop(columns=[col for col in omit_columns if col in df.columns])

# Group Columns by Body Part and Segment Type (with x/y/z)
grouped = {}

for col in metric_df.columns:
    for prefix in segment_prefixes.values():
        if col.startswith(prefix):
            suffix = col[len(prefix):].strip()

            if not suffix.lower().endswith((' x', ' y', ' z')):
                continue

            body_part = suffix[:-2].strip()  # remove axis
            axis = suffix[-1].lower()

            # Skip malformed names like "A Head", "V Head"
            if body_part.startswith(('A ', 'V ')):
                continue

            grouped.setdefault(body_part, {}).setdefault(prefix, {})[axis] = col
            break

# Process Each Worker & Save JSON per Body Part
for worker in workers:
    worker_df = df[df['Worker'] == worker]

    for body_part, segment_data in grouped.items():
        body_json = {
            "worker": worker,
            "body_part": body_part,
            "segments": {}
        }

        has_data = False

        for prefix, axes in segment_data.items():
            segment_entry = {
                "label": prefix_to_label.get(prefix, prefix),
                "type": "vector3",
                "components": {}
            }

            segment_valid = False

            for axis in ['x', 'y', 'z']:
                col_name = axes.get(axis)
                if not col_name or col_name not in worker_df.columns:
                    continue

                col_data = worker_df[col_name].dropna()
                if col_data.empty:
                    continue

                segment_valid = True
                segment_entry["components"][axis] = {
                    "min": float(col_data.min()),
                    "max": float(col_data.max())
                }

            if segment_valid:
                body_json["segments"][prefix] = segment_entry
                has_data = True

        if has_data:
            filename = f"{worker}_{body_part.replace(' ', '_')}.json"
            output_path = os.path.join(output_dir, filename)
            with open(output_path, 'w') as f:
                json.dump(body_json, f, indent=2)
            print(f"Saved: {output_path}")
