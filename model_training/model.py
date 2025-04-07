from typing import Any
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

class LLMHandler:
    def __init__(self):
        self.model = None
        self.tokenizer = None

    def initialize(self, context: Any):
        self.tokenizer = AutoTokenizer.from_pretrained("unsloth/llama-3-8b-bnb-4bit")
        self.model = AutoModelForCausalLM.from_pretrained("unsloth/llama-3-8b-bnb-4bit")
        self.model.load_state_dict(torch.load("model_weights.pt"))
        self.model.eval()

    def handle(self, data: Any, context: Any) -> Any:
        inputs = data[0].get("body")
        tokens = self.tokenizer(inputs, return_tensors="pt")
        outputs = self.model.generate(**tokens, max_new_tokens=50)
        return [self.tokenizer.decode(outputs[0], skip_special_tokens=True)]
