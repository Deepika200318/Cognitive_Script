# import csv
# import pandas as pd

# input_file = pd.read_csv("definition.csv")

# print(input_file[0])


import pandas as pd

# Load the CSV
input_file = pd.read_csv("definition.csv")

# Extract each column separately
parameters = input_file['Parameter'].tolist()   # List of all parameters
definitions = input_file['Definition'].tolist() # List of all definitions

# Example: print them separately
print("Parameters:")
for p in parameters:
    print(p)

print("\nDefinitions:")
for d in definitions:
    print(d)