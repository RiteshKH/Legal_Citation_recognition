#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 23:59:41 2019

@author: ritz
"""


#if __name__ == '__main__':
#    main()
    

from predict_citation import predict_single
from json_making import getjsonFile
from coref_jsoncreation import getcorefjson
from json_2_text_doc import getjsontotext,getjsontodocx
from citationhtmlutil import htmlgeneration
import sys
import time

def main(path): #Give the path to raw text file
    
    """
    Prediction on a single text file using spacy model, generates citations in csv format
    """
    predict_single(path)
    """
    Preparing the json file from csv data, getting indexes of citations
    """
    getjsonFile()
    """
    Passing the json for anaphoric and co-referencing filteration
    """
    getcorefjson()
    """
    Passing the json to create word and text file from raw data
    """
    getjsontotext()
    
    getjsontodocx()
    """
    Passing the json to create html file from raw data
    """
    htmlgeneration(path)
    
    print("Output saved in the folder")
    
    
#    
if __name__ == "__main__":
    
    t0 = time.time()
    main(sys.argv[1])

    print ('Total processing time:: '+str(time.time() - t0)+' secs')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    