import pandas as pd
import os

# Define list of Excel file paths
file_paths_boning = [
    # P1 Boning files
    r'C:\Users\adenk\Downloads\Theme2\Theme2\P1\Boning\MVN-J-Boning-90-004.xlsx',
    r'C:\Users\adenk\Downloads\Theme2\Theme2\P1\Boning\MVN-J-Boning-90-003.xlsx',
    r'C:\Users\adenk\Downloads\Theme2\Theme2\P1\Boning\MVN-J-Boning-90-002.xlsx',
    r'C:\Users\adenk\Downloads\Theme2\Theme2\P1\Boning\MVN-J-Boning-90-001.xlsx',
    r'C:\Users\adenk\Downloads\Theme2\Theme2\P1\Boning\MVN-J-Boning-79-001.xlsx',
    r'C:\Users\adenk\Downloads\Theme2\Theme2\P1\Boning\MVN-J-Boning-64-005.xlsx',
    r'C:\Users\adenk\Downloads\Theme2\Theme2\P1\Boning\MVN-J-Boning-64-006.xlsx',
    r'C:\Users\adenk\Downloads\Theme2\Theme2\P1\Boning\MVN-J-Boning-64-002.xlsx',
    r'C:\Users\adenk\Downloads\Theme2\Theme2\P1\Boning\MVN-J-Boning-64-003.xlsx',
    r'C:\Users\adenk\Downloads\Theme2\Theme2\P1\Boning\MVN-J-Boning-64-004.xlsx',
    r'C:\Users\adenk\Downloads\Theme2\Theme2\P1\Boning\MVN-J-Boning-64-001.xlsx',
    # P2 Boning files
    r'C:\Users\adenk\Downloads\Theme2\Theme2\P2\Boning\MVN-S-Boning-89-003.xlsx',
    r'C:\Users\adenk\Downloads\Theme2\Theme2\P2\Boning\MVN-S-Boning-89-004.xlsx',
    r'C:\Users\adenk\Downloads\Theme2\Theme2\P2\Boning\MVN-S-Boning-89-001.xlsx',
    r'C:\Users\adenk\Downloads\Theme2\Theme2\P2\Boning\MVN-S-Boning-89-002.xlsx',
    r'C:\Users\adenk\Downloads\Theme2\Theme2\P2\Boning\MVN-S-Boning-76-002.xlsx',
    r'C:\Users\adenk\Downloads\Theme2\Theme2\P2\Boning\MVN-S-Boning-76-001.xlsx',
    r'C:\Users\adenk\Downloads\Theme2\Theme2\P2\Boning\MVN-S-Boning-63-003.xlsx',
    r'C:\Users\adenk\Downloads\Theme2\Theme2\P2\Boning\MVN-S-Boning-63-002.xlsx',
    r'C:\Users\adenk\Downloads\Theme2\Theme2\P2\Boning\MVN-S-Boning-63-001.xlsx',
]

file_paths_slicing = [
    # P1 Slicing files
    r'C:\Users\adenk\Downloads\Theme2\Theme2\P1\Slicing\MVN-J-Slicing-87-001.xlsx',
    r'C:\Users\adenk\Downloads\Theme2\Theme2\P1\Slicing\MVN-J-Slicing-73-001.xlsx',
    r'C:\Users\adenk\Downloads\Theme2\Theme2\P1\Slicing\MVN-J-Slicing-64-001.xlsx',
    # P2 Slicing files
    r'C:\Users\adenk\Downloads\Theme2\Theme2\P2\Slicing\MVN-S-Slicing-87-001.xlsx',
    r'C:\Users\adenk\Downloads\Theme2\Theme2\P2\Slicing\MVN-S-Slicing-73-001.xlsx',
    r'C:\Users\adenk\Downloads\Theme2\Theme2\P2\Slicing\MVN-S-Slicing-63-001.xlsx',
]

# Combine and save Boning files
orientation_dfs = []
position_dfs = []
velocity_dfs = []
acceleration_dfs = []
angular_velocity_dfs = []
angular_acceleration_dfs = []

