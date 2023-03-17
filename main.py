import requests
from bs4 import BeautifulSoup
import json
from xml.etree import ElementTree

DEBUGING = False

# Download page html code
url_site = input("Please insert the link to the song from songsterr\n - ")
r = requests.get(url=url_site)

# Parse html code
soup = BeautifulSoup(r.text, 'html.parser')

scripts = soup.body.find_all("script")

for script in scripts:
    try:
        if script.attrs['id'] == "state":
            state = json.loads(str(script.string))
            break
    except KeyError:
        pass

# Parse json file
revisionId = str(state['meta']['current']['revisionId'])
title = str(state['meta']['current']['title'])
artist = str(state['meta']['current']['artist'])

# Download xml file
url_xml = f"https://www.songsterr.com/a/ra/player/songrevision/{revisionId}.xml"
r = requests.get(url=url_xml)

# Parse xml file
tree = ElementTree.ElementTree(ElementTree.fromstring(r.text))
root = tree.getroot()
url_gp5 = root[1][1][0].text

# Download gp5 file
r = requests.get(url=url_gp5)

# Suggested by mfr-panda 
# Remove invalid chars in output file name (/, \, ...)
char_remove = ["/", "\\"]
file_output = f"{artist} - {title} Tab.gp5"
for char in char_remove:
    file_output = file_output.replace(char, "-")

# Create gp5 file
with open(file_output, "wb") as gp5_file:
    gp5_file.write(r.content)
