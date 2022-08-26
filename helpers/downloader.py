import requests
import os
import re

# Ignore requests lib SSL warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from helpers.utils import remove_http_schema, format_url_to_snake_case, save_data
from helpers.constants import REQUESTS_FOLDER_NAME

def make_post_request(url: str, path: str, headers: object, data: [object, str] = "", save_as: str = "", path_to_save: str = ""):
    """
    Wrapper around request.post
    @param: same as requests
    @param save_as str, enables request logging in file, saves log with desidered name
    @return: requests object
    """

    if save_as:
        save_request_burp_format(
            url=url,
            path=path,
            headers=headers,
            data=data,
            save_as=save_as,
            path_to_save=path_to_save
        )
    print("pasou")
    return requests.post(
        url=f'{url}{path}', 
        headers=headers, 
        data=data,  
        verify=False
    )

def save_request_burp_format(url: str, path: str, headers: object, data: [object, str], save_as: str = "", path_to_save: str = ""):
    """
    Create burp-like request and saved to text file
    @param: same as requests
    """

    request = f"""POST {path} HTTP/1.1
Host: {remove_http_schema(url)}
{transform_headers_to_list(headers)}
{data.replace(" ", "")}
"""
    save_data(path=f'{path_to_save}/{REQUESTS_FOLDER_NAME}', filename=save_as, data=request)

def transform_headers_to_list(headers: dict) -> str:
    """
    Converts dicionary to text key:value fomat
    @param: headers dict
    @return request-like string 
    """
    output = ""
    for attr, value in headers.items():
        output += attr + ": " + value + "\n"
    return output