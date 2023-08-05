"""
Created on Fri Apr 7 21:49:16 2017

@author: cpkmanchee
"""

import numpy as np
import os
import csv
import pickle

from beamtools.file_formats import file_formats

__all__ = ['import_data_file', 'list_atr','list_filetypes']

class objdict(dict):
    def __init__(self,d):
        self.__dict__ = d
    def fields(self):
        return self.__dict__.keys()

def list_filetypes():
    '''Display all filetypes in dictionary
    '''
    [print(k) for k in file_formats.keys()]
    return

def list_atr(given_filetype):
    '''List the attributes of resultant object from data import.
    '''
    filetype = filetype_lookup(file_formats,given_filetype.lower())
    column_labels = file_formats.get(filetype).get('column_labels')
    print(column_labels)
    return

                
def filetype_lookup(file_dict, given_type):
    '''Identify file type for given input. Only first found match is returned.
    '''
    for k,v in file_dict.items():
        if given_type in file_dict.get(k).get('alias'):
            return(k)
        
    raise RuntimeError('File type lookup failed. File type "%s" not found' %(given_type))
    return(None)

def import_data_file(file, given_filetype):
    '''Imports data of given filetype.
    Data returned as object with appropriate attributes
    '''

    filetype = filetype_lookup(file_formats,given_filetype.lower())

    header_lines = file_formats.get(filetype).get('header_lines')
    delimiter = file_formats.get(filetype).get('delimiter')
    column_labels = file_formats.get(filetype).get('column_labels')

    #initialize header and output dictionary
    header=[]
    output={}
    [output.update({c:[]}) for c in column_labels]
    with open(file, 'r') as f:
        #extract header information only
        data = csv.reader(f, delimiter = delimiter)
        for i in range(header_lines):
            header.append(data.__next__())
        #write rest of data to dictionary, keys are column_labels, values = data 
        [[(output[c].append(row[c_ind].strip())) for c_ind,c in enumerate(column_labels)] for row in data]

    #convert data to float
    for c in output.keys():
        try:
            output[c] = np.asarray(output[c],dtype=np.float)
        except ValueError:
            try:
                output[c] = np.asarray(output[c])
            except ValueError:
                pass

    output.update({'header': header})
    output_obj = objdict(output)

    return output_obj

'''
filedir = '/Users/cpkmanchee/Google Drive/PhD/Data/2016-11-22 DILAS temp profile'
fileMON = '2016-11-22 MON temperature profile 10W.txt'
filePOW = '2016-11-22 PM100 temperature profile 10W.txt'

file = os.path.join(filedir,fileMON)
file_type = 'monitor'

data = import_data_file(file,file_type)
print(data.time[0])
'''


