"""GHCN-DAILY Station Data Preprocessing

Author: Swun Wunna Htet (Mar 2025)

"""
# importing the libraries to use
import numpy as np
import pandas as pd
import os

def readDLYfile(filename):
    """
    This function will read DLY files of GHCN-daily stations as unformatted pandas dataframe.
    
    Args:
        filename (str): station measurement with .dly file format.
    """

    # creating the column specifications based on GHCN readme.txt
    generic = [(0,11), # ID (character)
                (11,15), # Year (integer)
                (15,17), # month (integer)
                (17,21), # Parameter 
                ]

    # automatically creating DOY specifications based on readme.txt
    # these spaces are defined based on requirement of Pandas's open list nature and appending to the generic list
    for i in range(22,270, 8):
        x = i-1
        y = i+4

        val = (x,y)
        mflag = (y,y+1)
        qflag = (y+1,y+2)
        sflag = (y+2,y+3)

        generic.append(val)
        generic.append(mflag)
        generic.append(qflag)
        generic.append(sflag)

    # creating the column names based on the existing unique columns of station data
    names = ['ID', 'YEAR', 'MONTH', 'ELEMENT']

    for i in range(1,32):
        
        names.append('VALUE'+str(i))
        names.append('MFLAG'+str(i))
        names.append('QFLAG'+str(i))
        names.append('SFLAG'+str(i))

    # check the total elements of generic and column names. MUST BE THE SAME.
    flag = len(names) == len(generic)

    # raise error when the generic column names and columns are different.
    if flag:
        # combining two lists to read as data frame
        main= pd.read_fwf(filename, colspecs = generic, names = names)
    else:
        print('Number of Generic Column Names and Column unique names are different')
    
    
    return main

def createNewDataframe(raw_dataf, parameters = []):
    """
    Create a time-formatted skeletal pandas dataframe for GHCN-daily station data to substitute.
    
    Args:
        raw_dataf(Pandas DataFrame): unformatted dataframe (obtained from readDLYfile function).
        
    Return:
        
    """
    avail_elements = ['PRCP', 'SNOW', 'SNWD', 'TMAX', 'TMIN', 'ACMC', 'ACMH', 'ACSC', 'ADPT', 'ASLP',
                      'ASTP', 'AWBT', 'AWDR', 'AWND', 'DAEV', 'DAPR', 'DASF', 'DATN', 'DATX', 'DAWM', 
                      'DWPR', 'EVAP', 'FMTM', 'FRGB', 'FRGT', 'FRTH', 'GAHT', 'MDEV', 'MDPR', 'MDSF', 
                      'MDTN', 'MDTX', 'MDWM', 'MNPN', 'PGTM', 'PSUN', 'RHAV', 'RHMN', 'RHMX', 'SN01',
                      'SN01','SN02','SN03','SN04','SN05','SN06','SN07','SN11','SN12','SN13','SN14', 
                      'SN15','SN16','SN17','SN21','SN22','SN23','SN24','SN25','SN26','SN27','SN31',
                      'SN32', 'SN33','SN034','SN35','SN36','SN37','SN41','SN42','SN43','SN44','SN45',
                      'SN46', 'SN47','SN51','SN52','SN53','SN54','SN55','SN56','SN57','SN61','SN62',
                      'SN63', 'SN64', 'SN65','SN66','SN67','SN71','SN72','SN73','SN74','SN75','SN76',
                      'SN77','SN81', 'SX05','SX06','SX07','SX11','SX12','SX13','SX14', 'SX15','SX16',
                      'SX17','SX21','SX22','SX23','SX24','SX25','SX26','SX27','SX31','SX32', 'SX33',
                      'SX034','SX35','SX36','SX37','SX41','SX42','SX43','SX44','SX45','SX46', 'SX47',
                      'SX51','SX52','SX53','SX54','SX55','SX56','SX57','SX61','SX62','SX63','SX64',
                      'SX65','SX66','SX67','SX71','SX72','SX73','SX74','SX75','SX76','SX77','SX81', 
                      'SX82','SX83','SX84','SX85','SX86','SX87','TAXN','TAVG','THIC','TOBS', 'TSUN',
                      'WDF1', 'WDF2', 'WDF5', 'WDFG', 'WDFI', 'WDFM', 'WDMV', 'WESD', 'WESF', 'WSF1',
                      'WSF2', 'WSF5', 'WSFG', 'WSFI', 'WSFM', 'WT01', 'WT02', 'WT03', 'WT04', 'WT05',
                      'WT06', 'WT07', 'WT08', 'WT09', 'WT10', 'WT11', 'WT12', 'WT13', 'WT14', 'WT15',
                      'WT16', 'WT17', 'WT18', 'WT19', 'WT20', 'WT21', 'WT22', 'WV01', 'WV03', 'WV07',
                      'WV18', 'WV20']
    df = raw_dataf.copy()

    """If parameter list to process is provided, the list is cross-checked with the default GHCN available
    Elements. If not provided, the function will collect all elements."""
    if len(parameters)<=0:
        avail_params = np.unique(df['ELEMENT']).tolist()
    else:
        # list checking
        avail_params = []
        for i in parameters:
            if i in avail_elements:
                avail_params.append(i)
            else:
                print(f'{i} not in GHCN-Daily element list. {i} skipped')

    qlty_lst = ['QFLAG', 'MFLAG', 'SFLAG']

    dataframes = []

    for i in range(len(avail_params)):
        columns = [avail_params[i]]+qlty_lst

        # from the raw data, extract the top and bottom row's month and year. Remember, any year
        # less than YEAR 1200 will not be able to extract because of UNIX time limit.
        top_month =  df['MONTH'][0]
        top_year = np.min(df['YEAR'])

        bottom_month = df['MONTH'][len(df['MONTH'])-1]
        bottom_year =  np.max(df['YEAR'])

        month31 = [1, 3, 5, 7, 8, 10, 12]
        month30 = [4, 6, 9, 11]

        if top_month in month31:
            top_day = 31
        elif top_month in month30:
            top_day = 30
        else:
            if top_month ==2:
                # If February
                if top_year % 4 == 0:
                    top_day = 29
                else:
                    top_day = 28

        if bottom_month in month31:
            bottom_day = 31
        elif bottom_month in month30:
            bottom_day = 30
        else:
            if bottom_month ==2:
                # If February
                if bottom_year % 4 == 0:
                    bottom_day = 29
                else:
                    bottom_day = 28

        processed_columnnames = ['ID','DATE']+columns

        processed_df = pd.DataFrame(columns= processed_columnnames)

        processed_df['DATE'] = pd.date_range(start = str(top_year)+'-'+str(top_month)+'-'+str(top_day),
                                        end = str(bottom_year)+'-'+str(bottom_month)+ '-'+str(bottom_day))

        processed_df['ID'] = np.unique(df['ID'])[0]
        
        dataframes.append(processed_df)

    return dataframes

