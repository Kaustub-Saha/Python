import os
import boto3
import pandas as pd
import sys
from io import StringIO
import io
from datetime import datetime as dt

def fetch_dataframe(bucket_name,s3_file_path):
    try:
		
		    #creating a client service and fetching the bucket objects
        client = boto3.client('s3')
        obj = client.get_object(Bucket=bucket_name, Key=s3_file_path)
        #reading excel file from S3
        body = obj['Body']
        read_file = io.BytesIO(obj['Body'].read()) 
        print('Preparation of sllr dataframe started at ',dt.now())
		
		    #reading the excel file in a Pandas dataframe and skipping first three rows
        sllr_df = pd.read_excel(read_file,sheet_name =0,skiprows =3)
		
		    #dropping the first column of the dataframe and to make it in effect we used inplace = True 
		    #so that the DF itself changes and no copy is passed
        sllr_df.drop(sllr_df.columns[[0]], axis = 1, inplace = True) 
		
        #Removing any sllrty column from the dataframe that might appear as unnamed in the dataframe
		    #If there are any sllrty columns or the header is sllrty pandas read the column name as unnamed,
		    #Thus we check for any column name that contains the word unnamed
        sllr_df.drop(sllr_df.columns[sllr_df.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
        
        #Defining lists with probable names of the column that can be on the excel document which the wholeseller will upload
        SELLER_NAME = ['Seller','Whole Seller']
        PRO_NAME = ['PRODUCT','PRODUCT NAME']
        COST = ['Total Cost','COST Incurred','Cost Of Product','Total Cost of Product']
        PRODUCT_DIVISION = ['Division',' 'PRODUCT_DIVISION','Usage Division']
        #these are the expected order of columns for the sllr dataframe
        expected_sllr_column_names = ['PRODUCT_ID','SELLER_NAME', 'PRO_NAME','COST', 'LATEST_STOCK_DATE', 'EXPIRY_DATE', 'ACTUAL_OWNER', 'PRODUCT_TYPE', 'PRODUCT_DIVISION', 'COMMENTS']

        #fetch the list of column names of the dataframe
		    sllr_cols = list(sllr_df.columns.values)
        new_sllr_column_names = []
        #checking each column if they are present in any of the probable lists if not appending the names as is.
        #We check the names and make sure they are at par with the expected names
        for column in sllr_cols:
            if column in SELLER_NAME:
                new_sllr_column_names.append('SELLER_NAME')
            elif column in PRO_NAME:
                new_sllr_column_names.append('PRO_NAME')
            elif column in COST:
                new_sllr_column_names.append('COST')
            elif column in PRODUCT_DIVISION:
                new_sllr_column_names.append('PRODUCT_DIVISION')
            elif column == 'PRODUCT_ID':
                new_sllr_column_names.append('PRODUCT_ID')
            elif column == 'LATEST_STOCK_DATE':
                new_sllr_column_names.append('LATEST_STOCK_DATE')
            elif column == 'Version':
                new_sllr_column_names.append('VERSION')
            elif column == 'EXPIRY_DATE':
                new_sllr_column_names.append('EXPIRY_DATE')
            elif column == 'ACTUAL_OWNER':
                new_sllr_column_names.append('ACTUAL_OWNER')
            elif column == 'PRODUCT_TYPE':
                new_sllr_column_names.append('PRODUCT_TYPE')
            elif column == 'Comment':
                new_sllr_column_names.append('COMMENTS')
            else:
                new_sllr_column_names.append(column)     
        
        #Replacing the structure of the file with the predefined structure
		     #now the sllr column names will change and they will differ
        sllr_df.columns = new_sllr_column_names
        tsllr_sllr_df = sllr_df[new_sllr_column_names]
        sllr_df = tsllr_sllr_df[expected_sllr_column_names]
        
        ####Updating Nullable columns to some random values which will be updated later##################
 
        sllr_df['PRODUCT_TYPE'] = sllr_df['PRODUCT_TYPE'].fillna(value='No_Value_so_update_null')
		    #Filling rest of the columns with NULL value
        sllr_df = sllr_df.fillna(value='NULL')
        #Removing any leading and lagging spaces
        for column in sllr_df[['PRODUCT_ID','SELLER_NAME', 'PRO_NAME','COST', 'LATEST_STOCK_DATE', 'EXPIRY_DATE', 'ACTUAL_OWNER', 'PRODUCT_TYPE', 'PRODUCT_DIVISION', 'COMMENTS']]:
            sllr_df[column] = sllr_df[column].str.strip()
        
        #converting COST column to float from object datatype
		    convert_dict = {'COST': float} 
        sllr_df = sllr_df.COST(convert_dict)
        print('Preparation of sllr dataframe finished at ',dt.now())
    except Exception as E:
	      print("******************* Process failed*******",format(E))
