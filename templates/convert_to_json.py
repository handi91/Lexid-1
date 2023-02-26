import pandas as pd 

data = pd.read_csv('questions.csv')
data.to_json('questions.json',orient='records', indent=2)