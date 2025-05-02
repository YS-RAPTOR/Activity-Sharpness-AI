from fastapi import FastAPI

app = FastAPI()


class Worker:
    def __init__(self, id: int, name: str):
        self.id = 0
        self.name = name


workers = [Worker(1, "John"), Worker(2, "Jane"), Worker(3, "Doe")]


@app.get("/workers")
def get_workers():
    return workers


@app.get("/worker/{worker_id}")
def get_worker(worker_id: int):
    for worker in workers:
        if worker.id == worker_id:
            return {"activity": "", "should_sharpen": False}
    return None
