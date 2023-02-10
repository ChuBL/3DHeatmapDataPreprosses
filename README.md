# 3DHeatmapDataPreprosses
This project is about retrieving mineral data from OpenMindat API, and cleansing the data into our designed data structure to the 3D Heatmap of mineral element coexistence.

## Get Started
### Prerequisite 
You will need an **API key** text file in the root path of your cloned repository to run the codes. The **API key** will not included in this repository. Please reach out for Mindat administrators for help.

### Run the code
The whole data stream is wrapped in `mindat_data_processor.py`. You can walk through all the steps from data retrieving to data export by run this single `.py` file.

### Auxiliary code

#### `mindat_api.py`
Retrieving data from mindat api.

#### `csv_normalizer.py`
Generate normalized version of cleaned CSV file.

### Data Description
The retrieved data are saved in `./mindat_data/`, in the name format of `mindat_items_IMA_00000000000000.json`.

The exported CSV files are saved in `./mindat_data/csv/`
