import requests

# Ignore requests lib SSL warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def make_post_request(url: str, path: str, headers: object, save: bool = True, data: [object, str] = ""):
    """
    Wrapper around request.post
    @param: same as requests
    @param save boolean, enables request logging in file
    @return: requests object
    """

    if save:
        save_request_burp_format(
            url=url,
            path=path,
            headers=headers,
            data=data
        )

    return requests.post(
        url=f'{url}{path}', 
        headers=headers, 
        data=data,  
        verify=False
    )

def save_request_burp_format(url: str, path: str, headers: object, data: [object, str]):
    """
    Create burp-like request and saved to text file
    @param: same as requests
    """

    request = f"""POST {path} HTTP/1.1
Host: {url}
{transform_headers_to_list(headers)}
{data}
---------"""
    f = open("requests_log.txt", "a")
    f.write(request)
    f.close()

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