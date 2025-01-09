import logging

from fastapi import FastAPI

from .generate import generate_tests, PromptInput

logging.basicConfig(level=logging.INFO)

class GenerateRequestBody(PromptInput):
    pass

app = FastAPI()

@app.post("/generate")
async def generate(body: GenerateRequestBody):
    logging.info(body)
    resp = generate_tests(body)
    return { "data": resp }
