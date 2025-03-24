# Table of Contents
- [Python Dependencies Requirement](#python-dependencies-requirements)
- [Function Description](#function-description)

# Python Dependencies Requirements

The v1.0 ghcnsnowprocess requires the following dependencies.

1. NumPy (1.26.3 or newer)
2. Pandas (2.1.4 or newer)
3. os
4. openpyxl (3.1.2 or newer)
5. Xlsxwriter (3.2.0 or newer)

# Function Description

## `readDLYfile(filename)`

This function will read DLY files form the GHCN-Daily stations as unformatted pandas dataframe.

_Arguments:_

filename (string): Full directory of GHCN-Daily station measurements with .DLY file format.

_Return:_

`main` (Pandas DataFrame): Gives a column-unformatted raw data of GHCN-daily data.

___

## `createNewDataframe(raw_dataf, parameters = [])`

This function uses output from `readDLYfile` function to recreate a time-formatted skeletal pandas dataframe for each element available in raw data.

_Arguments:_

`raw_dataf` (Pandas Dataframe): Dataframe obtained from `readDLYfile` function.

`parameters` (list): A list of variable elements (stated by GHCN-Daily file format description). By **default** as an empty list, the function will produce all the available elements in the raw data file. If users provide the list of elements to process, the function will check whether each element is in the list. **If an element exists**, the processing is done. Otherwise, the function will alert the users that an unavailable element will be skipped.

_Return:_

`Parameters` (list): a python list of element-specific, column and time-formatted pandas dataframes.

_____

## `formatDLYdata(raw_df, empty_df)`

_Arguments:_

`raw_df` (Pandas Dataframe): a raw data obtained from `readDLYfile` function.

`empty_df` (List): a list of empty dataframes for each element obtained from `createNewDataframe` function.

_Return:_

`formatted_dfs` (List): a list of parameter-specific, column and time-formatted dataframes with values extracted from GHCN-Daily data. The number of dataframes is equal to the number of provided elements to process in `empty_df`. 

___

## `exportDFtoExcel(major_path, all_dataframes)`

_Arguments:_

`major_path` (string): The full file path to save all the parameters' dataframes as excel sheets.

`all_dataframes` (List): a python list containing all the pandas dataframes with all corresponding elements.

_Return:_
All outputs from `all_dataframes` will be exported to the desired `major_path` as excel sheet as xlsx format.

___



