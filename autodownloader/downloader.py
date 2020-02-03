import requests
from bs4 import BeautifulSoup
import os
from enum import Enum

class Results(Enum):
    SUCCESSFUL=0
    FAILURE=1

def connect(url):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
    try:
        result = requests.get(url, headers=headers)
        if result.ok:
            return result.text
        else:
            return None
    except Exception:
        print("Network Error")


def analyzeHTML(webContent, weburl = "", ext="pdf"):
    result = []
    html = BeautifulSoup(webContent, 'html.parser')
    allUrl = html.find_all("a")
    for url in allUrl:
        if not url.get('href'):
            continue
        corrUrl = url.attrs['href']
        if not corrUrl.endswith(ext):
            continue
        # Check if partial URL or complete URL
        # if not corrUrl.startsWith('http'):
        complete_first = weburl[:weburl.find('/')] if weburl.find('/') != -1 else weburl
        sub_first = corrUrl[:corrUrl.find('/')] if corrUrl.find('/') != -1 else corrUrl
        if complete_first != sub_first:
            if corrUrl.startswith("."):
                completeUrl = weburl + corrUrl[1:]
            else:    
                completeUrl = weburl + corrUrl
        else:
            completeUrl = corrUrl
        name = corrUrl.split('/')[-1] if corrUrl.find('/') != -1 else corrUrl
        result.append((completeUrl, name))
    return result

def download(url, verbose, name, loc):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
    os.chdir(loc)
    res = requests.get(url, headers=headers)
    if res.ok:
        with open(name, 'wb') as f:
            f.write(res.content)
        if verbose:
            print("Successfully download files from {}".format(url))
        return Results.SUCCESSFUL
    else:
        print("Failed to download files from {}".format(url))
        return Results.FAILURE



