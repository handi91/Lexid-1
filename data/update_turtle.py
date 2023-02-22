import os
import requests

# Konfigurasi server Blazegraph
endpoint_url = 'http://192.168.1.5:9999/blazegraph/sparql'
update_url = 'http://192.168.1.5:9999/blazegraph/namespace/kb/sparql'
headers = {'Content-type': 'application/x-turtle'}

# Mendapatkan daftar file dalam direktori sexual
# directory = 'sexual'
# file_list = os.listdir(directory)
locations = []
list_folder = ['data/bn', 'data/lain-lain', 'data/ln', 'data/perda']
for folder in list_folder:
    for (root, dirs, files) in os.walk(folder, topdown=True):
        for arr in files:
            if root[-1:] != "\\":
                locations.append("{}\{}".format(root, arr))
            else:
                locations.append("{}{}".format(root, arr))

# Mengirimkan data turtle ke server
# while len(locations) > 0:
file_executed = 0
failed_document = []
for file_name in locations:
    file_executed += 1
    # if file_executed > 541:
    with open(file_name, 'rb') as f:
        data = f.read()
        response = requests.post(update_url, headers=headers, data=data)
        if response.status_code == 200:
            print('Data from file {} is successfully uploaded'.format(file_name))
        else:
            print('Failed to upload data from file {}'.format(file_name))
            failed_document.append(file_name)

print("======================FAILED DOCUMENT============================")
print(len(failed_document))
for i in failed_document:
    print(i)

with open("failed.txt", 'w') as f:
    for i in failed_document:
        f.write(i)
