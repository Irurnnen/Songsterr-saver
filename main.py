import requests
from bs4 import BeautifulSoup
import json
from xml.etree import ElementTree
import os

DEBUGING = False

#  Download page html code
url = input("Please insert the link to the song from songsterr\n - ")
r = requests.get(url=url)

#  Parse html code
soup = BeautifulSoup(r.text, 'html.parser')

scripts = soup.body.find_all("script")

for script in scripts:
    try:
        if script.attrs['id'] == "state":
            state = json.loads(str(script.string))
            break
    except KeyError:
        pass

#  Parse json file
revisionId = str(state['meta']['current']['revisionId'])

#  Download xml file
url = f"https://www.songsterr.com/a/ra/player/songrevision/{revisionId}.xml"

r = requests.get(url=url)

with open("file.xml", "w") as file:
    file.write(r.text)

#  Parse xml file
tree = ElementTree.parse("file.xml")
root = tree.getroot()
url = root[1][1][0].text
#  Delete xml file
os.remove('file.xml')
# Link output
print(url)