# Loop through each Boning file and load specific sheets
for path in file_paths_boning:
    try:
        orientation_dfs.append(pd.read_excel(path, sheet_name="Segment Orientation - Euler"))
        position_dfs.append(pd.read_excel(path, sheet_name="Segment Position"))
        velocity_dfs.append(pd.read_excel(path, sheet_name="Segment Velocity"))
        acceleration_dfs.append(pd.read_excel(path, sheet_name="Segment Acceleration"))
        angular_velocity_dfs.append(pd.read_excel(path, sheet_name="Segment Angular Velocity"))
        angular_acceleration_dfs.append(pd.read_excel(path, sheet_name="Segment Angular Acceleration"))
    except Exception as e:
        print(f"Error reading from {path}: {e}")

# Combine each type of sheet into a single dataframe for Boning
df_orientation_boning = pd.concat(orientation_dfs, ignore_index=True)
df_position_boning = pd.concat(position_dfs, ignore_index=True)
df_velocity_boning = pd.concat(velocity_dfs, ignore_index=True)
df_acceleration_boning = pd.concat(acceleration_dfs, ignore_index=True)
df_angular_velocity_boning = pd.concat(angular_velocity_dfs, ignore_index=True)
df_angular_acceleration_boning = pd.concat(angular_acceleration_dfs, ignore_index=True)

# Save Boning dataframes to Excel
output_dir = r'C:\Users\adenk\OneDrive\Documents\COS40007\Design Project\Combined Data'
df_orientation_boning.to_excel(os.path.join(output_dir, 'Boning-Segment-Orientation.xlsx'), index=False)
df_position_boning.to_excel(os.path.join(output_dir, 'Boning-Segment-Position.xlsx'), index=False)
df_velocity_boning.to_excel(os.path.join(output_dir, 'Boning-Segment-Velocity.xlsx'), index=False)
df_acceleration_boning.to_excel(os.path.join(output_dir, 'Boning-Segment-Acceleration.xlsx'), index=False)
df_angular_velocity_boning.to_excel(os.path.join(output_dir, 'Boning-Segment-Angular-Velocity.xlsx'), index=False)
df_angular_acceleration_boning.to_excel(os.path.join(output_dir, 'Boning-Segment-Angular-Acceleration.xlsx'), index=False)

# Combine and save Slicing files
orientation_dfs = []
position_dfs = []
velocity_dfs = []
acceleration_dfs = []
angular_velocity_dfs = []
angular_acceleration_dfs = []

# Loop through each Slicing file and load specific sheets
for path in file_paths_slicing:
    try:
        orientation_dfs.append(pd.read_excel(path, sheet_name="Segment Orientation - Euler"))
        position_dfs.append(pd.read_excel(path, sheet_name="Segment Position"))
        velocity_dfs.append(pd.read_excel(path, sheet_name="Segment Velocity"))
        acceleration_dfs.append(pd.read_excel(path, sheet_name="Segment Acceleration"))
        angular_velocity_dfs.append(pd.read_excel(path, sheet_name="Segment Angular Velocity"))
        angular_acceleration_dfs.append(pd.read_excel(path, sheet_name="Segment Angular Acceleration"))
    except Exception as e:
        print(f"Error reading from {path}: {e}")

# Combine each type of sheet into a single dataframe for Slicing
df_orientation_slicing = pd.concat(orientation_dfs, ignore_index=True)
df_position_slicing = pd.concat(position_dfs, ignore_index=True)
df_velocity_slicing = pd.concat(velocity_dfs, ignore_index=True)
df_acceleration_slicing = pd.concat(acceleration_dfs, ignore_index=True)
df_angular_velocity_slicing = pd.concat(angular_velocity_dfs, ignore_index=True)
df_angular_acceleration_slicing = pd.concat(angular_acceleration_dfs, ignore_index=True)

# Save Slicing dataframes to Excel
df_orientation_slicing.to_excel(os.path.join(output_dir, 'Slicing-Segment-Orientation.xlsx'), index=False)
df_position_slicing.to_excel(os.path.join(output_dir, 'Slicing-Segment-Position.xlsx'), index=False)
df_velocity_slicing.to_excel(os.path.join(output_dir, 'Slicing-Segment-Velocity.xlsx'), index=False)
df_acceleration_slicing.to_excel(os.path.join(output_dir, 'Slicing-Segment-Acceleration.xlsx'), index=False)
df_angular_velocity_slicing.to_excel(os.path.join(output_dir, 'Slicing-Segment-Angular-Velocity.xlsx'), index=False)
df_angular_acceleration_slicing.to_excel(os.path.join(output_dir, 'Slicing-Segment-Angular-Acceleration.xlsx'), index=False)