# 4chan Ripper
I made this script so you nice and easily can download all media files from any 4chan thread on a worksafe board.


To run the script, you need to have Python 3.7 plus a few modules installed:
	
	beautifulsoup4
	argparse
	urllib
  
To run the script and save the files in a folder created by the script, type in the following command:

	python3 downloader.py [url]

To run the script and save the files in a folder created by the script, and save that folder in a specific folder of your choosing, type in the following:

	python3 downloader.py [url] -d [absoulute path to folder]

or

	python3 downloader.py [url] --destination [absoulute path to folder]

For help, type in:

	python3 downloader.py -h
