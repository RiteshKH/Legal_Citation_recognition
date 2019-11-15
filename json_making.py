# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 17:22:04 2019

@author: 726094
"""
import json
import pandas as pd
import re
import os
from fuzzywuzzy import fuzz 

def getjsonFile():
    
#    citation_raw_file_folder = 'C:/Users/726094/Desktop/analysis/json_building/'
    citation_ml_output_csv = 'outputs/result_citation.csv'
    input_path = 'input/'
    fn = citation_ml_output_csv
    data = pd.read_csv(fn)
    print('')
    print('Data dimensions: ',data.shape)
    
    filenames = data['FileName'].unique()
    citationsar = []
    json_obj = {}
    json_object = []
    for ii in filenames:
        print(ii)
        citations = data.loc[data['FileName'] == ii]['Citation']
        citationsar.extend(citations)

    start_and_len = []
    snl = {}
    ctr = 00
    for i in range(len(citationsar)):
        fname = data.iloc[i]['FileName']
        fname = fname.replace('xml.xml', 'txt')
        myfile = open(input_path + fname).read()
#        myfile = re.sub(r'[^\x00-\x7F]+|\x0c',' ', myfile)  # remove all non-XML-compatible characters
#        citationsar[i] = re.sub(r'[^\x00-\x7F]+|\x0c',' ', citationsar[i])
        startid = myfile.find(citationsar[i], 0, len(myfile))
        length = len(citationsar[i])
        if(startid != -1 and length < 150):
            snl = {
                    'start_id': startid,
                    'len': length,
                    'citation': citationsar[i],
                    'filename': data.iloc[i]['FileName'],
                  	'subtype': data.iloc[i]['SubType'],
                    'anaphoric': {
                          'status': data.iloc[i]['Anaphoric'],
                          'co-ref': str(data.iloc[i]['CoReference'])
                    }
                }
            
            if(i == 0):
                start_and_len.append(snl)
            else:
                fuzzr = 0
                for obj in range(len(start_and_len)):
                    fuzzr = (fuzz.ratio(snl['citation'],start_and_len[obj]['citation']))
                    if fuzzr > 90:
                        break
                if fuzzr < 90:
                    start_and_len.append(snl)
                else:
#                    print('Duplicate')
                    strd = (start_and_len[len(start_and_len)-1]['start_id']+20)  
                    startid = myfile.find(citationsar[i], strd, len(myfile))    # Searching for the string after the last valid citation
#                    print(citationsar[i])
#                    print("Dup: ",startid)
                    snl = {
                        'start_id': startid,
                        'len': length,
                        'citation': citationsar[i],
                        'filename': data.iloc[i]['FileName'],
                      	'subtype': data.iloc[i]['SubType'],
                        'anaphoric': {
                              'status': data.iloc[i]['Anaphoric'],
                              'co-ref': str(data.iloc[i]['CoReference'])
                              }
                        }
                    if(startid != -1):
                        start_and_len.append(snl)
        else:
            data.drop(i,inplace=False)
            i=i+1
        
    for i in range(len(start_and_len)):
#        print(start_and_len[i]['start_id'], start_and_len[i]['len'])
#        print(start_and_len[i]['citation'])
        json_obj = {
                "filename": start_and_len[i]['filename'],
              	"subtype": start_and_len[i]['subtype'],
              	"citation_id": ctr,
              	"citation_textstartid": start_and_len[i]['start_id'],
              	"citation_textlength": start_and_len[i]['len'],
              	"anaphoric": {
                  "status": start_and_len[i]['anaphoric']['status'],
                  "co-ref": start_and_len[i]['anaphoric']['co-ref']
                },
                "name": start_and_len[i]['citation']
                }
                      
        ctr+=1
#        print(json_obj)
        json_object.append(json_obj)
    
#    json_object.remove({})  
    final = {
        "citation": json_object
        }
        
#    fnm = fn.replace('.csv','_')
    with open('outputs/result_citation_data.json', 'w') as outfile:
        json.dump(final, outfile) 
    print('Output file: result_citation_data.json')
    
    print("Intermediate file - JSON created successfully")
    

    
    
    
    
    
    
    
    
    
    