from flask import Flask, request, jsonify
from flask_cors import CORS
import torch
from unsloth import FastLanguageModel
from transformers import TextStreamer
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Model parameters
max_seq_length = 2048
load_in_4bit = True

# Load the model once when the server starts
print("Loading model...")
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = os.environ.get("MODEL_PATH", "lora_model"),
    max_seq_length = max_seq_length,
    load_in_4bit = load_in_4bit,
)
# Prepare model for inference
FastLanguageModel.for_inference(model)
print("Model loaded successfully!")

# Define the prompt template (same as used during training)
alpaca_prompt = """Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

### Instruction:
{}

### Input:
{}

### Response:
"""

def process_message(message):
    """Process user messages to determine instruction and input"""
    # Default values
    instruction = message
    input_text = ""
    
    # Process based on message content
    if "SMILES" in message and "notation" in message:
        # User is asking for SMILES notation
        instruction = "Provide the SMILES notation for the following chemical compound."
        # Extract the compound name
        if "for" in message:
            input_text = message.split("for")[-1].strip().rstrip('?.')
    elif "SMILES" in message:
        # User is providing a SMILES notation
        instruction = "Provide information about the chemical compound with the following SMILES notation."
        # Extract the SMILES string
        input_text = message.split("SMILES")[-1].strip().rstrip('?.')
    elif "properties" in message.lower() or "describe" in message.lower():
        instruction = "Describe the key properties of the following chemical compound."
        # Extract the compound name
        if "of" in message:
            input_text = message.split("of")[-1].strip().rstrip('?.')
        else:
            input_text = message.replace("describe", "").replace("properties", "").strip().rstrip('?.')
    
    return instruction, input_text

def generate_response(instruction, input_text=""):
    """Generate a response using the fine-tuned model."""
    prompt = alpaca_prompt.format(instruction, input_text)
    inputs = tokenizer([prompt], return_tensors="pt").to("cuda" if torch.cuda.is_available() else "cpu")
    
    outputs = model.generate(
        **inputs,
        max_new_tokens=256,
        use_cache=True
    )
    return tokenizer.batch_decode(outputs)[0]

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message', '')
    
    # Process the message to get instruction and input
    instruction, input_text = process_message(message)
    
    try:
        # Generate response
        response = generate_response(instruction, input_text)
        
        # Extract just the response part (after "### Response:")
        if "### Response:" in response:
            response = response.split("### Response:")[-1].strip()
        
        return jsonify({"message": response})
    except Exception as e:
        print(f"Error generating response: {e}")
        return jsonify({"message": f"Sorry, an error occurred: {str(e)}"}), 500

@app.route('/run-code', methods=['POST'])
def run_code():
    data = request.json
    code = data.get('code', '')
    
    
    result = f"Simulated execution of:\n\n{code}\n\nOutput would appear here in a production environment."
    
    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)), debug=False)