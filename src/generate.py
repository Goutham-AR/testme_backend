from transformers import AutoModelForCausalLM, AutoTokenizer
from pydantic import BaseModel


class PromptInput(BaseModel):
    code: str
    extension: str
    test_framework: str

def generate_prompt(input: PromptInput):
    prompt = f"""
        Generate unit test for the below given code assuming ${input.test_framework} library is installed. Don't use any additional libraries other than the testing library. Cover all edge cases and generate only output file content and not any extra note. If you want to include some notes, include it as comments in the generated code. Some informations about the code is given after the code.
        code: {input.code}
        file extension: {input.extension}
    """
    return prompt


def generate_tests(input: PromptInput):
    model_name = "Qwen/Qwen2.5-Coder-14B-Instruct-AWQ"
    
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype="auto",
        device_map="auto"
    )
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    prompt = generate_prompt(input)
    messages = [
        {"role": "system", "content": "You are qwen, a helpful assistant that will help me generate test cases"},
        {"role": "user", "content": prompt}
    ]
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)
    
    generated_ids = model.generate(
        **model_inputs,
        max_new_tokens=1500
    )
    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]
    
    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return response
