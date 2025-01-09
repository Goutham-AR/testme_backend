import logging

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

from .generate import generate_tests, PromptInput
from .generate_streaming import generate_tests_streaming

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

@app.post("/generate_streaming")
async def generate_streaming(body: GenerateRequestBody):
    logging.info(body)
    return StreamingResponse(generate_tests_streaming(body), media_type="text/plain")
