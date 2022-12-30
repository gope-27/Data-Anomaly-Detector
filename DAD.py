import pandas as pd
import streamlit as st
import numpy as np
from datetime import datetime
st.header('UPLOAD YOUR FILE')
sample_file = st.file_uploader('Upload the CSv file')
if sample_file is not None:
    data_file = pd.read_excel(sample_file)
    st.dataframe(data_file)
    obtained_columns = list(data_file.columns)
    requiredCols = ["Band 2D Barcode", "Work Order","Station", "Date & Time", "Shift", "Batch", "Inspector", "Line No.", "Status", "Defect", "Grade", "Locations"]
    fail_flag = 0
    for i in requiredCols:
        if str(i) not in obtained_columns:
            fail_flag = 1
            st.write("Missed column name:", i)
    if fail_flag != 1:
        st.write("All the columns are present \n",requiredCols)
    masterConcat = pd.DataFrame()
    df =  data_file[requiredCols]
    masterConcat = pd.concat([masterConcat, df])
    masterConcat['REASONFORFAILURE'] = np.nan
    masterConcat['LOAD_DATE']  = datetime.now()
    new_id = 0
    masterConcat['LOAD_IDENTIFIER'] = new_id
    dic_dtypes=masterConcat.dtypes.apply(lambda x: x.name).to_dict()
    req_dtypes ={'Band 2D Barcode': 'object',
    'Work Order': 'object',
    'Station': 'object',
    'Date & Time': 'datetime64[ns]',
    'Shift': 'float64',
    'Batch': 'object',
    'Inspector': 'object',
    'Line No.': 'object',
    'Status': 'object',
    'Defect': 'object',
    'Grade': 'object',
    'Locations': 'object',
    'REASONFORFAILURE': 'object',
    'LOAD_DATE': 'datetime64[ns]',
    'LOAD_IDENTIFIER': 'int64'}
    req_keys =list(dic_dtypes.keys())
    for i in req_keys:
     if (dic_dtypes[i] == req_dtypes[i]):
        continue
        #print(i,'column has proper datatype')
     else:
         st.write(i,'column has wrong datatype')