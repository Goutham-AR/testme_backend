from .prompt import Prompt
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch


async def generate_from_deepseek(prompts: list[Prompt]):
    tokenizer = AutoTokenizer.from_pretrained(
        "deepseek-ai/DeepSeek-Coder-V2-Lite-Instruct", trust_remote_code=True
    )
    model = AutoModelForCausalLM.from_pretrained(
        "deepseek-ai/DeepSeek-Coder-V2-Lite-Instruct",
        trust_remote_code=True,
        torch_dtype=torch.bfloat16,
    ).cuda()
    messages = [{"role": prompt.role, "content": prompt.content} for prompt in prompts]
    inputs = tokenizer.apply_chat_template(
        messages, add_generation_prompt=True, return_tensors="pt"
    ).to(model.device)
    # tokenizer.eos_token_id is the id of <｜end▁of▁sentence｜>  token
    outputs = model.generate(
        inputs,
        max_new_tokens=4500,
        do_sample=False,
        top_k=50,
        top_p=0.95,
        num_return_sequences=1,
        eos_token_id=tokenizer.eos_token_id,
    )
    return tokenizer.decode(outputs[0][len(inputs[0]) :], skip_special_tokens=True)
