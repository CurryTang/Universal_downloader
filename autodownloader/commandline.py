import argparse
from downloader import connect, analyzeHTML, download, Results
from multiprocessing import cpu_count, Pool
import sys
import os

def argumentHandler(input):
    parser = argparse.ArgumentParser(description="Parse the parameters for pdf downloader")
    parser.add_argument("url", type=str, help="the url of the website which you \
        would like to download all pdf files from")
    parser.add_argument("-p", "--process", dest="process" ,type=int, help="Set up the number of processes when downloading files, \
         default is equal to the number of cpu cores", default = cpu_count())
    parser.add_argument("-v", "--verbose", action="store_true", dest="verbose", help="Verbose information for debugging", \
        )
    parser.add_argument("-t", "--timeout", dest="timeout", type=int, help="Time for download to be timeout", \
        default=20)
    parser.add_argument("-lo", "--location", dest="location", type=str, help="Location of the downloaded file", \
        default=os.getcwd())
    ## TODO: support for pattern
    parser.add_argument("-e", "--ext", dest="extension", type=str, help="Specify the extension of \
        the files that you'd like to download", default="pdf")
    ## TODO: support for self-defined filenames
    return parser.parse_args(input)


def downloadFiles(url, numofProcess, verbose, timeout, location):
    conn = connect(url)
    if not conn:
        print("Unable to connect to corresponding url {}".format(url))
    urlSet = analyzeHTML(conn, url)
    with Pool(processes=numofProcess) as pool:
        res = [pool.apply_async(download, (url, verbose, name, location)) for url, name in urlSet]
        success = [r.get(timeout) for r in res]
        print("Success: {}/{}".format(success.count(Results.SUCCESSFUL), len(success)))
    



if __name__ == '__main__':
    command_line_arg = argumentHandler(sys.argv[1:])
    website = command_line_arg.url
    numofProcess = command_line_arg.process
    verbose = command_line_arg.verbose
    timeout = command_line_arg.timeout
    location = command_line_arg.location
    downloadFiles(website, numofProcess, verbose, timeout, location)



