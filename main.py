from prompt_generator import get_prompts


if __name__ == "__main__":
    
    definitions = """
        There was no payment discussion in the call | Abrupt call disconnection before the collector could obtain authorization from cardholder.

    """
    def_list = definitions.strip("\n").lstrip(' ').split("|")

    print(def_list)

    #Get all prompts
    prompts = get_prompts(def_list)

    # Make a csv prompts file with all the entity,question,prompt and propagation sequence

    # make an api call to llama server
    

