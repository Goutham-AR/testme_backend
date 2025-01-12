from threading import Thread

from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer

from .prompt import PromptInput, generate_prompt, PromptInputWithImport, generate_prompt_with_imports

def generate_tests(input: PromptInput):
    model_name = "Qwen/Qwen2.5-Coder-7B-Instruct"

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

def generate_tests_v2(input: PromptInputWithImport):
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
    prompt = generate_prompt_with_imports(input)
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

    for new_output in streamer:
        print(new_output)
        yield new_output
