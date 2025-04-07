import torch
from unsloth import FastLanguageModel
from transformers import TextStreamer
import os

# Model parameters - should match your training configuration
max_seq_length = 2048
load_in_4bit = True

# Load the fine-tuned model
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "e:/googleAI/lora_model",
    max_seq_length = max_seq_length,
    load_in_4bit = load_in_4bit,
)

# Prepare model for inference
FastLanguageModel.for_inference(model)

# Define the prompt template (same as used during training)
alpaca_prompt = """Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

### Instruction:
{}

### Input:
{}

### Response:
"""

def generate_response(instruction, input_text="", max_new_tokens=256, stream=True):
    """
    Generate a response using the fine-tuned model.
    
    Args:
        instruction: The instruction for the model
        input_text: Additional context for the instruction
        max_new_tokens: Maximum number of tokens to generate
        stream: Whether to stream the output token by token
    
    Returns:
        The generated text
    """
    prompt = alpaca_prompt.format(instruction, input_text)
    inputs = tokenizer([prompt], return_tensors="pt").to("cuda" if torch.cuda.is_available() else "cpu")
    
    if stream:
        text_streamer = TextStreamer(tokenizer)
        _ = model.generate(
            **inputs, 
            streamer=text_streamer,
            max_new_tokens=max_new_tokens,
            use_cache=True
        )
        return None  # Output is streamed directly
    else:
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            use_cache=True
        )
        return tokenizer.batch_decode(outputs)[0]

def chatbot_mode():
    """Run a chatbot-like session with the model."""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=" * 60)
    print("🧪 ChEMBL Assistant - Chemistry Chatbot 🧪")
    print("=" * 60)
    print("Ask me anything about chemical compounds!")
    print("Type 'exit' to quit, 'help' for example queries")
    print("=" * 60)
    
    # Some example instructions for help
    example_instructions = [
        "Provide the SMILES notation for the following chemical compound.",
        "Provide information about the chemical compound with the following SMILES notation.",
        "Describe the key properties of the following chemical compound.",
        "What are the targets of the following compound?",
        "Compare the properties of these two compounds."
    ]
    
    while True:
        print()
        user_input = input("You: ")
        
        if user_input.lower() == 'exit':
            print("\nThank you for using ChEMBL Assistant. Goodbye!")
            break
            
        if user_input.lower() == 'help':
            print("\nHere are some example queries you can try:")
            for i, example in enumerate(example_instructions, 1):
                print(f"{i}. {example}")
            print("\nFor example: 'Provide the SMILES notation for Aspirin'")
            continue
        
        # Process the user input to extract instruction and input
        # For simplicity, we'll use a default instruction if none is detected
        if "SMILES" in user_input and "notation" in user_input:
            # User is asking for SMILES notation
            instruction = "Provide the SMILES notation for the following chemical compound."
            # Extract the compound name (assuming it's at the end of the query)
            compound = user_input.split("for")[-1].strip().rstrip('?.')
        elif "SMILES" in user_input:
            # User is providing a SMILES notation
            instruction = "Provide information about the chemical compound with the following SMILES notation."
            # Extract the SMILES string (this is simplified and might need refinement)
            compound = user_input.split("SMILES")[-1].strip().rstrip('?.')
        elif "properties" in user_input or "describe" in user_input:
            instruction = "Describe the key properties of the following chemical compound."
            # Extract the compound name
            if "of" in user_input:
                compound = user_input.split("of")[-1].strip().rstrip('?.')
            else:
                compound = user_input.replace("describe", "").replace("properties", "").strip().rstrip('?.')
        elif "targets" in user_input:
            instruction = "What are the targets of the following compound?"
            compound = user_input.split("targets")[-1].replace("of", "").strip().rstrip('?.')
        else:
            # Default to a general query
            instruction = user_input
            compound = ""
        
        print("\nChEMBL Assistant: ")
        generate_response(instruction, compound)

if __name__ == "__main__":
    # Run in chatbot mode directly
    chatbot_mode()