import torch
from unsloth import FastLanguageModel
from transformers import TextStreamer

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

def interactive_mode():
    """Run an interactive session with the model."""
    print("ChEMBL Assistant - Interactive Mode")
    print("Type 'exit' to quit")
    print("=" * 50)
    
    while True:
        instruction = input("\nInstruction (e.g., 'Provide the SMILES notation for the following chemical compound.'): ")
        if instruction.lower() == 'exit':
            break
            
        input_text = input("Input (e.g., 'Aspirin'): ")
        
        print("\nGenerating response...\n")
        generate_response(instruction, input_text)
        print("\n" + "=" * 50)

if __name__ == "__main__":
    # Example usage
    print("ChEMBL Assistant - Example Queries")
    print("=" * 50)
    
    # Example 1: Get SMILES notation
    print("\nExample 1: Get SMILES notation for Aspirin")
    generate_response(
        "Provide the SMILES notation for the following chemical compound.",
        "Aspirin"
    )
    
    # Example 2: Get compound information from SMILES
    print("\n" + "=" * 50)
    print("\nExample 2: Get information about a compound from SMILES")
    generate_response(
        "Provide information about the chemical compound with the following SMILES notation.",
        "CC(=O)OC1=CC=CC=C1C(=O)O"  # SMILES for Aspirin
    )
    
    # Example 3: Describe properties
    print("\n" + "=" * 50)
    print("\nExample 3: Describe properties of Paracetamol")
    generate_response(
        "Describe the key properties of the following chemical compound.",
        "Paracetamol"
    )
    
    # Start interactive mode
    print("\n" + "=" * 50)
    choice = input("\nWould you like to enter interactive mode? (y/n): ")
    if choice.lower() == 'y':
        interactive_mode()
    else:
        print("Exiting. Goodbye!")