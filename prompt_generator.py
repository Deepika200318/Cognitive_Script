import json
from llm_response import load_model,generate_response

prompt_template = """
    Your task is to generate the prompt for meta llama 3.1b model for the following scenario. Mark YES if the following scenarios occur{definition}. Else, Mark NO. Give me a one sigle liner prompt(as a question), which is short and crisp. Answer strictly in valid json format as {{'prompt':<prompt generated>}}.
"""

print(prompt_template)

tokenizer, model = load_model()

def generate_prompt(definition):

    prompt = prompt_template.format(definition =definition)
    response = generate_response(tokenizer,model,prompt)
    print(f"SCRIPT | MAIN | PROMPT GENERATOR | RESPONSE: {response}")

    prompt_extension = "Answer strictly in valid JSON format as {'validation': 'YES'/'NO'}. Provide explanation outside the JSON."
    match = response.find('assistant')
    generated_prompt = response[match:].strip('assistant').strip("\n")

    data = json.loads(generated_prompt)
    generated_prompt = data["prompt"] + prompt_extension
    print(f"SCRIPT | MAIN | PROMPT GENERATOR | GENERATED PROMPTS: {generated_prompt}")
    return generated_prompt


def get_prompts(def_list):
    prompts = []
    for i in def_list:
        prompts.append(generate_prompt(i))
    return prompts
