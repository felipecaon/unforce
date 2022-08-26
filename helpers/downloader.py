import requests
import os
import re

# Ignore requests lib SSL warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from helpers.utils import remove_http_schema, format_url_to_snake_case, save_data_in_file
from helpers.constants import BASE_FOLDER_NAME, REQUESTS_FOLDER_NAME, RESPONSE_FOLDER_NAME

def make_post_request(url: str, path: str, headers: object, data: [object, str] = "", save_as: str = ""):
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
            save_as=save_as
        )
    print("pasou")
    return requests.post(
        url=f'{url}{path}', 
        headers=headers, 
        data=data,  
        verify=False
    )

def save_request_burp_format(url: str, path: str, headers: object, data: [object, str], save_as: str = ""):
    """
    Create burp-like request and saved to text file
    @param: same as requests
    """

    request = f"""POST {path} HTTP/1.1
Host: {remove_http_schema(url)}
{transform_headers_to_list(headers)}
{data.replace(" ", "")}
"""
    path_to_save=f'{format_url_to_snake_case(url)}_{BASE_FOLDER_NAME}/{REQUESTS_FOLDER_NAME}'
    save_data_in_file(path=path_to_save, filename=save_as, data=request)

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