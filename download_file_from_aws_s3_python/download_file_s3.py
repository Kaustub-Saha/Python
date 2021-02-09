import os
import boto3
import sys
from datetime import datetime as dt
import io

#we have placed a file with environment and other details in a ebnironment file in a particular location
sys.path.append(r"C:\Users\kaustub.saha\Desktop\itc")
import ENV


print('Script Execution started at ', dt.now())
#assigning variables from ENV
a_key = ENV.a_key
s_key = ENV.s_key
bucket = ENV.bucket #specifying the bucket from which the download needs to be done
folder = ENV.folder #specifying the folder inside bucket from where we need to download
download_path = ENV.download_path #Specifying the local system where the download with happen

#declaring global variables
fname_to_dwnld = []
itc_fpath = '' 
itc_fname = ''

def download_file_s3():
    print('File download from S3 started at ', dt.now())
	  #refering the global variables within the function
    global bucket,folder,itc_fname,download_path
    client = boto3.client('s3',aws_access_key_id = a_key,aws_secret_access_key = s_key)
    object_to_dwnld = ''
    fname_to_dwnld = '' #nameof the file that will be downloaded
    dwnld_file_path = ''
    bucket_name = bucket
    object_key = folder
    f= list() #variable to store the filenames
	
	  #fetching all the content of the bucket, we receive this information as a dictionary of lists
    Bucket_content = client.list_objects(Bucket=bucket_name, Prefix=object_key)
    #performing list and list slicing to fetch the file name
    list_obj = Bucket_content.get('Contents')
    for list_item in list_obj:
		#key holds the name of the file and folders in the bucket
        f.append(list_item.get('Key'))
    #There could be multiple f and folders, but the way I designed my use case, 
	  #I needed to download only one file thus hardcoding the value to 1
    object_to_dwnld = f[1] 
	
	  #fetching the exact filename by separating it out from its parent directory name
    f = f[1].split("/")
    fname_to_dwnld = f[1]
    print(fname_to_dwnld)
    dwnld_file_path = download_path+fname_to_dwnld
    print(dwnld_file_path)
	
	  #This download_file option downloads the file from the S3 bucket
    client.download_file(bucket,object_to_dwnld,dwnld_file_path)
    print('File download from S3 finished at ', dt.now())        
    return(dwnld_file_path,fname_to_dwnld)
    
if __name__=="__main__":
    #filepath and filena
    itc_filepath,itc_filename = download_file_s3()
