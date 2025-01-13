from threading import Thread

from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer

from .prompt import (
    PromptInput,
    PromptInputWithSampleTest,
    generate_prompt,
    PromptInputWithImport,
    generate_prompt_with_imports,
    generate_prompt_with_sample_test,
)
from .config import MODEL_NAME


def generate_tests(input: PromptInput):
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME, torch_dtype="auto", device_map="auto"
    )
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    prompt = generate_prompt(input)
    messages = [
        {
            "role": "system",
            "content": "You are qwen, a helpful assistant that will help me generate test cases",
        },
        {"role": "user", "content": prompt},
    ]
    text = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)
    generated_ids = model.generate(**model_inputs, max_new_tokens=1500)
    generated_ids = [
        output_ids[len(input_ids) :]
        for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]

    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return response


def generate_tests_v2(input: PromptInputWithImport):
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME, torch_dtype="auto", device_map="auto"
    )
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    streamer = TextIteratorStreamer(
        tokenizer, timeout=10, skip_prompt=True, skip_special_token=True
    )
    prompt = generate_prompt_with_imports(input)
    messages = [
        {
            "role": "system",
            "content": "You are qwen, a helpful assistant that will help me generate test cases",
        },
        {"role": "user", "content": prompt},
    ]
    text = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)
    generate_kwargs = dict(
        model_inputs,
        streamer=streamer,
        max_new_tokens=3000,
    )
    t = Thread(target=model.generate, kwargs=generate_kwargs)
    t.start()

    for new_output in streamer:
        yield new_output


def generate_tests_v3(input: PromptInputWithSampleTest):
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME, torch_dtype="auto", device_map="auto"
    )
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    streamer = TextIteratorStreamer(
        tokenizer, timeout=10, skip_prompt=True, skip_special_token=True
    )
    prompt = generate_prompt_with_sample_test(input)
    messages = [
        {
            "role": "system",
            "content": "You are qwen, a helpful assistant that will help me generate test cases",
        },
        {"role": "user", "content": prompt},
    ]
    text = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)
    generate_kwargs = dict(
        model_inputs,
        streamer=streamer,
        max_new_tokens=3000,
    )
    t = Thread(target=model.generate, kwargs=generate_kwargs)
    t.start()

    for new_output in streamer:
        yield new_output
