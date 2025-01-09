import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .generate import generate_tests, PromptInput

logging.basicConfig(level=logging.INFO)

origins = ["*"]


class GenerateRequestBody(PromptInput):
    pass

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate")
async def generate(body: GenerateRequestBody):
    logging.info(body)
    resp = generate_tests(body)
    return { "data": resp }
