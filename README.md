# File Downloader

This simple program can help you to download files from website

Usage: 

[-h] [-p PROCESS] [-v] [-t TIMEOUT] url

Parse the parameters for pdf downloader

positional arguments:
  url                   the url of the website which you would like to
                        download all pdf files from

optional arguments:
  -h, --help            show this help message and exit
  -p PROCESS, --process PROCESS
                        Set up the number of processes when downloading files,
                        default is equal to the number of cpu cores
  -v, --verbose         Verbose information for debugging
  -t TIMEOUT, --timeout TIMEOUT
                        Time for download to be timeout