def formatDLYdata(raw_df, empty_df):

    # copying the dataframes (input and output)
    main = raw_df.copy()
    output = empty_df.copy()

    output_dataframe = []

    # loop for each row of output dataframe columns. For each row, we will fill up the corresponding values of
    # parameterization to their corresponding
    for i in range(len(empty_df)):

        output_df = empty_df[i]
        omitcolumns = ['ID', 'DATE', 'QFLAG', 'MFLAG', 'SFLAG']
        unique_ID = [x for x in output_df.columns.tolist() if x not in omitcolumns][0]

        para_list = []
        qflag_lst = []
        mflag_lst = []
        sflag_lst = []

        for j in range(output_df.shape[0]):

            # day, month and year extraction from the output data
            dy = output_df['DATE'][j].day
            mth = output_df['DATE'][j].month
            yr = output_df['DATE'][j].year

            # get the Column names to extract parameters and their quality flags of each respective date.
            para_val_col = 'VALUE'+str(dy)
            qflag_col = 'QFLAG'+str(dy)
            mflag_col = 'MFLAG'+str(dy)
            sflag_col = 'SFLAG'+str(dy)

            # another loop will enter. This extract automatically the respective parameters' values
            # Row for respective month of year with multiple parameters.
            # print(unique_ID)
            row = main.loc[(main['YEAR'] == yr) & (main['MONTH'] == mth) & (main['ELEMENT'] == unique_ID)]

            if len(row) == 0:
                para_val = -99
                qflag_val = -99
                mflag_val = -99
                sflag_val = -99
            else:
                para_val = row[para_val_col].to_numpy()[0]
                qflag_val = row[qflag_col].to_numpy()[0]
                mflag_val = row[mflag_col].to_numpy()[0]
                sflag_val = row[sflag_col].to_numpy()[0]
            
            para_list.append(para_val)
            qflag_lst.append(qflag_val)
            mflag_lst.append(mflag_val)
            sflag_lst.append(sflag_val)
        
        output_df[unique_ID] = para_list
        output_df['QFLAG'] = qflag_lst
        output_df['MFLAG'] = mflag_lst
        output_df['SFLAG'] = sflag_lst

        output_dataframe.append(output_df)

    return output_dataframe

def exportDFtoExcel(major_path, all_dataframes):
    """Exporting all the specific parameter's dataframe into workable excel sheet.
    For each pandas dataframe, the file names are uniquely combined with Station ID 
    with major parameter name
    
    major_path (String): Specify the major file path to save all parameters' excel sheet.
    all_dataframe(List): A python list containing all the pandas dataframes
    """

    mjr_pth = major_path

    stationID = all_dataframes[0]['ID'][0]

    folder_path = mjr_pth+r'/'+stationID

    os.makedirs(mjr_pth+r'/{}/'.format(stationID), exist_ok = True)
    print('{} folder created successfully'.format(stationID))

    for i in range(len(all_dataframes)):

        columns = all_dataframes[i].columns.tolist()
        mjr_para_name = [x for x in columns if x not in ['ID', 'DATE', 'QFLAG', 'MFLAG', 'SFLAG']][0]

        writer = pd.ExcelWriter(folder_path+r'/'+stationID+'_'+mjr_para_name+'.xlsx', engine = 'openpyxl')

        all_dataframes[i].to_excel(writer, sheet_name = mjr_para_name)
        writer.close()
        print('   {} completed'.format(mjr_para_name))