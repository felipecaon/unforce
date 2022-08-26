import time
from os.path import exists
import json

def get_cache_by_url(path: str, url: str):
    """
    Returns cache information by url and path
    @param: path str
    @param: url str
    """
    file_name = f'{path}/.unforce'
    if exists(file_name):
        f = open(file_name, "r")
        data = f.read().replace("\'", "\"")
        f.close()
        json_data = json.loads(data)
        return json_data

def save_cache(path: str, url: str, fwuid: str, endpoint: str):
    """
    Saves cache information in hidden file
    @param: path str
    @param: url str
    @param: fwuid str
    @param: endpoint str
    """
    file_name = f'{path}/.unforce'
    if not exists(file_name):
        data = {}
        data['url'] = url
        data['fwuid'] = fwuid
        data['endpoint'] = endpoint
        data["date_created"] = time.strftime("%d-%m-%Y %H:%M")

        f = open(file_name, "a")
        f.write(str(data))
        f.close()

def check_cache(path: str, url: str) -> [None, str]:
    """
    Checks if cache exists
    @param: path str
    @param: url str
    @return: Nothing in cache cache does not exists or cache information in string in case it exists
    """
    current_cache = get_cache_by_url(path, url)

    if not current_cache:
        return
    
    return current_cache