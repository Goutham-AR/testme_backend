from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from .config import MODEL_NAME

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME, torch_dtype="auto", device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

tokenizer = AutoTokenizer.from_pretrained(
    "deepseek-ai/DeepSeek-Coder-V2-Lite-Instruct", trust_remote_code=True
)
model = AutoModelForCausalLM.from_pretrained(
    "deepseek-ai/DeepSeek-Coder-V2-Lite-Instruct",
    trust_remote_code=True,
    torch_dtype=torch.bfloat16,
).cuda()
