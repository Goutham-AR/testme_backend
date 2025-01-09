from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer
from pydantic import BaseModel
from threading import Thread

class PromptInput(BaseModel):
    code: str
    extension: str
    test_framework: str

def generate_prompt(input: PromptInput):
    prompt = f"""
        Generate unit test for the below given code assuming ${input.test_framework} library is installed. Cover all edge cases and generate only output code as text, no need of any prefix suffix or any extra note. If you want to include some notes, include it as comments in the generated code. Some informations about the code is given after the code.
        code: {input.code}
        file extension: {input.extension}
    """
    return prompt


def generate_tests_streaming(input: PromptInput):
    model_name = "Qwen/Qwen2.5-Coder-7B-Instruct"
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype="auto",
        device_map="auto"
    )
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    streamer = TextIteratorStreamer(
        tokenizer,
        timeout=10,
        skip_prompt=True,
        skip_special_token=True
    )
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
    generate_kwargs = dict(
        model_inputs,
        streamer=streamer,
        max_new_tokens=1500,
    )
    t = Thread(target=model.generate, kwargs=generate_kwargs)
    t.start()

    partial_output = ""
    for new_output in streamer:
        partial_output += new_output
        # generated_ids = [output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, partial_output)]
        # response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        yield { "data": partial_output }
