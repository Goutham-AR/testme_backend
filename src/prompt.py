from pydantic import BaseModel


class Prompt(BaseModel):
    role: str
    content: str


class PromptInput(BaseModel):
    filename: str
    code: str
    extension: str
    testFramework: str


class Import(BaseModel):
    path: str
    code: str


class PromptInputWithImport(PromptInput):
    framework: str
    imports: list[Import]
    packagejson: str


class PromptInputWithSampleTest(PromptInputWithImport):
    sampleTest: str


def _get_imports_prompt(imports_list: list[Import]):
    imports = ""
    for imp in imports_list:
        imports += f"""
            path: {imp.path}
            content: {imp.code},
        """
    return imports


def generate_prompt(input: PromptInput):
    prompt = f"""
        Generate unit test for the below given code assuming ${input.testFramework} library is installed. Cover all edge cases and generate only output code as text, no need of any prefix suffix or any extra note. If you want to include some notes, include it as comments in the generated code. Some informations about the code is given after the code.
        code: {input.code}
        file extension: {input.extension}
    """
    return prompt


def generate_prompt_with_imports(input: PromptInputWithImport):
    imports = _get_imports_prompt(input.imports)
    prompt = f"""
        Generate unit test for the below code assuming {input.testFramework} library is installed. The code uses a framework called {input.framework}. Cover all edge cases and generate only output code, no need of any prefix, suffix or any extra notes. If you want to include some notes, include it as comments in the generated code. The extension of the code file is {input.extension}. The code is given between '<code>'. The content of local imports in the given code is given alongside its path after the code segment. Each imports are separated by ','. Also add appropriate imports at the top of the result.
        <code>
        {input.code}
        <code>
        <imports>
            {imports}
        <imports>
    """
    return prompt


def generate_prompt_with_sample_test(input: PromptInputWithSampleTest):
    imports = _get_imports_prompt(input.imports)
    prompt = f"""
        Generate unit test for the below code assuming {input.testFramework} library is installed. The code uses a framework called {input.framework}. Cover all edge cases and generate only output code, no need of any prefix, suffix or any extra notes. If you want to include some notes, include it as comments in the generated code. The extension of the code file is {input.extension}. The code is given between '<code>'. The content of local imports in the given code is given alongside its path after the code segment. Each imports are separated by ','. Also add appropriate imports at the top of the result. A sample test file content is given between '<sample>'.
        <code>
        {input.code}
        <code>
        <imports>
            {imports}
        <imports>
        <sample>
            {input.sampleTest}
        <sample>
    """
    return prompt


def generate_new_prompt(input: PromptInputWithImport):
    imports = _get_imports_prompt(input.imports)
    prompt = f"""
## Overview
You are a code assistant that accepts a {input.extension} source file. Your goal is to generate comprehensive unit tests in order to increase the code coverage against the source file.

Additional guidelines:
- Carefully analyze the provided code. Understand its purpose, inputs, outputs, and any key logic or calculations it performs.
- Brainstorm a list of diverse and meaningful test cases you think will be necessary to fully validate the correctness and functionality of the code, and achieve 100% code coverage.
- After each individual test has been added, review all tests to ensure they cover the full range of scenarios, including how to handle exceptions or errors.

## Source File
Here is the source file that you will be writing tests against, called `{input.filename}`.
=========
{input.code}
=========

## Imported Files
Below are the contents of the files imported by the main source file.
{imports}

## Project information file (package.json)
Below is the file that contains some information about the project like the dependencies list, versions etc.
{input.packagejson}


### Test Framework
The test framework used for running tests is `{input.testFramework}`


## Response
The output should be a valid program of {input.extension} language. Additional notes should be included as comments only.
    """
    return prompt
