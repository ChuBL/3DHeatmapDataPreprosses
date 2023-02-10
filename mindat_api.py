import requests
import sys
import json
from pathlib import Path
import re
import pprint
from datetime import datetime

class MindatApi:
    def __init__(self, API_KEY_FILENAME):
        self._api_key = self._get_api_key(API_KEY_FILENAME)
        self.MINDAT_API_URL = "https://api.mindat.org"
        self._headers = {'Authorization': 'Token '+ self._api_key}
        self.params = {'format': 'json'}
        self.endpoint = "/items/"
        self.data_dir = './mindat_data/'
        Path(self.data_dir).mkdir(parents=True, exist_ok=True)

    def set_params(self, PARAMS_DICT):
        self.params = PARAMS_DICT

    def set_endpoint(self, ENDPOINT):
        self.endpoint = ENDPOINT
        
    def get_params(self):
        return self.params

    def get_headers(self):
        return self._headers
    
    def get_items(self, PARAMS_DICT = {}, FILENAME = 'mindat_items'):
        if {} == PARAMS_DICT:
            params = self.params
        else:
            params = PARAMS_DICT
        print("Retrieving items with params:")
        pprint.pprint(params)

        response = requests.get(self.MINDAT_API_URL+"/items/",
                                params=params,
                                headers=self._headers)

        json_file = response.json()
        if 'mindat_items' == FILENAME:
            export_path = self.data_dir + 'mindat_items.json'
        else:
            export_path = self.data_dir + FILENAME + '.json'
        
        with open(export_path, 'w') as f:
            json.dump(json_file, f, indent=4)
        
        self.print_the_result(json_file, FILENAME)

    def print_the_result(self, JSONFILE, FILENAME):
        print("Successfully retrieved", len(JSONFILE['results']), "items in", FILENAME, '. ')

    def _get_api_key(self, API_KEY_FILENAME):
        try:
            with open(API_KEY_FILENAME, 'r') as f:
                api_key = f.read()
        except FileNotFoundError:
            print("API key file not found. Please create a file containing api key named 'api_key.txt' and place it in the same directory as this script.")
            sys.exit()
        return api_key

    def get_all_items(self):
        # https://api.mindat.org/items/?format=json
        # return all mindat items (minerals, varieties, groups, synonyms, rocks, etc.),
        # unfiltered, paginated
        params = {'format': 'json',
                'page_size': '20'}
        response = requests.get(self.MINDAT_API_URL+"/items/",
                                params=params,
                                headers=self._headers, )
        json_file = response.json()
        saving_path = self.data_dir + 'mindat_items.json'
        with open(saving_path, 'w') as f:
            json.dump(json_file, f, indent=4)

    def get_select_fields_items(self, FILEDS_STR = 'id,name,dispformulasimple',\
                PAGE_SIZE = '100'):
        # https://api.mindat.org/items/?fields=id,name,dispformulasimple&page_size=100
        # display only selected fields.
        # selecting only necessary fields slightly reduces db queries size so its appreciated
        # customize page_size to 100 items per page
        params = {'fields': FILEDS_STR,
                'page_size': PAGE_SIZE,
                'format': 'json'}

        response = requests.get(self.MINDAT_API_URL+"/items/",
                        params=params,
                        headers=self._headers)

        json_file = response.json()
        field_sequence = re.sub(r'\,','_',FILEDS_STR)
        saving_path = self.data_dir + 'mindat_items_with_fields_' + field_sequence + '.json'
        with open(saving_path, 'w') as f:
            json.dump(json_file, f, indent=4)

    def get_omit_fields_items(self, OMIT_STR = 'id,name,dispformulasimple'):
        # https://api.mindat.org/items/?omit=id,name,dispformulasimple
        # exclude fields from display
        params = {'omit': OMIT_STR,
                'format': 'json'}

        response = requests.get(self.MINDAT_API_URL+"/items/",
                        params=params,
                        headers=self._headers)

        json_file = response.json()
        omit_sequence = re.sub(r'\,','_',OMIT_STR)
        saving_path = self.data_dir + 'mindat_items_omit_fields_' + omit_sequence + '.json'
        with open(saving_path, 'w') as f:
            json.dump(json_file, f, indent=4)

    def get_filtered_items(self, FILTERS_DICT = {'density__to': '3',
          'crystal_system': 'Triclinic',
          'color': 'red',
          'ima': 1,          # show only minerals approved by ima
          'format': 'json'}):
        # for filters reference on this endpoint see generated documentation:
        # https://api.mindat.org/schema/redoc/#tag/items/operation/items_list
        
        # filters on minerals, examples
        # https://api.mindat.org/items/?density__to=3&crystal_system=Triclinic&color=red&ima=1
        params = FILTERS_DICT
        response = requests.get(self.MINDAT_API_URL+"/items/",
                        params=params,
                        headers=self._headers)

        json_file = response.json()
        saving_path = self.data_dir + 'mindat_items_filtered.json'
        with open(saving_path, 'w') as f:
            json.dump(json_file, f, indent=4)

    def get_datetime(self):
        # use datetime to get current date and time
        now = datetime.now()
        dt_string = now.strftime("%m%d%Y%H%M%S")
        return dt_string

    def get_ima_items(self):
        '''
            get all minerals approved by ima.
            Since this API has a limit of 1000 items per page,
            we need to loop through all pages and save them to a single json file
        '''
        omit_str = '''updttime,varietyof,synid,polytypeof,groupid,
            entrytype,entrytype_text,description_short,impurities
            '''
        ima_path = self.data_dir
        Path(ima_path).mkdir(parents=True, exist_ok=True)
        date = self.get_datetime()
        print("Retriving Mindat data for IMA approved minerals. This may take a while... ")
        with open(ima_path + 'mindat_items_IMA_' + date + '.json', 'w') as f:
            PAGE_RANGE = 7
            for page in range(1, PAGE_RANGE):
                params = {
                    #'omit': omit_str,
                    #'fields': "id,name,elements",
                    'ima': 1,          # show only minerals approved by ima
                    'page_size': '20000',
                    'page': str(page),
                    'format': 'json'
                }

                response = requests.get(self.MINDAT_API_URL+"/items/",
                                params=params,
                                headers=self._headers)

                json_file = response.json()
                if 1 == page:
                    json_all = json_file
                else:
                    json_all['results'] += json_file['results']

            json.dump(json_all, f, indent=4)
            print("Successfully saved " + str(len(json_all['results'])) + " entries to" + ima_path + 'mindat_items_IMA_' + date + '.json')

    def download_localities(self):
        pass


if __name__ == "__main__":
    ma = MindatApi("api_key.txt")
    # params = {'density__to': '3',
    #       'crystal_system': 'Triclinic',
    #       'color': 'red',
    #       'page_size': '1000',
    #       'ima': 1,          # show only minerals approved by ima
    #       'format': 'json'}
    # ma.set_params(params)
    # file_name = "test"
    # ma.get_items(FILENAME=file_name)
    ma.get_ima_items()
    #ma.get_all_items()
    #ma.get_select_fields_items()
    #ma.get_filtered_items()
    #ma.get_omit_fields_items()
    #ma.get_ima_items()
