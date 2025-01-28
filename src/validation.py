from pydantic import BaseModel

from .prompt import (
    PromptInput,
    PromptInputWithImport,
    PromptInputWithSampleTest,
    Prompt,
)


class GenerateRequestBody(PromptInput):
    pass


class GenerateRequestBodyV2(PromptInputWithImport):
    pass


class GenerateRequestBodyV3(PromptInputWithSampleTest):
    pass


class PromptRequestBody(BaseModel):
    prompts: list[Prompt]
