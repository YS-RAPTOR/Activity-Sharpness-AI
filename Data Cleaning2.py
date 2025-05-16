import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from concurrent.futures import ProcessPoolExecutor, as_completed
import os

# File paths for all datasets
df_boning_orientation = pd.read_excel(r'C:\Users\adenk\OneDrive\Documents\COS40007\Design Project\Combined Data\Boning-Segment-Orientation.xlsx')
df_boning_position = pd.read_excel(r'C:\Users\adenk\OneDrive\Documents\COS40007\Design Project\Combined Data\Boning-Segment-Position.xlsx')
df_boning_velocity = pd.read_excel(r'C:\Users\adenk\OneDrive\Documents\COS40007\Design Project\Combined Data\Boning-Segment-Velocity.xlsx')
df_boning_acceleration = pd.read_excel(r'C:\Users\adenk\OneDrive\Documents\COS40007\Design Project\Combined Data\Boning-Segment-Acceleration.xlsx')
df_boning_angular_velocity = pd.read_excel(r'C:\Users\adenk\OneDrive\Documents\COS40007\Design Project\Combined Data\Boning-Segment-Angular-Velocity.xlsx')
df_boning_angular_acceleration = pd.read_excel(r'C:\Users\adenk\OneDrive\Documents\COS40007\Design Project\Combined Data\Boning-Segment-Angular-Acceleration.xlsx')

df_slicing_orientation = pd.read_excel(r'C:\Users\adenk\OneDrive\Documents\COS40007\Design Project\Combined Data\Slicing-Segment-Orientation.xlsx')
df_slicing_position = pd.read_excel(r'C:\Users\adenk\OneDrive\Documents\COS40007\Design Project\Combined Data\Slicing-Segment-Position.xlsx')
df_slicing_velocity = pd.read_excel(r'C:\Users\adenk\OneDrive\Documents\COS40007\Design Project\Combined Data\Slicing-Segment-Velocity.xlsx')
df_slicing_acceleration = pd.read_excel(r'C:\Users\adenk\OneDrive\Documents\COS40007\Design Project\Combined Data\Slicing-Segment-Acceleration.xlsx')
df_slicing_angular_velocity = pd.read_excel(r'C:\Users\adenk\OneDrive\Documents\COS40007\Design Project\Combined Data\Slicing-Segment-Angular-Velocity.xlsx')
df_slicing_angular_acceleration = pd.read_excel(r'C:\Users\adenk\OneDrive\Documents\COS40007\Design Project\Combined Data\Slicing-Segment-Angular-Acceleration.xlsx')

all_data = [df_boning_orientation, df_boning_position, df_boning_velocity, df_boning_acceleration, df_boning_angular_velocity, df_boning_angular_acceleration,
            df_slicing_orientation, df_slicing_position, df_slicing_velocity, df_slicing_acceleration, df_slicing_angular_velocity, df_slicing_angular_acceleration]

# Function to process a single dataset
def process_dataset(df):
    # Drop duplicate rows
    df.drop_duplicates(inplace=True)

    # Remove outliers using IQR method
    Q1 = df.quantile(0.25)
    Q3 = df.quantile(0.75)
    IQR = Q3 - Q1

    upper_whisker = Q3 + 1.5 * IQR
    lower_whisker = Q1 - 1.5 * IQR

    # Exclude "Frame" and "Label" columns
    data_col = [col for col in df.columns if col not in ["Frame", "Label"]]

    # Replace outliers
    for col in data_col:
        df[col] = np.where(df[col] > upper_whisker[col], upper_whisker[col], df[col])
        df[col] = np.where(df[col] < lower_whisker[col], lower_whisker[col], df[col])

    # Normalize data
    df_numeric = df.drop(columns=["Frame", "Label"], errors="ignore")
    scaler = MinMaxScaler()
    normalized_numeric = pd.DataFrame(scaler.fit_transform(df_numeric), columns=df_numeric.columns)

    # Add back Frame and Label columns
    if "Frame" in df.columns:
        normalized_numeric["Frame"] = df["Frame"]
    if "Label" in df.columns:
        normalized_numeric["Label"] = df["Label"]

    return normalized_numeric

# Use ProcessPoolExecutor to process datasets in parallel
if __name__ == "__main__":
    processed_data = []
    with ProcessPoolExecutor() as executor:
        futures = {executor.submit(process_dataset, df): idx for idx, df in enumerate(all_data)}
        for future in as_completed(futures):
            idx = futures[future]
            try:
                processed_data.append(future.result())
                print(f"Dataset {idx + 1} processed successfully.")
            except Exception as e:
                print(f"Error processing dataset {idx + 1}: {e}")

    # Save the cleaned data to a single Excel file with multiple sheets
    names = ["Boning-Orientation", "Boning-Position", "Boning-Velocity", "Boning-Acceleration",
             "Boning-Angular-Velocity", "Boning-Angular-Acceleration", "Slicing-Orientation", "Slicing-Position",
             "Slicing-Velocity", "Slicing-Acceleration", "Slicing-Angular-Velocity", "Slicing-Angular-Acceleration"]

    # Save each dataset as a CSV file
    output_dir = r'C:\Users\adenk\OneDrive\Documents\COS40007\Design Project\Combined Data'
    for df, name in zip(processed_data, names):
        csv_path = os.path.join(output_dir, f"{name}.csv")
        df.to_csv(csv_path, index=False)
        print(f"Saved {name} to {csv_path}")
