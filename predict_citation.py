# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 11:00:05 2019

@author: 726094
"""


import pandas as pd
import spacy
from spacy.util import minibatch, compounding
import plac
from pathlib import Path
import random
import os
import re
import ntpath

def predict_single(raw_text_file):
    output_dir="./model_folder"
    print("Loading from", output_dir)
    nlpOut = spacy.load(output_dir)
    print("Model loaded")
    
#    raw_text_files_folder = 'C:/Users/726094/Desktop/analysis/predict_single_file/'
#    raw_text_file = 'CT-4VYR-5YH0-TXFN-T263-00000-00.txt'

    myfile = open(raw_text_file).read()
#    myfile = re.sub(r'[^\x00-\x7F]+|\x0c',' ', myfile) # remove all non-XML-compatible characters
    fname = ntpath.basename(raw_text_file)
    print('Feeding raw data from: ',fname)
    
    lstFile = []
    lstCitation=[]
    lstLabel = []
#    lstSubType = []
    lstAnaphoric=[]
    lstEnt = []
        
    content = myfile
    doc2 = nlpOut(content)
    for ent in doc2.ents:
        raw_text_file = fname.replace('txt','xml.xml')
        lstFile.append(raw_text_file)
        lstCitation.append(ent.text)
        label = ent.label_
        lstEnt.append(label)
        if label.find("LONG") >= 0:
            lstLabel.append("L")
            lstAnaphoric.append("F")
        else:
            lstLabel.append("S")
            lstAnaphoric.append("T")           
        
        
#        print(ent.label_, ent.text)
            
    dfResult = pd.DataFrame()
    dfResult["FileName"] = lstFile
    dfResult["SubType"] ="JUDICIALCOURTDECISION"
    dfResult["Anaphoric"] = lstAnaphoric
    dfResult["Citation"] = lstCitation
    dfResult["CitationType"] = lstLabel
    dfResult["CoReference"]="NA"
    #dfResult["TestENT"]= lstEnt
    
    #dfResult["FileName"] = lstFile.replace('txt','xml.xml')
    
    dfResult.to_csv("outputs/result_citation.csv", index = False)
    
    print("Model Execution finished")
    print('Number of citations found: ',len(doc2.ents))
    print('Citation data saved as: result_citation.csv')
     