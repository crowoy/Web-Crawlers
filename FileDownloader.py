import os
import urllib
import requests
from bs4 import BeautifulSoup

originUrl = 'https://www.sfu.ca/'
extensions = ['xls']
searchDepth = 10
outputDirectory = './download/'

def downloadFromUrl(originUrl, extensions, depth, directory):
    downloadCount = 0
    urls = set()
    urls.add(originUrl)

    if not os.path.exists(directory):
        os.makedirs(directory)

    for i in range(depth):
        print("Depth: " + str(i) + " - Pages: " + str(len(urls)) + " - Downloads:  " + str(downloadCount))
        for url in urls.copy():
            source_code = requests.get(url)
            plain_text = source_code.text
            soup = BeautifulSoup(plain_text, "lxml")

            for link in soup.findAll('a'):
                href = url.rsplit('/',1)[0] + '/' + link.get('href')

                if any(ext in href for ext in extensions):
                    fileName = href.rsplit('/',1)[1]
                    filename = fileName.decode('iso-8859-1')
                    fileName = urllib.unquote(fileName)

                    fullPath = directory + fileName

                    if not os.path.exists(fullPath):
                        urllib.urlretrieve (href, fullPath)
                        downloadCount += 1
                        print(fileName)
                else:
                    urls.add(href)

    print("Pages visited: " + len(urls))
    print("Files downloaded: " + downloadCount)

downloadFromUrl(originUrl, extensions, searchDepth, outputDirectory)