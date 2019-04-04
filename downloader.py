import bs4
import argparse
import urllib.request as urllib
import urllib.parse as urlparse
import os.path
import sys


def get_html(url):
    res = urllib.urlopen(url)
    txt = res.read()
    txtstr = txt.decode("utf-8")
    return txtstr


def get_board_thread_name(url):
    # nl = urlparse.urlparse(url).netloc.split(".")[1]
    # path = urlparse.urlparse(url).path.split("/")[1] + "_" + urlparse.urlparse(url).path.split("/")[3]
    path = urlparse.urlparse(url).path.split("/")[1]
    # return nl + "_" + path
    return '[' + path + ']'


def get_op(html):
    soup = bs4.BeautifulSoup(html, 'html.parser')
    op = soup.find('blockquote', {'class': 'postMessage'}).text
    op = op.replace(">", "")
    op = op.replace("<", "")
    op = op.replace("\n", " ")
    op_words = op.split(" ")
    new_op = ''
    if len(op_words) < 5:
        for word in op_words:
            new_op += word + "_"
    else:
        for x in range(0, 5):
            new_op += op_words[x] + "_"
    return new_op[:-1]


def get_download_links(html):
    soup = bs4.BeautifulSoup(html, 'html.parser')
    event_cells = soup.find_all('div', {'class': 'fileText'})

    url_filename_dict = {}
    for e in event_cells:
        file_url = e.select('a')[0]['href']
        file_url = "https:" + file_url
        filename = e.select('a')[0].text
        if filename == "Spoiler Image":
            filename = e["title"]
        url_filename_dict.update({filename: file_url})
    return url_filename_dict


def make_dir(path):
    try:
        os.mkdir(path)
    except OSError:
        print("Creation of the directory %s failed" % path)
    else:
        print("Successfully created the directory %s " % path)


def download_files(links_and_filenames_dict, directory, url):
    # path = get_board_thread_name(url) + '/'
    path = get_board_thread_name(url) + get_op(get_html(url)) + '/'
    if directory == None:
        make_dir(path)
    else:
        path = directory + path
        make_dir(path)
    for filename_key, url_value in links_and_filenames_dict.items():
        try:
            with urllib.urlopen(url_value) as dlFile:
                content = dlFile.read()
                filename = filename_key.replace('?', '')
                complete_name = os.path.join(path + filename)
                file = open(complete_name, "wb")
                file.write(content)
                file.close
            print(url_value + " was saved as " + filename)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='A script that downloads all media files from a 4chan thread')
    parser.add_argument(
        'url', help='URL for the 4chan thread you want to download the files from')
    parser.add_argument('-d', '--destination', help='The absolute path to the directory you want the new folder with the downloaded files to be stored in. NOTE: If left blank, a new directory will be created in the active directory from where you are running the script.')
    args = parser.parse_args()
    if args.url == "test":
        print("URL: " + str(args.url))
        print("Destination: " + str(args.destination))
        sys.exit()
    download_files(get_download_links(get_html(args.url)),
                   args.destination, args.url)
