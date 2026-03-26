import torch
from transformers import AutoTokenizer, AutoModelForCausalLM


MODEL_PATH = "/home/hpadmin/Documents/Deepika/Cognitive_Script/qwen3_model/models--Qwen--Qwen3-4B-Instruct-2507/snapshots/cdbee75f17c01a7cc42f958dc650907174af0554"   # change if needed

def load_model():
    print("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_PATH,
        use_fast=False,          # Important for Qwen
        trust_remote_code=True
    )

    print("Loading model...")
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_PATH,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        device_map="auto" if torch.cuda.is_available() else None,
        trust_remote_code=True
    )

    if not torch.cuda.is_available():
        model = model.to("cpu")

    print("Model loaded successfully!\n")
    return tokenizer, model


def generate_response(tokenizer, model, prompt):
    messages = [
    {"role": "user", "content": prompt}
    ]
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=False # Switches between thinking and non-thinking modes. Default is True.
    )
    inputs = tokenizer(text, return_tensors="pt")

    if not prompt.strip():
        print("PLease enter a valid message")

    if torch.cuda.is_available():
        inputs = {k: v.to(model.device) for k, v in inputs.items()}

    print("Sending to the model")
    outputs = model.generate(
        **inputs,
        max_new_tokens=300,
        temperature=0.7,
        top_p=0.9,
        do_sample=True
        
    )
    print("Response generated successfully!!")

    return tokenizer.decode(outputs[0], skip_special_tokens=True)
