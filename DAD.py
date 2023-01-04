#Required Modules
import pandas as pd
import streamlit as st
import numpy as np
from PIL import Image
from datetime import datetime
import sqlalchemy
from sqlalchemy import create_engine


st.set_page_config(page_title="DAD", page_icon="tata-icon (1).png",
                   layout="wide", initial_sidebar_state="expanded")


st.subheader("Data Anomaly Detector")

name = st.text_input("Enter your name ")

if not name:
  st.warning("Please fill out so required fields")

# PTX Anamoly Detector Module
ptx_columns = ["Date", "Shift", "Band 2D Barcode", "list of NG FAI's", "CNC-4 Dot-Matrix", "CNC-4", "CNC-4 Machining Date", "CNC-5-1 Dot-Matrix", "CNC-5-1", "CNC-5-1 Machining Date",
               "CNC-5-2 Dot-Matrix", "CNC-5-1.1", "CNC-5-2 Machining Date", "CNC-6 Dot-Matrix", "CNC-6", "CNC-6 Machining Date", "IM Dot-Matrix", "IM1 Cavity", "IM1 Mould", "IM2 Cavity", "IM2 Mould"]

ptx_columns_number = 21

data_file_name = st.sidebar.selectbox('Select the Name of the Data File', ['PTX', 'Cosmetics'])

if data_file_name == 'PTX':
    file_uploaded = st.file_uploader("Upload Dataset"+ data_file_name, type=["csv", "xlsx", "xls"])

    if file_uploaded is not None:
        st.success('File Uploaded Successfully!')
        input_df = pd.read_csv(file_uploaded)   

        # Performing Minimal Data Cleaning
        input_df.dropna(how = 'all', axis = 0, inplace = True)

        # Checking Column Count in Uploaded File
        if len(input_df.columns) == ptx_columns_number:
            st.write('Requied Column Count: '+ str(ptx_columns_number),icon =  '✅')
            st.write('Uploaded Column Count:'+ str(len(input_df.columns)))
            st.info('Column Count is matching with uploaded file')
        else:
            st.write('Requied Column Count: '+str(ptx_columns_number), icon = '✅')
            st.write('Uploaded Column Count: '+str(len(input_df.columns)))
            st.info('Column Count is not matching')

        for col in ptx_columns:
            if col in input_df.columns:
                print(col + ' ---> Column Availble')
            else:
                st.write(col +' ---> Column not Available')

        new_columns = []

        if np.nan in list(input_df['Date'].unique()):
            st.error('Repeated Data Columns/Found Null/None/Blank in Data Columns', icon="🚨")

        for col in input_df.columns:
            if col not in ptx_columns:
                new_columns.append(col)
                # st.write(col+'is not in the list')
        st.markdown("Below columns are not in the given list")
        new_columns

        file_details = {"Filename": file_uploaded.name,
                    "FileType": file_uploaded.type, "FileSize": file_uploaded.size}

        filename = file_details["Filename"]

        filetype = file_details['FileType']
       
        current_dateTime = datetime.now()
        
        df_data = [name,filename,filetype,current_dateTime,len(input_df.columns)]
        

        # df_data = pd.DataFrame()
        # df = df.append({'Name':name},ignore_index = True)
        # df = df.append({"Filename":filename},ignore_index = True)
        # df = df.append({"FileType":filetype },ignore_index = True)
        # df_data.append(df_data, ignore_index=True)

        df_cols = ['Name', 'Filename' , 'Filetype','Date & Time','Column_Count']
        
        new_df =pd.DataFrame(columns = df_cols)

        # using the loc indexer
        new_df.loc[0] = df_data

        new_df

        DB = {'servername': 'DESKTOP-GARLJAI\SQLEXPRESS',
            'database': 'DATA',
            'driver': 'driver=ODBC Driver 17 for SQL Server'}

          # create the connection
        engine = create_engine(
           'mssql+pyodbc://' + DB['servername'] + '/' + DB['database'] + "?" + DB['driver'])

        data2 = new_df.to_sql(
                'DAD', con=engine, index=False, if_exists='append')

        if len(input_df.columns) == ptx_columns_number:

            st.download_button(label='Download csv',
                           data=new_df.to_csv(), mime='text/csv')
        else:
            st.warning('Columns not matching', icon="⚠️")
        
