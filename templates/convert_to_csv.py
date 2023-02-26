import pandas as pd

# data = pd.read_csv("valid-document-title.txt", header=None)

# data.columns = ['Peraturan']
# data.to_csv('valid-document-title.csv')
match = 0
titles = []
with open('valid-document-title.txt', 'r') as f:
    for line in f:
        titles.append(line.strip())
titles.sort(reverse=True)
data = {'Peraturan': titles}
df = pd.DataFrame.from_dict(data)
df.to_csv('valid-document-title.csv', index=False)