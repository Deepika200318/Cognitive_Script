import os
from dotenv import load_dotenv


load_dotenv()

definitions = os.getenv("DEFINITION","")
parameter_name = os.getenv("PARAM_NAME","")
machine_parm_name = os.getenv("MACHINE_PARAM_NAME","")
transcript_file = os.getenv("INPUT_FILE")
gt_file = os.getenv("GT_FILE")