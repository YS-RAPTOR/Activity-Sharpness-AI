from fastapi import FastAPI
import time
import random
from sensor_data import SENSOR_DATA
from typing import Literal

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

    def step(self, current_time: float):
        duration = current_time - self.last_update
        num_steps = int(duration * STEPS_PER_SECOND)
        if num_steps < 1:
            return

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

class Worker:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
        self.sensors = [Sensor(name, *vals) for name, vals in SENSOR_DATA.items()]
        
    def get_data(self):
        current_time = time.time()
        data = {}
        for sensor in self.sensors:
            data.update(sensor.step(current_time))
        return data
    

workers = [Worker(1, "John"), Worker(2, "Jane"), Worker(3, "Doe")]

def predict_activity(data) -> Literal["Cutting","Idle","Slicing","Steeling","Dropping","Reaching","Walking","Dropping","Placing/ Manipulating","Pulling"]:
    # TODO: Implement the model
    return "Idle"

def should_sharpen(data) -> bool:
    # TODO: Implement the model
    return False

@app.get("/workers")
def get_workers():
    results = []
    for worker in workers:
        data = worker.get_data()
        results.append({"id": worker.id, "name": worker.name, "activity": predict_activity(data), "should_sharpen": should_sharpen(data)})
    return results