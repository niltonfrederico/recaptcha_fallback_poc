from environs import Env
from fastapi import FastAPI, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
import requests

# Environment Variables
env = Env()
env.read_env()
# App
app = FastAPI(title="Recaptcha POC")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoints
@app.get("/hello")
def hello(request: Request, response: Response):
    recaptcha_request = requests.post(
        "https://www.google.com/recaptcha/api/siteverify",
        data={
            "secret": env.str("RECAPTCHA_V2_SECRET")
            if request.headers.get("recaptcha_version") == "v2"
            else env.str("RECAPTCHA_V3_SECRET"),
            "response": request.headers.get("recaptcha"),
        },
    )

    score = 1.0
    rr_json = recaptcha_request.json()

    if rr_json.get("success"):
        if rr_json.get("score") and rr_json.get("score") < score:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return ({"error": "score", "data": rr_json},)

    return {"hello": "world"}
