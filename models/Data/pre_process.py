from data import PREPROCESS_DATA_DIR, PROCESSED_DATA_DIR
import pandas as pd
from pathlib import Path

data_path = Path(PREPROCESS_DATA_DIR)
sheets = {
    "Segment Orientation - Euler": "SO",
    "Segment Position": "SP",
    "Segment Velocity": "SV",
    "Segment Acceleration": "SA",
    "Segment Angular Velocity": "SAV",
    "Segment Angular Acceleration": "SAA",
}

activity = {
    "Boning": [
        "Idle",
        "Walking",
        "Steeling",
        "Reaching",
        "Cutting",
        "Dropping ",
    ],
    "Slicing": [
        "Idle",
        "Walking",
        "Steeling",
        "Reaching",
        "Cutting",
        "Slicing",
        "Pulling",
        "Placing/ Manipulating",
        "Dropping",
    ],
}

final_df = pd.DataFrame()


def read_data(
    file: Path,
    worker: str,
    job: str,
    knife_sharpness: str,
    shift_number: str,
):
    sharpness = "Blunt"
    if int(knife_sharpness) >= 85:
        sharpness = "Sharp"
    elif int(knife_sharpness) >= 70:
        sharpness = "Medium"

    creation = pd.DataFrame()
    for i, (sheet, front) in enumerate(sheets.items()):
        print(f"Reading {sheet} from {file}")
        df = pd.read_excel(file, sheet_name=sheet)

        if "Marker" in df.columns:
            label = "Marker"
        elif "Label" in df.columns:
            label = "Label"

        if i == 0:
            creation["Activity"] = df[label].apply(lambda x: activity[job][int(x)])  # type: ignore
            creation["Worker"] = worker
            creation["Job"] = job
            creation["Knife Sharpness"] = sharpness
            creation["Shift Number"] = shift_number

        headers = [h for h in df.columns if h not in ["Frame", label]]  # type: ignore
        print(headers)
        for header in headers:
            creation[f"{front} {header}"] = df[header]
    global final_df
    final_df = pd.concat([final_df, creation], ignore_index=True)


for worker_path in data_path.iterdir():
    if not worker_path.is_dir():
        continue

    worker = worker_path.name

    for job_path in worker_path.iterdir():
        if not job_path.is_dir():
            continue

        job = job_path.name

        for file in job_path.iterdir():
            if not file.is_file():
                continue

            _, _, _, knife_sharpness, shift_number = file.name.split("-")
            shift_number = shift_number.split(".")[0]
            read_data(file, worker, job, knife_sharpness, shift_number)


write_dir = Path(PROCESSED_DATA_DIR)
write_dir.mkdir(parents=True, exist_ok=True)

final_df.to_csv(write_dir / "data.csv", index=False)
