import os
import requests

# Blazegraph server configuration
# endpoint_url = 'http://localhost:9999/blazegraph/sparql'
# update_url = 'http://localhost:9999/blazegraph/namespace/kb/sparql'
# headers = {'Content-type': 'application/x-turtle'}

endpoint_url = 'http://34.143.173.88:9999/blazegraph/'
update_url = 'http://34.143.173.88:9999/blazegraph/namespace/kb/sparql'
headers = {'Content-type': 'application/x-turtle'}

locations = []
list_folder = ['data/bn', 'data/lain-lain', 'data/ln', 'data/perda']
for folder in list_folder:
    for (root, dirs, files) in os.walk(folder, topdown=True):
        for arr in files:
            if root[-1:] != "\\":
                locations.append("{}\{}".format(root, arr))
            else:
                locations.append("{}{}".format(root, arr))

# send turtle files to server
file_executed = 0
failed_document = []
data_to_process = len(locations)
for file_name in locations:
    file_executed += 1
    if data_to_process < 214:
        with open(file_name, 'rb') as f:
            data = f.read()
            response = requests.post(update_url, headers=headers, data=data)
            if response.status_code == 200:
                print('Data from file {} is successfully uploaded'.format(file_name))
            else:
                print('Failed to upload data from file {}'.format(file_name))
                failed_document.append(file_name)
    data_to_process -= 1
    print(f"{data_to_process} files remaining")

# failed data
print("======================FAILED DOCUMENT============================")
print(len(failed_document))
for i in failed_document:
    print(i)

with open("data/failed-to-upload.txt", 'w') as f:
    for i in failed_document:
        f.write(i)
