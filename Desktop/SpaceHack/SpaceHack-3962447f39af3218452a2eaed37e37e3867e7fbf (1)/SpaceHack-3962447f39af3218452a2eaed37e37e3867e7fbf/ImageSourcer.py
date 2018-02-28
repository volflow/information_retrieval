import requests
import json
import os

class ImageSourcer:

    # Constructor initialising attributes
    def __init__(self, rover, sol):
        apiKey = "lORFMg7rox7XMLBWzM1byE9fd5WAe3Cf9KkoQYmp"
        self.rover = rover
        self.sol = sol
        self.responseString = ("https://api.nasa.gov/mars-photos/api/v1/rovers/" + self.rover + "/photos?sol="
                              + self.sol + "&api_key=" + apiKey)


    # Write links to images to text file
    def writeToFile(self, data, fileName):
        textFile = open(fileName, "w")
        for entry in data["photos"]:
            print(entry["img_src"])
            textFile.write(entry["img_src"])
            textFile.write("\n")

    # Send API request for JSON object
    def receiveImages(self):
        response = requests.get(self.responseString)

        # Check to see if request OK
        if (response.status_code != 200):
            print ("API Request failed")
        else:
            data = response.json()

            # Create file name and store in folder 'images'
            fileName = self.rover + "-" + self.sol + ".txt"
            completeFileName = os.path.join("images/", fileName)

            # Remove file if already exists for parameters, to allow new data
            # to be retrieved
            if (os.path.isfile(completeFileName)):
                os.remove(completeFileName)
            else:
                self.writeToFile(data, completeFileName)


img1 = ImageSourcer("Curiosity", "500")
img1.receiveImages()
