import requests

list_url = "https://api.mfapi.in/mf"
filter_criteria = []
def list_all_mfs():
    response = requests.get(list_url)
    data = response.json()
    # Print the JSON data
    print(data)


list_all_mfs()