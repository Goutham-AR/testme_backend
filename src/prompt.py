from pydantic import BaseModel

class PromptInput(BaseModel):
    code: str
    extension: str
    testFramework: str

class Import(BaseModel):
    path: str
    code: str
    
class PromptInputWithImport(PromptInput):
    imports: list[Import]


def generate_prompt(input: PromptInput):
    prompt = f"""
        Generate unit test for the below given code assuming ${input.testFramework} library is installed. Cover all edge cases and generate only output code as text, no need of any prefix suffix or any extra note. If you want to include some notes, include it as comments in the generated code. Some informations about the code is given after the code.
        code: {input.code}
        file extension: {input.extension}
    """
    return prompt


def generate_prompt_with_imports(input: PromptInputWithImport):
    imports = ""
    for imp in input.imports:
        imports += f"""
            path: {imp.path}
            content: {imp.code},
        """
    prompt = f"""
        Generate unit test for the below code assuming ${input.testFramework} library is installed. Cover all edge cases and generate only output code, no need of any prefix, suffix or any extra notes. If you want to include some notes, include it as comments in the generated code. The extension of the code file is {input.extension}. The code is given between '<code>'. The content of local imports in the given code is given alongside its path after the code segment. Each imports are separated by ','. Also do not add '```typescript' at the beginning.
        <code>
        {input.code}
        <code>
        <imports>
            {imports}
        <imports>
    """
    return prompt
