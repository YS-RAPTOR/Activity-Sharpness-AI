from typing import Literal, Tuple

import time
import random
import joblib
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sensor_data import SENSOR_DATA
import selected_features as selected_features


def get_model(path):
    with open(path, "rb") as f:
        model = joblib.load(f)
    return model


Activity_Model = get_model("./models/Models_Activity/model_best.pkl")
Kinfe_Sharpness_Model = get_model("./models/Models_Knife Sharpness/model_best.pkl")
STEPS_PER_SECOND = 10


class Sensor:
    def __init__(
        self,
        name: str,
        min_accel: float,
        max_accel: float,
        min_velocity: float,
        max_velocity: float,
    ):
        self.name = name
        self.last_update = time.time()

        self.min_accel = min_accel
        self.max_accel = max_accel

        self.min_velocity = min_velocity
        self.max_velocity = max_velocity

        self.velocity = random.uniform(min_velocity, max_velocity)
        self.acceleration = random.uniform(min_accel, max_accel)

    def step(self, current_time: float) -> dict[str, float]:
        duration = current_time - self.last_update
        num_steps = int(duration * STEPS_PER_SECOND)
        if num_steps < 1:
            return {}

        for _ in range(num_steps):
            self.update()

        self.last_update = current_time
        return {f"SV {self.name}": self.velocity, f"SA {self.name}": self.acceleration}

    def update(self):
        self.acceleration += (
            random.uniform(self.min_accel, self.max_accel) / STEPS_PER_SECOND
        )
        self.acceleration = max(self.min_accel, min(self.max_accel, self.acceleration))

        self.velocity += self.acceleration / STEPS_PER_SECOND
        self.velocity = max(self.min_velocity, min(self.max_velocity, self.velocity))


app = FastAPI()
origins = ["http://localhost:8001"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Worker:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
        self.sensors = [Sensor(name, *vals) for name, vals in SENSOR_DATA.items()]

    def get_data(self) -> dict[str, float]:
        current_time = time.time()
        data = {}
        for sensor in self.sensors:
            data.update(sensor.step(current_time))
        return data


workers = [Worker(1, "John"), Worker(2, "Jane"), Worker(3, "Doe")]


def predict_activity(
    data,
) -> Literal[
    "Cutting",
    "Idle",
    "Slicing",
    "Steeling",
    "Dropping",
    "Reaching",
    "Walking",
    "Dropping",
    "Placing/ Manipulating",
    "Pulling",
]:
    prediction = Activity_Model.predict(data)
    print(prediction)
    return prediction


def should_sharpen(data) -> bool:
    prediction = Kinfe_Sharpness_Model.predict(data)
    print(prediction)
    return prediction == "Blunt"


def get_filtered_data(
    data: dict[str, float],
) -> Tuple[dict[str, float], dict[str, float]]:
    sharpen_data = {}
    activity_data = {}

    for key, value in data.items():
        if key in selected_features.Kinfe_Sharpness:
            sharpen_data[key] = value
        if key in selected_features.Activity:
            activity_data[key] = value

    return sharpen_data, activity_data


@app.get("/workers")
def get_workers():
    results = []
    for worker in workers:
        data = worker.get_data()
        sharpen_data, activity_data = get_filtered_data(data)
        results.append(
            {
                "id": worker.id,
                "name": worker.name,
                "activity": predict_activity(sharpen_data),
                "should_sharpen": should_sharpen(activity_data),
            }
        )
    return results
