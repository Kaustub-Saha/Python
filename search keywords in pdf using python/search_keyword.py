#using tika as it returns text as ordered in the pdf format
from tika import parser # pip install tika 
import re
import camelot #using Camelot to search keywords in tables
import os
from os import listdir
from os.path import isfile, join
import sys

#configuration details are stored in a separate file
sys.path.append (r'C:\Users\Administrator\Desktop\assignment\config')
import config

#This method checks the input directory and reads all the file in the directory
def read_input_file_path():
    input_path = config.input_path
    files_path = [os.path.join(input_path,f) for f in listdir(input_path) if isfile(join(input_path,f))]
    return files_path

#This method is used to write the output in a file
def write_output(learning_outcome,filename):
    output_path = config.output_path
    f = filename.split("\\")
    l = len(f)
    filename_with_pdf_ext = f[l-1].split(".")
    filename = filename_with_pdf_ext[0]
    output_file_path = output_path + '\\' + filename + '.txt'
    fileopen = open(output_file_path, "w", encoding="utf-8")
    fileopen.write(learning_outcome)
    fileopen.close()

class search_learning_outcome:
    def __init__(self,keywords):
        self.keywords=keywords

#This method is being used to read the files
    def read_text(self,file_path):
        try:
            #keywords = ['learning outcome','learning objective']
            keywords = self.keywords
            self.file_path = file_path
            #fetching the text of the PDF
            #tika returns the contents of the file as a dictionary of list, and to fetch the contents I had to call the content key
            raw = parser.from_file(self.file_path)
            text = raw['content']
            text=text.lower()
            indexes = []
            for key in keywords:
                if key in text:
                    #searching for the keyword in the text
                    index_of_key = text.index(key)
                    #We are trying to find the begining of the text from where the keyword is starting
                    start_index_key_line = text.rfind('\n', 0, index_of_key)
                    string_check= re.compile('[@_!#$,;%^&*()<>?/\|}{~:]')
                    #we search for any new line character or any special character after the occurence of the keyword 
                    spl_chr_search = re.search(string_check,text[index_of_key::])
                    spl_chr_to_str = str(spl_chr_search)
                    spl_chr = spl_chr_to_str[::-1][2]
                    stop_index_spl_chr = text.index(spl_chr,index_of_key)
                    stop_index_newline = text.index('\n',index_of_key)
                    
                    if (stop_index_spl_chr < stop_index_newline):
                        stop_index_key_line = stop_index_spl_chr
                    else:
                        stop_index_key_line = stop_index_newline
                    
                    ending_index_key_line = stop_index_key_line + 500
                    end_string_check= re.compile('[,;.]')
                    end_spl_chr_search = re.search(end_string_check,text[ending_index_key_line::])
                    end_spl_chr_to_str = str(end_spl_chr_search)
                    end_spl_chr = end_spl_chr_to_str[::-1][2]
                    end_stop_index_spl_chr = text.index(end_spl_chr,ending_index_key_line)
                    starting_text = text[start_index_key_line:stop_index_key_line]
                    learning_outcome = text[stop_index_key_line:end_stop_index_spl_chr+1]
                    complete_text = starting_text + '\n' + learning_outcome
                    if (complete_text != None):
                        return complete_text
        except Exception as E:
            print(E)
    
    def read_tables(self,file_path):
        try:
            self.file_path = file_path
            tables = camelot.read_pdf(self.file_path)
            #keywords = ['learning outcome','learning objective']
            keywords = self.keywords
            complete_text = ''
            n = str(tables)
            d = n.index("=")
            c = n[:d:-1][1::]
            number_tables = int(c)
            
            for i in range(number_tables):
                df = tables[i].df # get a pandas DataFrame!
                #print(df)
                if (len(df.columns) ==2):
                    #df = df[0].str.lower()
                    for key in keywords:
                        if (key in df[0][0].lower()):
                            if (len(df[1][0])> len(df[0][1])):
                                for idx, row in df.iterrows():
                                    if key in row[0].lower():
                                        complete_text += row[0] + '\n'
                                        complete_text += row[1]
                                        
                            else:
                                for idx, row in df.iterrows():
                                    complete_text += row[0] + '\n'
                else:
                    for col in range(len(df.columns)):
                        for key in keywords:
                            if key in df[col][0].lower():
                                for row in range(len(df)):
                                    complete_text += df[col][row] + '\n\n'
            if (complete_text != None):
                return complete_text
            
        except Exception as E:
            print(E)

if __name__ == "__main__":
    keywords = ['learning outcome','learning objective']
    obj_search_learn_outcome = search_learning_outcome(keywords)
    files_path = read_input_file_path()
    for filename in files_path:
        if filename.lower().endswith('.pdf'):
            print(filename)
            learning_outcome = obj_search_learn_outcome.read_tables(filename)
            if (learning_outcome == '' or learning_outcome ==None ):
                learning_outcome = obj_search_learn_outcome.read_text(filename)
            
            if (learning_outcome ==None):
                print('We could not find any possible match')
            else:
                print("Output written to file")
                write_output(learning_outcome,filename)
