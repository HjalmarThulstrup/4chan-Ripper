import bs4, argparse, sys, re, datetime, time, shutil, os.path, random
import urllib.request as urllib
import urllib.parse as urlparse
from hurry.filesize import size
import dir_time_bar as dtb


def get_html(url):
    try:
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
               'Accept-Encoding': 'none',
               'Accept-Language': 'en-US,en;q=0.8',
               'Connection': 'keep-alive'}
        req = urllib.Request(url, headers=hdr)
        res = urllib.urlopen(req)
        txt = res.read()
        txtstr = txt.decode("utf-8")
        return txtstr
    except:
        parser.print_help()
        sys.exit()


def get_board_name(url):
    path = urlparse.urlparse(url).path.split("/")[1]
    return '[' + path + ']'


def get_op(html):
    folder_name = ''
    soup = bs4.BeautifulSoup(html, 'html.parser')
    subjects = soup.find_all('span', {'class': 'subject'})
    subject = subjects[1].text
    op = soup.find('blockquote', {'class': 'postMessage'}).text
    if subject != "":
        subject = subject.replace("'", "")
        subject = re.sub(r"[^a-zA-Z0-9-!]+", ' ', subject)
        subject_words = subject.split(" ")
        folder_name += make_str(subject_words, True)
    else:
        op = op.replace("'", "")
        op = re.sub(r"[^a-zA-Z0-9-!]+", ' ', op)
        op_words = op.split(" ")
        folder_name += make_str(op_words, False)
    if folder_name[:1] == "_":
        return folder_name[1:-1]
    else:
        return folder_name[:-1]


def make_str(words, subject_bool):
    string = ''
    if not subject_bool:
        if len(words) < 7:
            for word in words:
                string += word + "_"
        else:
            for x in range(0, 7):
                string += words[x] + "_"
    else:
        for word in words:
            string += word + "_"
    return string

def check_fn(filename, fn_dict):
    new_fn = filename.lower()
    if new_fn in fn_dict:
        fn_l = filename.rsplit('.', 1)
        new_fn = fn_l[0] + str(random.randint(1, len(fn_dict))) + '.' + fn_l[1]
        if new_fn in fn_dict:
            check_fn(new_fn, fn_dict)
        else:
            return new_fn
    else:
        return new_fn

def get_download_links(html):
    soup = bs4.BeautifulSoup(html, 'html.parser')
    event_cells = soup.find_all('div', {'class': 'fileText'})
    url_filename_dict = {}
    for e in event_cells:
        file_url = e.select('a')[0]['href']
        file_url = "https:" + file_url
        filename = e.select('a')[0]
        if filename.has_attr('title'):
            filename = filename['title']
        else:
            filename = filename.text
        if filename == "Spoiler Image":
            filename = e["title"]
        filename = check_fn(filename, url_filename_dict)
        url_filename_dict.update({filename: file_url})
    return url_filename_dict



def download_files(links_and_filenames_dict, directory, url, list_bool, time_bool, overwrite_bool, length, index=1):
    start = time.time()
    path = get_board_name(url) + get_op(get_html(url)) + '/'
    i = index
    if directory == None:
        dtb.check_dir(path, overwrite_bool, length, index)
    else:
        path = directory + path
        dtb.check_dir(path, overwrite_bool, length, index)
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
            dtb.printProgressBar(i, length, prefix = 'Progress:', suffix = 'Complete', length = 25)
            i += 1
        except Exception as e:
            print(e)
    end = time.time()
    total_time = end - start
    if time_bool:
        dtb.get_time(total_time)
    if not list_bool:
        dir_files_list = dtb.calc_dir_size(path, list_bool)
        print("\nYou downloaded " +
              dir_files_list[1] + " files with a combined filesize of " + dir_files_list[0])
    else:
        return_list = [dtb.calc_dir_size(path, list_bool), i]
        return return_list


if __name__ == '__main__':
    disk_space = 0
    amount_files = 0
    parser = argparse.ArgumentParser(
        description='A script that downloads all media files from a 4chan thread')
    parser.add_argument(
        '-u', '--url', help='URL for the 4chan thread you want to download the files from')
    parser.add_argument('-d', '--destination', help='The absolute path to the directory you want the new folder with the downloaded files to be stored in. NOTE: If left blank, a new directory will be created in the active directory from where you are running the script.')
    parser.add_argument(
        '-l', '--list', help="List of thread URLs you want to download the files from. List needs to be surrounded by quotation marks and URLs seperated by spaces.", type=str)
    parser.add_argument(
        '-o', '--overwrite', help='Automatically overwrites any folders with the same name as the folders being created by the script', action='store_true')
    args = parser.parse_args()
    if args.url == None:
        if args.list == None:
            parser.print_help()
            sys.exit()
    if args.url == "test":
        print("URL: " + str(args.url))
        print("Destination: " + str(args.destination))
        print("URL List:" + str(args.list))
        sys.exit()
    dest = args.destination
    if dest != None:
        if dest[-1:] != "/" or dest[-1:] != "\\":
            dest = dest + "/"
    if args.list != None:
        start = time.time()
        url_list = [str(item) for item in args.list.split(' ')]
        length = 0
        index = 1
        for url in url_list:
            length += len(get_download_links(get_html(url)))
        for url in url_list:
            return_list = download_files(get_download_links(get_html(url)),
                                         dest, url, True, False, args.overwrite, length, index)
            disk_space += return_list[0][0]
            amount_files += return_list[0][1]
            index = return_list[1]
        end = time.time()
        total_time = end - start
        dtb.get_time(total_time)
    else:
        download_files(get_download_links(get_html(args.url)),
                       dest, args.url, False, True, args.overwrite, len(get_download_links(get_html(args.url))))
    if disk_space > 0:
        print("\nYou downloaded " +
              str(amount_files) + " files with a combined filesize of " + size(disk_space))
