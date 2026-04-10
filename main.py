import os
from config import definitions
from prompt_generator import get_prompts
from store import make_prompt_file
from llm_call import run_llm


if __name__ == "__main__":

    def_list = definitions.strip("\n").lstrip(' ').split("|")

    print(def_list)

    #Get all prompts
    prompts = get_prompts(def_list)

    # Make a csv prompts file with all the entity,question,prompt and propagation sequence
    make_prompt_file(prompts)

    # make an api call to llama server
    output_file = run_llm()

    print(type(output_file))

    #fetch the GT sheet and get the matched/mismatched data
    

