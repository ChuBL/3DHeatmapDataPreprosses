import re
import json
from pathlib import Path
import os
import numpy as np
import pandas as pd
import sys
from csv_normalizer import CsvNormalizer
from mindat_api import MindatApi
import copy

class MindatDataProcessor:
    ALL_ELEMENT_LIST = ['H', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Na', 'Mg', 'Al', 'Si', 'P', 'S',\
        'Cl', 'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge',\
            'As', 'Se', 'Br', 'Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd',\
                'In', 'Sn', 'Sb', 'Te', 'I', 'Cs', 'Ba', 'La', 'Ce', 'Nd', 'Sm', 'Gd', 'Dy', 'Er',\
                    'Yb', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Th', 'U']
    THIRTY_ELEMENT_LIST = ['H', 'B', 'C', 'O', 'F', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'K', 'Ca', \
        'Ti', 'V', 'Mn', 'Fe', 'Ni', 'Cu', 'Zn', 'As', 'Se', 'Ag', 'Sb', 'Ba', 'Pb', 'Bi', 'U', 'REE']
    REE_LIST = ['Sc', 'Y', 'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu']
    
    def __init__(self):
        self.data_file_path = "./mindat_data/"
        self.all_element_list = MindatDataProcessor.ALL_ELEMENT_LIST
        self.thirty_element_list = MindatDataProcessor.THIRTY_ELEMENT_LIST
        self.ree_list = MindatDataProcessor.REE_LIST

        # Step 1. get the latest mindat data.
        # self.update_mindat_data()
        
        # Step 2. cleansing the api data, generate csv files.
        # self.prepare_data()
        # self.export_csv()

        # Step 3. generate normalized csv files, based on the results of step 2.
        # get_normalized_csv()

        # Or you can run all the steps at once.
        # self.run_data_preprocess()

    def run_data_preprocess(self):
        self.update_mindat_data()

        self.prepare_data()
        self.export_csv()
        
        self.get_normalized_csv()

    def update_mindat_data(self):
        mindat_api = MindatApi('api_key.txt')
        mindat_api.get_ima_items()
    
    def prepare_data(self):
        self.mindat_json = self._load_mindat_data()
        for element in self.all_element_list:
            self.prep_element_json(element, 'elements', 72)
            self.prep_element_json(element, 'sigelements', 72)
        
        for element in self.thirty_element_list:
            self.prep_element_json(element, 'elements', 30)
            self.prep_element_json(element, 'sigelements', 30)

    def export_csv(self):
        self.batch_convert_json_to_csv(self.thirty_element_list, 'sigelements')
        self.batch_convert_json_to_csv(self.thirty_element_list, 'elements')

        self.batch_convert_json_to_csv(self.all_element_list, 'sigelements')
        self.batch_convert_json_to_csv(self.all_element_list, 'elements')


    def get_normalized_csv(self):
        cn = CsvNormalizer()
        cn.batch_normalizing()


    def _load_mindat_data(self):
        up_to_date = 0
        # iterate over the directory and return the file names
        for filename in os.listdir(self.data_file_path):
            if "mindat_items_IMA" in filename:
                data_date = int(re.findall(r'(?<=_)\d+(?=\.json)', filename)[0])
                if data_date > up_to_date:
                    up_to_date = data_date
                    up_to_date_file = filename
                #data_date = filename.split("_")[3]

        mindat_path = self.data_file_path + up_to_date_file
        with open(mindat_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        return json_data


    def prep_element_json(self, ELEMENT_NAME, ELEMENT_ATTRIBUTE, ELEMENT_COUNT):
        # ELEMENT_NAME is selected from self.30elements, including REE
        if ('72' == str(ELEMENT_COUNT)):
            df = self.initialize_df(self.all_element_list)
        elif ('30' == str(ELEMENT_COUNT)):
            df = self.initialize_df(self.thirty_element_list)
        else:
            print("ELEMENT_COUNT error")
            sys.exit()

        for item in self.mindat_json["results"]:
            element_attribute_list = self.get_item_element_attributes(item, ELEMENT_ATTRIBUTE)
            if ('30' == str(ELEMENT_COUNT)):
                element_attribute_list = self.convert_to_list_with_ree(element_attribute_list)
            if ELEMENT_NAME in element_attribute_list:
                df = self.load_list_to_frame(element_attribute_list, df, ELEMENT_COUNT)
                      
        export_path = Path(self.data_file_path, str(ELEMENT_COUNT), ELEMENT_ATTRIBUTE)
        export_path.mkdir(parents=True, exist_ok=True)
        export_file = os.path.join(export_path, ELEMENT_NAME + "_" + str(ELEMENT_COUNT) + "_mindat.json")
        with open(export_file, 'w', encoding='utf-8') as f:
            json.dump(df, f, indent=4)


    def load_list_to_frame(self, CONVERTED_LIST, DATAFRAME, ELEMENT_COUNT):
        if ('72' == str(ELEMENT_COUNT)):
            target_element_list = self.all_element_list
        elif ('30' == str(ELEMENT_COUNT)):
            target_element_list = self.thirty_element_list
        else:
            print("ELEMENT_COUNT error")
            sys.exit()

        remaining_elements = CONVERTED_LIST.copy()
        df = DATAFRAME

        for x in CONVERTED_LIST:
            remaining_elements.remove(x)
            if x not in target_element_list:
                continue
            else:
                df["with"][x][x] += 1
        
            for y in remaining_elements:
                if y not in target_element_list:
                    continue
                else:
                    df["with"][x][y] += 1 
        
        return df


    def initialize_df(self, ELEMENT_LIST):
        df = {"with": {}}
        for i, x in enumerate(ELEMENT_LIST):
            df["with"][x] = {}
            for y in ELEMENT_LIST[i:]:
                df["with"][x][y] = 0
        return df


    def convert_to_list_with_ree(self, ELEMENT_LIST):
        converted_element_list = []
        is_ree = False
        for element in ELEMENT_LIST:
            if element not in self.ree_list:
                converted_element_list.append(element)
            else:
                is_ree = True
        
        if True == is_ree:
            converted_element_list.append("REE")
        return converted_element_list


    def get_item_element_attributes(self, item, ELEMENT_KEY):
        ele_attr_list = item[ELEMENT_KEY].split("-")
        ele_attr_list = [e for e in ele_attr_list if e in self.all_element_list]
        ele_attr_list = sorted(ele_attr_list, key=lambda x: self.all_element_list.index(x))
        return ele_attr_list


    def get_element_pair(self, JSONDATA, ELEMENT_I, ELEMENT_J):
        if ELEMENT_I not in JSONDATA['with'].keys():
            return 0
        if ELEMENT_J not in JSONDATA['with'][ELEMENT_I].keys():
            return 0
        return JSONDATA['with'][ELEMENT_I][ELEMENT_J]


    def make_flip(self, dataframe):
        for i in range(len(dataframe.columns)):
            for j in range(len(dataframe.index)):
                if i > j:
                   dataframe.iloc[i, j] = dataframe.iloc[j, i]
        

    def insert_yaxis(self, dataframe):
        element_count = len(dataframe.columns)
        if (72 == element_count):
            target_element_list = self.all_element_list
        elif (30 == element_count):
            target_element_list = self.thirty_element_list
        else:
            print("ELEMENT_COUNT error")
            sys.exit()

        dataframe.insert(0, "yaxis", target_element_list, True)


    def insert_zaxis(self, dataframe):
        element_count = len(dataframe.index)
        zaxis = np.full(element_count, self.current_element, dtype=object)
        dataframe.insert(0, "zaxis", zaxis, True)


    def convert_json_to_df(self, ELEMENT_NAME, JSON_PATH):
        element_count = str(re.findall(r'(?<=\/)\d+(?=\/)', str(JSON_PATH))[0])
        if ('72' == element_count):
            target_element_list = self.all_element_list
        elif ('30' == element_count):
            target_element_list = self.thirty_element_list
        else:
            print("ELEMENT_COUNT error")
            sys.exit()

        self.current_element = ELEMENT_NAME
        # assert self.current_element in self.element_list
        file_path = Path(JSON_PATH, ELEMENT_NAME + '_' + element_count + '_mindat.json')
        with open(file_path, 'r') as f:
            jsondata = json.load(f)

        data = np.zeros((int(element_count), int(element_count)),dtype=int)
        df = pd.DataFrame(data, columns=target_element_list)

        for i, element_i in enumerate(target_element_list):
            for j, element_j in enumerate(target_element_list):
                pair_value = self.get_element_pair(jsondata, element_i, element_j)
                df.iloc[i][j] = pair_value
        
        self.make_flip(df)
        self.insert_yaxis(df)
        self.insert_zaxis(df)
        return df


    def batch_convert_json_to_csv(self, ELEMENT_LIST, ELEMENT_ATTRIBUTE):
        total_df = pd.DataFrame()
        element_count = len(ELEMENT_LIST)
        for index, element in enumerate(ELEMENT_LIST):
            print("Converting {}_mindat.json ... ({:.2f}%)".format(element, (index + 1)/len(ELEMENT_LIST)*100))
            json_path = Path(self.data_file_path, str(element_count), ELEMENT_ATTRIBUTE)
            current_df = self.convert_json_to_df(element, json_path)
            if total_df.empty:
                total_df = current_df
            else:
                total_df = self.concatenate_df(total_df, current_df)
        
        csv_ouput_path = Path(self.data_file_path, 'csv', str(element_count) + '_' + ELEMENT_ATTRIBUTE + '.csv')
        csv_ouput_path.parent.mkdir(parents=True, exist_ok=True)
        total_df.to_csv(csv_ouput_path, index=False)
        print("Output CSV file in: {}".format(csv_ouput_path))


    def concatenate_df(self, HEAD_DF, TAIL_DF):
        concatenated_df = pd.concat([HEAD_DF, TAIL_DF], ignore_index=True)
        return concatenated_df



if __name__ == "__main__":
   
    mdp = MindatDataProcessor()
    mdp.run_data_preprocess()
    # mdp.prepare_data()
    # mdp.export_csv()