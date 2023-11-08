from typing import Dict
from fastapi import FastAPI

app = FastAPI()

_API_VERSION = "1.0.0"
_API_NAME = "dummy"


@app.get(f"/{_API_VERSION}/{_API_NAME}")
def dummy_api() -> Dict:
    return {}


@app.get("/health")
def health_api() -> Dict:
    return {}
