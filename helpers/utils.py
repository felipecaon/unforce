import re
import os

from helpers.constants import BASE_FOLDER_NAME, REQUESTS_FOLDER_NAME, RESPONSE_FOLDER_NAME

def remove_http_schema(url: str) -> str:
    """
    Remove http schema
    @param: url str
    @return: str without http schema
    """
    return re.sub(r'https?:\/\/', '', url)

def format_url_to_snake_case(url: str) -> str:
    """
    Converts url input to snake case
    @param: url str
    @return: snake case str
    """
    return remove_http_schema(url).replace(".", "_").replace("/", "_")

def create_folder_structure(target: str) -> str:
    """
    Created folder structure for requests and responses
    @param: target str
    @return: base folder str
    """

    if not os.path.isdir(BASE_FOLDER_NAME):
        os.mkdir(BASE_FOLDER_NAME)

    snake_case_target = format_url_to_snake_case(target)
    target_folder_name = f'{BASE_FOLDER_NAME}/{snake_case_target}'

    if not os.path.isdir(target_folder_name):
        os.mkdir(target_folder_name)
        os.mkdir(f'{target_folder_name}/{REQUESTS_FOLDER_NAME}')
        os.mkdir(f'{target_folder_name}/{RESPONSE_FOLDER_NAME}')

    return target_folder_name

def save_data(filename: str, path: str, data: any):
    """
    Creates file with provided parameters
    @param: filename str
    @param: path str
    @param: data any
    """   
    f = open(f'{path}/{filename}.txt', "a")
    f.write(data)
    f.close()

def save_response(filename: str, path: str, data: any):
    """
    Creates file in response folder with provided parameters
    @param: filename str
    @param: path str
    @param: data any
    """   
    f = open(f'{path}/{RESPONSE_FOLDER_NAME}/{filename}.txt', "a")
    f.write(data)
    f.close()