import pandas as pd
import os
from pathlib import Path
import sys

class CsvNormalizer:
    # 72 list
    # ALL_ELEMENT_LIST = ['H', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Na', 'Mg', 'Al', 'Si', 'P', 'S',\
    #     'Cl', 'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge',\
    #         'As', 'Se', 'Br', 'Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd',\
    #             'In', 'Sn', 'Sb', 'Te', 'I', 'Cs', 'Ba', 'La', 'Ce', 'Nd', 'Sm', 'Gd', 'Dy', 'Er',\
    #                 'Yb', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Th', 'U']

    # 73 list
    ALL_ELEMENT_LIST = ['H', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Na', 'Mg', 'Al', 'Si', 'P', 'S',\
        'Cl', 'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge',\
            'As', 'Se', 'Br', 'Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd',\
                'In', 'Sn', 'Sb', 'Te', 'I', 'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd', 'Sm', 'Gd', 'Dy', 'Er',\
                    'Yb', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Th', 'U']

    THIRTY_ELEMENT_LIST = ['H', 'B', 'C', 'O', 'F', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'K', 'Ca', \
        'Ti', 'V', 'Mn', 'Fe', 'Ni', 'Cu', 'Zn', 'As', 'Se', 'Ag', 'Sb', 'Ba', 'Pb', 'Bi', 'U', 'REE']

    def __init__(self):
        self.csv_path = './mindat_data/csv/'

    def read_csv(self, CSV_FILENAME):
        csv_path = self.csv_path + CSV_FILENAME
        df = pd.read_csv(csv_path)
        return df

    def normalizing_df(self, DATAFRAME, ELE_COUNT):
        if (len(CsvNormalizer.ALL_ELEMENT_LIST) == int(ELE_COUNT)):
            target_element_list = CsvNormalizer.ALL_ELEMENT_LIST
        elif (len(CsvNormalizer.THIRTY_ELEMENT_LIST) == int(ELE_COUNT)):
            target_element_list = CsvNormalizer.THIRTY_ELEMENT_LIST
        else:
            print("ELEMENT_COUNT error")
            sys.exit()

        df = DATAFRAME
        for index, element in enumerate(target_element_list):
            try:
                base_number = df.iloc[(ELE_COUNT + 1) * index, index + 2]
                if 0 == base_number:
                    # print(((ELE_COUNT + 1) * index, index + 2))
                    continue
            except IndexError:
                break

            for x in range(ELE_COUNT * index, ELE_COUNT * (index + 1)):
                for y in range(2, ELE_COUNT +2):
                    df.iloc[x, y] = df.iloc[x, y] / base_number
        return df
        

    def save_normalized_csv(self, FILENAME):
        df = self.read_csv(FILENAME)
        element_count = int(FILENAME.split("_")[0])
        df = self.normalizing_df(df, element_count)
        df.to_csv(self.csv_path + 'normalized_' + FILENAME, index = False)

    def batch_normalizing(self):
        print("Start nomalizing csv files")
        for filename in os.listdir(self.csv_path):
            if "normalized_" in filename:
                continue
            if "csv" in filename:
                print("Normalizing " + filename)
                self.save_normalized_csv(filename)
        print("Normalization finished.")

if __name__ == "__main__":
    cn = CsvNormalizer()
    cn.batch_normalizing()