from .prompt import PromptInput, PromptInputWithImport, PromptInputWithSampleTest


class GenerateRequestBody(PromptInput):
    pass


class GenerateRequestBodyV2(PromptInputWithImport):
    pass


class GenerateRequestBodyV3(PromptInputWithSampleTest):
    pass
