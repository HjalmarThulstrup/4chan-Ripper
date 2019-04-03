import bs4
import argparse
import urllib.request as urllib
import os.path
import sys

def get_html(url):
    res = urllib.urlopen(url)
    txt = res.read()
    txtstr = txt.decode("utf-8")
    return txtstr

def get_download_links(html):
    soup = bs4.BeautifulSoup(html, 'html.parser')
    event_cells = soup.find_all('div', {'class': 'fileText'})

    url_filename_dict = {}
    url_arr = []
    for e in event_cells:
        file_url = e.select('a')[0]['href']
        file_url = "https:" + file_url
        url_arr.append(file_url)
        filename = e.select('a')[0].text
        url_filename_dict.update({filename:file_url})
    return url_filename_dict

def download_files(links_and_filenames_dict):
    for filename_key, url_value in links_and_filenames_dict.items():
        try:
            with urllib.urlopen(url_value) as dlFile:
                content = dlFile.read()
                complete_name = os.path.join('files/' + filename_key)
                file = open(complete_name, "wb")
                file.write(content)
                file.close
            print(url_value + " was saved as " + filename_key)
        except Exception as e: print(e)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A script that downloads all media files from a 4chan thread')
    parser.add_argument('url', help='URL for the 4chan thread you want to download the files from')
    args = parser.parse_args()
    if args.url == "test":
        print("URL: " + str(args.url))
        sys.exit()
    download_files(get_download_links(get_html(args.url)))
