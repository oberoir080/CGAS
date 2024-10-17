import xml.etree.ElementTree as ET

file_path = 'allrecipes_urls.txt'

# Read the content of the XML file
with open(file_path, 'r', encoding='utf-8') as file:
    xml_content = file.read()

# Parse the XML content
try:
    root = ET.fromstring(xml_content)
except ET.ParseError as e:
    print(f"Error parsing XML: {e}")
    exit()

url_set = set()
namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

count = 0
for url in root.findall('ns:url', namespace):
    count+=1
    loc = url.find('ns:loc', namespace)
    if loc is not None and len(url_set)<10000 and count>10000:
        url_set.add(loc.text)

# Save the URL set as a text file
with open('url_set2.txt', 'w', encoding='utf-8') as file:
    for url in url_set:
        file.write(url + '\n')


print(len(url_set))
