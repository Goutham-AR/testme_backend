from transformers import AutoModelForCausalLM, AutoTokenizer

from .config import MODEL_NAME

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME, torch_dtype="auto", device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
