import logging

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

from .generate import (
    generate_tests,
    PromptInput,
    generate_tests_v2,
    PromptInputWithImport,
)

logging.basicConfig(level=logging.INFO)

origins = ["*"]


class GenerateRequestBody(PromptInput):
    pass


class GenerateRequestBodyV2(PromptInputWithImport):
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
    return {"data": resp}


@app.post("/generate/v2")
async def generate_v2(body: GenerateRequestBodyV2):
    logging.info(body)
    return StreamingResponse(generate_tests_v2(body), media_type="text/plain")
