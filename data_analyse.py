import pandas as pd
# from config import gt_file,machine_parm_name

gt_file = "/home/hpadmin/Documents/Deepika/Cognitive_Script/input_folders/gt.csv"

machine_parm_name= "Did the collector force the consumer to make the payment (Dispute & Fraud)"

def cal_accuracy():
    df = pd.read_csv(gt_file,keep_default_na=False)
    print(df[machine_parm_name])
    print(df['Audio Name'])



output_file = "output_Did_the_collector_force_the_consumer_to_make_the_payment?.csv"
cal_accuracy(output_file)