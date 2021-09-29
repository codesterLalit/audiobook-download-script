import os
import requests
from bs4 import BeautifulSoup
import sys, getopt



def set_base_url(argv):
    if argv[0] =='-d':
        if argv[1]:
            return argv[1]
        else:
            print("Error: \nCorrect Format: python book-download.py -d <url>")
            sys.exit()
    else:
        print("Error: \nCorrect Format: python book-download.py -d <url>")
        sys.exit()
    
def get_audio_links(base_url):
    audio_links = []
    r = requests.get(base_url)

    soup = BeautifulSoup(r.content,'html.parser')
    links = soup.findAll('source')
    
    for link in links:
        if link['src'] and link['src'].find('.mp3') > 0:
            audio_links.append(link['src'])
    return audio_links

def download_audiobook(audio_links, base_url):
    folder = base_url.split('/')[-1]
    print("Directory created");
    print("Download Started...\n");
    
    os.mkdir(folder)
    for linkIndex, link in enumerate(audio_links):
        file_name = str(linkIndex + 1)+'.mp3'
        target = os.path.join(folder,file_name)
        

        print("Downloading file: %s"%file_name)

        r = requests.get(link, stream=True)

        #creating response object
        with open(target,'wb') as f:
            for chunk in r.iter_content(chunk_size = 1024 * 1024):
                if chunk:
                    f.write(chunk)
        print("%s downloaded!\n"%file_name)
    print("All audio downloaded");


if __name__ == "__main__":
    baseUrl = set_base_url(sys.argv[1:])
    print("Process initiated")
    audio_links = get_audio_links(baseUrl)
    print("Audio Link are found");
    download_audiobook(audio_links,baseUrl)
