import pandas as pd
from tqdm import tqdm
import requests
import json
import ast
import os
from config import transcript_file


def extract_information(text, entity, text_language, prompts, prompt_prop_seq, additional_params=None):
    url = "http://127.0.0.1:5000/extract_information"
    headers = {"Content-Type": "application/json"}
    additional_params = {"prompt_propogation_sequence": prompt_prop_seq}
    clean_prompts = [p.strip('"') for p in prompts]
    prompts = [
        {
            "entity": entity,
            "prompts": clean_prompts
        }
    ]

    payload = {
        "text": text,
        "text_language": text_language,
        "prompts": prompts,
        "additional_params": additional_params or {}
    }

    try:
        response = requests.post(url, headers=headers,
                                 data=json.dumps(payload))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None


def run_llm():

    prompts_file = "prompt_file.csv"

    df = pd.read_csv(transcript_file)
    prompts_df = pd.read_csv(prompts_file)


    prompts_sets = []
    for _, prow in prompts_df.iterrows():
        entity = prow["entity"]
        question = prow["question"]
        prompts = [p.strip() for p in prow["prompt"].split("|")]
        propagation_sequence = ast.literal_eval(prow["propagation_sequence"])
        prompts_sets.append({
            "entity": entity,
            "prompts": prompts,
            "question": question,
            "propagation_sequence": propagation_sequence
        })

    text_language = "en"


    # 🔹 Process one prompt set fully across all files before moving to the next
    for pset in prompts_sets:
        entity = pset["entity"]
        question = pset["question"]
        results = []

        output_file = f"output_files/output_{question.replace(' ','_')}.csv"
        # output_file = "Output_file.csv"

        for idx, row in tqdm(df.iterrows(), total=len(df), desc=f"Processing '{question}'"):
            filename = row["filename"]
            text = row["text"]


            api_response = extract_information(
                text, entity, text_language, pset["prompts"], pset["propagation_sequence"])
            print("##### API Response:", api_response)
            if api_response and api_response.get("success") == "true":
                derived = api_response.get("data", {}).get("derived_value", [])
                if derived:
                    last_item = derived[-1]
                    result_value = last_item.get("result", "NA")
                    explanation = last_item.get("reference", [{}])[
                        0].get("text", "")
                else:
                    result_value = "NA"
                    explanation = ""
            else:
                result_value = "ERROR"
                explanation = ""

            results.append({
                "File_name": filename,
                "Audit_question": question,
                "Answer": result_value,
                "Text": explanation
            })

            # 🔹 Save every 1000 steps
            if (idx + 1) % 10 == 0:
                checkpoint_df = pd.DataFrame(results)
                checkpoint_df.to_csv(output_file, index=False)
            #     print(f"💾 Checkpoint saved after {idx+1} rows to {output_file}")

        # 🔹 Save final for this question
        # output_df = pd.DataFrame(results)
        # # output_df.to_csv("/test_results/{output_file}", index=False)
        # output_df.to_csv(output_file, index=False)

        print(f"✅ Final results for '{question}' saved to {output_file}")
        print(f"Output file: {output_file}")
        return output_file
