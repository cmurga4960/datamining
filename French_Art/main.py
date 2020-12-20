import time
import requests
from bs4 import BeautifulSoup
import re
import shutil


url_base = "https://www.parismuseescollections.paris.fr"
url_path = "https://www.parismuseescollections.paris.fr/en/recherche/image-libre/true?page="
url_end = "&solrsort=ds_created desc"
end_point = 2313
key_word = "/en/node/"
key_word2 = "/en/zip/"
current = 2004


def download_page(page_url, current):
    r1 = requests.get(page_url)
    soup = BeautifulSoup(r1.text, features="html.parser")
    done = []
    for link in soup.findAll('a', attrs={'href': re.compile("^"+key_word)}):
        art_base = link.get('href')
        if art_base not in done:
            try:
                r2 = requests.get(url_base+art_base)
                soup2 = BeautifulSoup(r2.text, features="html.parser")
                zip = soup2.find('a', attrs={'href': re.compile("^"+key_word2)})
                zip_url = zip.get("href")
                r3 = requests.get(url_base+zip_url, stream=True)
                with open(str(current)+'_'+str(len(done))+'.zip', 'wb') as out_file:
                    shutil.copyfileobj(r3.raw, out_file)
            except Exception as e:
                print(current, len(done), e)

            done.append(art_base)
            time.sleep(3)


if __name__ == '__main__':
    print('starting')
    while current < end_point:
        print(current)
        try:
            download_page(url_path+str(current)+url_end, current)
        except:
            current -= 1
            time.sleep(20)
        current += 1
        time.sleep(5)
    print('done')

