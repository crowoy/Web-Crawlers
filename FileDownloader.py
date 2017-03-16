import os
import urllib
import requests
from bs4 import BeautifulSoup

urls =  [
        'http://ec.europa.eu/eurostat/',
        'https://www.sfu.ca/',
        'http://www.fao.org/',
        'https://data.humdata.org/',
        'https://world.openfoodfacts.org/'
        ]
extensions = ['xls', 'csv']
searchDepth = 5
outputDirectory =   [
                    './download_eurostat/',
                    './download_sfu/',
                    './download_fao/',
                    './download_hdx/',
                    './download_off/'
                    ]

def downloadFromUrl(originUrl, extensions, depth, directory):
    downloadCount = 0
    urls = set()
    urls.add(originUrl)

    try:
        if not os.path.exists(directory):
            os.makedirs(directory)

        for i in range(depth):
            for url in urls.copy():
                print('Depth: ' + str(i) + '/' + str(searchDepth) + ' - Pages: ' + str(len(urls)) + ' - Downloads:  ' + str(downloadCount))
                source_code = requests.get(url)
                plain_text = source_code.text
                soup = BeautifulSoup(plain_text, 'lxml')

                for link in soup.findAll('a'):
                    if link.get('href') == None:
                        href = str(url.rsplit('/',1)[0])
                    else :
                        href = str(url.rsplit('/',1)[0]) + '/' + str(link.get('href'))

                    if any(ext in href for ext in extensions):
                        fileName = href.rsplit('/',1)[1]
                        filename = fileName.decode('iso-8859-1')
                        fileName = urllib.unquote(fileName)

                        fullPath = directory + fileName

                        if not os.path.exists(fullPath):
                            urllib.urlretrieve (href, fullPath)
                            downloadCount += 1
                            # print(fileName)
                    else:
                        urls.add(href)
    except Exception:
        print(url.rsplit('/',1)[0] + ' ---------- ' + link.get('href'))
        pass

    print('Pages visited: ' + str(len(urls)))
    print('Files downloaded: ' + str(downloadCount))

for i in range(len(urls)):
    url = urls[i]
    directory = outputDirectory[i]
    print('URL: ' + str(url) + ' - Directory: ' + str(directory) + ' - Depth: ' + str(searchDepth))
    downloadFromUrl(url, extensions, searchDepth, directory)