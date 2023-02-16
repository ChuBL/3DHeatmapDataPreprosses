# 3D Heat Map Data Preprocess
This project is about retrieving mineral data from OpenMindat API and cleansing the data into our designed data structure for the 3D heat map to analyze co-relationships between minerals and elements.

## Get Started
### Prerequisite 
You will need an **API key** text file in the root path of your cloned repository to run the codes. The **API key** will not be included in this repository. Please reach out to Mindat administrators for help.

### Run the code
The whole data stream is wrapped in `mindat_data_processor.py`. You can walk through all the steps from data retrieving to data export by running this single `.py` file.

## File structures

### Data Description
The retrieved data are saved in `./mindat_data/raw_data`, in the name format of `mindat_items_IMA_00000000000000.json`.

The exported CSV files are saved in `./mindat_data/csv/`
Under this directory we provided 8  generated datasets derived from OpenMindat IMA-approved mineral species.

#### Subset 30 Common Elements Datasets
- `30_elements.csv` Elements cooccurrence 3D matrix, comprises of as a concatenated 2D matrices of **top 30 common** elements in Mindat attribute `elements`.

- `30_sigelements.csv` Elements cooccurrence 3D matrix, comprises of as a concatenated 2D matrices of **top 30 common elements** in Mindat attribute `sigelements`.

- `normalized_30_elements.csv` *Normalized* elements cooccurrence 3D matrix, comprises of as a concatenated 2D matrices of **top 30 common elements** in Mindat attribute `elements`.

- `normalized_30_sigelements.csv` *Normalized* elements cooccurrence 3D matrix, comprises of as a concatenated 2D matrices of **top 30 common elements** in Mindat attribute `sigelements`.

#### All Elements Datasets
- `all_elements.csv` Elements cooccurrence 3D matrix, comprises of as a concatenated 2D matrices of **all elements** in Mindat attribute `elements`.

- `all_sigelements.csv` Elements cooccurrence 3D matrix, comprises of as a concatenated 2D matrices of **all elements** in Mindat attribute `sigelements`.

- `normalized_all_elements.csv` *Normalized* elements cooccurrence 3D matrix, comprises of as a concatenated 2D matrices of **all elements** in Mindat attribute `elements`.

- `normalized_all_sigelements.csv` *Normalized* elements cooccurrence 3D matrix, comprises of as a concatenated 2D matrices of **all elements** in Mindat attribute `sigelements`.

### Auxiliary code

#### Data retrieving
`mindat_api.py` for retrieving data from Mindat api.

#### Csv Normalization

`csv_normalizer.py` for generating normalized version of the cleaned CSV file.