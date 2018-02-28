import requests
import json
import os



# Make a get request to get the latest position of the international space station from the opennotify api.
parameters = {"earth_date": "2018-02-02", "camera": "PANCAM"}
response = requests.get("https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?earth_date=2018-01-22&api_key=DEMO_KEY")
#response = requests.get("https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?earth_date=2015-6-3&camera=navcam&api_key=DEMO_KEY")


# Print the status code of the response.
print(response.status_code)
data = response.json()

os.remove("images.txt")

text_file = open("images.txt", "w")
#text_file.write("Purchase Amount: %s" % TotalAmount)
#text_file.close()

#j = json.loads(data)
for entry in data["photos"]:
    print(entry["img_src"])
    text_file.write(entry["img_src"])
    text_file.write("\n")

text_file.close()



#print(response.headers["content-type"])

'''
# Set up the parameters we want to pass to the API.
# This is the latitude and longitude of New York City.
parameters = {"lat": 40.71, "lon": -74}

# Make a get request with the parameters.
response = requests.get("http://api.open-notify.org/iss-pass.json", params=parameters)

# Print the content of the response (the data the server returned)
# print(response.content)

# Get the response data as a python object.  Verify that it's a dictionary.
data = response.json()
print(type(data))
print(data)


# Headers is a dictionary
print(response.headers)

# Get the content-type from the dictionary.
print(response.headers["content-type"])

response = requests.get("http://api.open-notify.org/astros.json")
data = response.json()

print(data)
'''
