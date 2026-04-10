import csv
import pandas as pd
from config import machine_parm_name

prompt_file = "/home/hpadmin/Documents/Deepika/Cognitive_Script/prompt_file.csv"

def make_prompt_file(prompts):
    if prompts:
        clean_prompts = prompts[0]
        for prompt in prompts[1:]:
            clean_prompts = clean_prompts + "|" + prompt
        results = []
        results.append({
            "entity":"clear_and_effective_communication_sequence",
            "question": machine_parm_name,
            "prompt" : clean_prompts,
            "propagation_sequence": len(prompts)*["YES"]
        })

        output_df = pd.DataFrame(results)
        output_df.to_csv(prompt_file,index=False)
        print(f"Prompt File is made and stored at {prompt_file}")


    else:
        print("Missing prompts!!")