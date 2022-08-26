import re
import json

from helpers.constants import USER_AGENT, AURA_ENDPOINTS, BASE_FOLDER_NAME
from helpers.downloader import make_post_request
from helpers.utils import save_data, format_url_to_snake_case, save_response
from helpers.cache import save_cache

class SFAura:
    def __init__(self, url):
        self.url = url
        self.endpoint = ""
        self.context = ""
        self.fwuid = ""
        self.context = ""
        self.token = "unforcerocks"

        self.folder = f'{format_url_to_snake_case(url)}_{BASE_FOLDER_NAME}'
        self.header = {'User-Agent':f'{USER_AGENT}', 'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}

    def is_salesforce_aura(self) -> bool:
        """
        Checks if URL is using salesforce lightining. 
        If yes, attributes url and path to scope variable 
        @return: boolean value
        """

        for endpoint in AURA_ENDPOINTS: 
            response = make_post_request(url=self.url, path=endpoint, headers=self.header)

            if 'aura:invalidSession' in response.text:
                self.endpoint = endpoint
                break
            
        return bool(self.endpoint)

    @staticmethod
    def build_context(fwuid: str) -> object:
        """
        Builds json formatted context
        @param: fwuid str
        @return: json object
        """
        return json.dumps({"mode":"PROD","fwuid":fwuid,"app":"siteforce:communityApp","loaded":{"APPLICATION@markup://siteforce:communityApp":""},"dn":[],"globals":{},"uad":False})

    def retrive_fwuid(self) -> None:
        """
        Uses regex to extract fwuid
        """
        message = {}
        context = self.build_context("givemefwuid")
        post_data = f'message={message}&aura.context={context}&aura.token={self.token}'
        response = make_post_request(url=self.url, path=self.endpoint, headers=self.header, data=post_data)

        fwuid_pattern = "Expected:(.*?) Actual"
        self.fwuid = re.search(fwuid_pattern, response.text).group(1).strip()
        self.context = self.build_context(self.fwuid)
    
        save_cache(path=self.folder, url=self.url, fwuid=self.fwuid, endpoint=self.endpoint)

    def get_config_data(self) -> object:
        """
        Calls getConfigData
        @return: json object
        """
        message = json.dumps({"actions":[{"id":"123;a","descriptor":"serviceComponent://ui.force.components.controllers.hostConfig.HostConfigController/ACTION$getConfigData","callingDescriptor":"UNKNOWN","params":{}}]})
        post_data = f'message={message}&aura.context={self.context}&aura.token={self.token}'
        return make_post_request(url=self.url, path=self.endpoint, headers=self.header, data=post_data, save_as="get_config_data", path_to_save=self.folder).json()

    def get_objects(self, json: object) -> list:
        """
        Returns objects from config data
        @param: json object
        @return: list of objects
        """
        objects = list(json['actions'][0]['returnValue']['apiNamesToKeyPrefixes'].keys())
        for obj in objects:
            save_data(path=self.folder, filename="objects", data=obj + '\n')
        return objects

    def get_csp_trusted_urls(self, json: object) -> list:
        """
        Returns csp trusted sites from config data
        @param: json object
        @return: list of trusted sites
        """
        sites = json['actions'][0]['returnValue']['cspTrustedSites']
        for site in sites:
            save_data(path=self.folder, filename="csp_sites", data=site + '\n')

    def get_objects_items(self, items: list):
        """
        Returns items of an object
        @param: items list
        """
        for item in items:
            message = self.build_object_item_message(item)
            post_data = f'message={message}&aura.context={self.context}&aura.token={self.token}'
            response = make_post_request(url=self.url, path=self.endpoint, headers=self.header, data=post_data, save_as=f'{item}_object', path_to_save=self.folder).json()
            save_response(path=self.folder, filename=f'{item}_object', data=str(response))

    @staticmethod
    def build_object_item_message(item: str) -> object:
        """
        Builds json formatted message for retrieving items of an object 
        @param: item str
        @return: json object
        """
        return json.dumps({"actions":[{"id":"123;a","descriptor":"serviceComponent://ui.force.components.controllers.lists.selectableListDataProvider.SelectableListDataProviderController/ACTION$getItems","callingDescriptor":"UNKNOWN","params":{"entityNameOrId":item,"layoutType":"FULL","pageSize":100,"currentPage":0,"useTimeout":False,"getCount":False,"enableRowActions":False}}]})
    
    def get_item_record(self, objects: object):
        for obj in objects:
            message = json.dumps({"actions":[{"id":"123;a","descriptor":"serviceComponent://ui.force.components.controllers.detail.DetailController/ACTION$getRecord","callingDescriptor":"UNKNOWN","params":{"recordId":"0DB3k0000005W3eGAE","record":null,"inContextOfComponent":"","mode":"VIEW","layoutType":"FULL","defaultFieldValues":null,"navigationLocation":"LIST_VIEW_ROW"}}]})
        pass

    def get_custom_controllers(self):
        pass

    def update_scope_from_cache(self, fwuid: str, endpoint: str):
        """
        Updates scope with results retrieved from cache 
        @param: fwuid str
        @param: endpoint str
        """
        self.fwuid = fwuid
        self.context = self.build_context(self.fwuid)
        self.endpoint = endpoint

     