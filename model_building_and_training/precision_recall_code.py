#!/usr/bin/env python
# coding: utf-8
#### Creation of Csv file from xml file

import os
import pandas as pd
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz


folder_path = "C:\\Users\\590446\\Documents\\LN_CR_training_xml\\LN_CR_training"

df = pd.DataFrame()
col = ["FileName", "Subtype", "Anaphoric", "Name", "CitationType", "Co-Ref"]
data = []

for root, dirs, files in os.walk(folder_path):
    for file_ in files:
        if not file_.endswith(".xml"):
            continue
        
        ## Performing further steps if file is ".xml"
        full_path = os.path.join(root, file_)
        #print("full_path:", full_path)
    
        infile = open(full_path, "r", errors="ignore")
        print("file: ", root, file_)
        fcontent = infile.read()
    
        soup = BeautifulSoup(fcontent,'xml')
        cit_data = soup.findAll('CITATION')
    
        for cit in cit_data:
            anaphoric = "FALSE"
            co_ref = "NA"
            cit_type = "S"
            
            try:
                subtype = cit['SUBTYPE']
                anaphoric = cit['ANAPHORIC']
            except:
                pass
    
            if subtype == "JUDICIALCOURTDECISION":
                name = cit.text
                if anaphoric == "FALSE":
                    cit_type = "L" 
                    
                print(subtype, anaphoric, co_ref, cit_type)
                data.append([file_, subtype, anaphoric, name, cit_type, co_ref])
                

# Create the pandas DataFrame 
df = pd.DataFrame(data, columns = col) 

# saving to csv
df.to_csv("all_data.csv")

# print dataframe. 
df.head()

cit_data = soup.findAll('CITATION')


cit_data
ind = cit_data[0]

anaphoric = "False"
co_ref = "NA"
try:
    subtype = ind['SUBTYPE']
    anaphoric = ind['ANAPHORIC']
    name = ind.text
except:
    pass
    
if subtype == "JUDICIALCOURTDECISION":
    print(subtype, anaphoric, co_ref)
    
print(subtype, anaphoric, co_ref)

path = "C:\\Users\\590446\\Documents\\LN_CR_training_xml\\LN_CR_training"
for root, dirs, files in os.walk(path):
    for file in files:
        print(file)

######################################
######## Comparing Actual and PRedict#
######################################

import pandas as pd
from fuzzywuzzy import fuzz

a_df = pd.read_csv("all_data.csv")
#p_df = pd.read_csv("all_data.csv")
p_df = pd.read_csv("result_25Sep_225_475_100_ab_Files.csv")

unique_file = p_df["FileName"].unique()
data = []
col = ["FileName", "ActualSubType", "ActualAnaphoric", "ActualCitation", "ActualCitationType", "ActualCoReference", 
       "PredictedSubType", "PredictedAnaphoric", "PredictedCitation", "PredictedCitationType", "PredictedCoReference", 
       "MatchPercentage"]

## Generating csv file keeping "Predicted as Base"
#count = 0
for file_name in unique_file:
    afile_data = a_df[a_df["FileName"] == file_name]
    pfile_data = p_df[p_df["FileName"] == file_name]
    print(afile_data.shape, pfile_data.shape)
    
    for a_row in afile_data.itertuples(index=False):
        match_per = 0
        max_per = 0
        
        for p_row in pfile_data.itertuples(index=False):
            match_per = fuzz.ratio(a_row.Name, p_row.Citation)
            
            if max_per <= match_per:
                max_per = match_per
                
                a_name = a_row.Name
                a_subtype = a_row.Subtype
                a_anaphoric = a_row.Anaphoric
                a_cit_type = a_row.CitationType
                a_co_ref = a_row.CoRef
                
                p_name = p_row.Citation
                p_subtype = p_row.SubType
                p_anaphoric = p_row.Anaphoric
                p_cit_type = p_row.CitationType
                p_co_ref = p_row.CoReference
                
        ## appending value in data
        print(a_subtype, a_anaphoric)
        data.append([file_name, a_subtype, a_anaphoric, a_name, a_cit_type, a_co_ref,
                    p_subtype, p_anaphoric, p_name, p_cit_type, p_co_ref, max_per])
                
        print("Max Percentage: ", max_per)  

    # for testing purpose
    #count += 1
    #if count >= 1:
        #break
        

# Create the pandas DataFrame 
df = pd.DataFrame(data, columns = col) 

# saving to csv
df.to_csv("actual_predicted_data_1.csv")

# print dataframe. 
df.head()
    
    
    
##########################################################
######## Generating csv file Comparing Actual and PRedict#
##########################################################

import pandas as pd
from fuzzywuzzy import fuzz

def compare_actual_predict(all_data_file, result_file):
    a_df = pd.read_csv(all_data_file)
    #p_df = pd.read_csv("all_data.csv")
    p_df = pd.read_csv(result_file)

    unique_file = p_df["FileName"].unique()
    data = []
    col = ["FileName", "ActualSubType", "ActualAnaphoric", "ActualCitation", "ActualCitationType", "ActualCoReference", 
           "PredictedSubType", "PredictedAnaphoric", "PredictedCitation", "PredictedCitationType", "PredictedCoReference", 
           "MatchPercentage"]

    ## Generating csv file keeping "Predicted as Base"
    #count = 0
    for file_name in unique_file:
        afile_data = a_df[a_df["FileName"] == file_name]
        pfile_data = p_df[p_df["FileName"] == file_name]
        print(afile_data.shape, pfile_data.shape)

        for a_row in afile_data.itertuples(index=False):
            match_per = 0
            max_per = 0

            for p_row in pfile_data.itertuples(index=False):
                match_per = fuzz.ratio(a_row.Name, p_row.Citation)

                if max_per <= match_per:
                    max_per = match_per

                    a_name = a_row.Name
                    a_subtype = a_row.Subtype
                    a_anaphoric = a_row.Anaphoric
                    a_cit_type = a_row.CitationType
                    a_co_ref = a_row.CoRef

                    p_name = p_row.Citation
                    p_subtype = p_row.SubType
                    p_anaphoric = p_row.Anaphoric
                    p_cit_type = p_row.CitationType
                    p_co_ref = p_row.CoReference

            ## appending value in data
            print(a_subtype, a_anaphoric)
            data.append([file_name, a_subtype, a_anaphoric, a_name, a_cit_type, a_co_ref,
                        p_subtype, p_anaphoric, p_name, p_cit_type, p_co_ref, max_per])

            print("Max Percentage: ", max_per)  

        # for testing purpose
        #count += 1
        #if count >= 1:
            #break


    # Create the pandas DataFrame 
    df_base_predicted = pd.DataFrame(data, columns = col) 

    # saving to csv
    df_base_predicted.to_csv("base_predicted.csv")

    # print dataframe. 
    #df.head()

    ## Generating csv file keeping "Actual as Base"
    data = []
    col = ["FileName", "ActualSubType", "ActualAnaphoric", "ActualCitation", "ActualCitationType", "ActualCoReference", 
           "PredictedSubType", "PredictedAnaphoric", "PredictedCitation", "PredictedCitationType", "PredictedCoReference", 
           "MatchPercentage"]
    
    for file_name in unique_file:
        afile_data = a_df[a_df["FileName"] == file_name]
        pfile_data = p_df[p_df["FileName"] == file_name]
        print(afile_data.shape, pfile_data.shape)

        for p_row in pfile_data.itertuples(index=False):
            match_per = 0
            max_per = 0

            for a_row in afile_data.itertuples(index=False):
                match_per = fuzz.ratio(a_row.Name, p_row.Citation)

                if max_per <= match_per:
                    max_per = match_per

                    a_name = a_row.Name
                    a_subtype = a_row.Subtype
                    a_anaphoric = a_row.Anaphoric
                    a_cit_type = a_row.CitationType
                    a_co_ref = a_row.CoRef

                    p_name = p_row.Citation
                    p_subtype = p_row.SubType
                    p_anaphoric = p_row.Anaphoric
                    p_cit_type = p_row.CitationType
                    p_co_ref = p_row.CoReference

            ## appending value in data
            print(a_subtype, a_anaphoric)
            data.append([file_name, a_subtype, a_anaphoric, a_name, a_cit_type, a_co_ref,
                        p_subtype, p_anaphoric, p_name, p_cit_type, p_co_ref, max_per])

            print("Max Percentage: ", max_per)  

    # Create the pandas DataFrame 
    df_base_actual = pd.DataFrame(data, columns = col) 

    # saving to csv
    df_base_actual.to_csv("base_actual.csv")

    # print dataframe. 
    #df.head()



### Geneating recall, precision value
import json

def generate_confusion_matrix_value(base_actual_file, base_predicted_file, threshold,Condition):
    base_a_df = pd.read_csv(base_actual_file)
    #p_df = pd.read_csv("all_data.csv")
    base_p_df = pd.read_csv(base_predicted_file)
    
    tn_count = 0
    tp_count = base_a_df[base_a_df["MatchPercentage"] >= threshold].shape[0]
    fn_count = base_a_df.shape[0] - tp_count
    
    tp_L_count=0
    tp_S_count=0
    ##TP_L & FN_L
    tp_L_count = base_a_df[(base_a_df["MatchPercentage" ] >= threshold)& (base_a_df["ActualCitationType"]=='L')].shape[0]
    fn_L_count = base_a_df[(base_a_df["ActualCitationType"]=='L')].shape[0] - tp_L_count
    ##TP_S & FN_S
    tp_S_count = base_a_df[(base_a_df["MatchPercentage" ] >= threshold)& (base_a_df["ActualCitationType"]=='S')].shape[0]
    fn_S_count = base_a_df[(base_a_df["ActualCitationType"]=='S')].shape[0] - tp_S_count
    
    ## Generating FP
    if Condition=="ALL":
        base_a_data = base_a_df[base_a_df["MatchPercentage"] < threshold]
        base_p_data = base_p_df[base_p_df["MatchPercentage"] < threshold]
    elif Condition=="S":
        base_a_data = base_a_df[(base_a_df["MatchPercentage"] < threshold) & (base_a_df["ActualCitationType"]=='S')]
        base_p_data = base_p_df[(base_p_df["MatchPercentage"] < threshold) & (base_p_df["ActualCitationType"]=='S')]
    else:
        base_a_data = base_a_df[(base_a_df["MatchPercentage"] < threshold) & (base_a_df["ActualCitationType"]=='L')]
        base_p_data = base_p_df[(base_p_df["MatchPercentage"] < threshold) & (base_p_df["ActualCitationType"]=='L')]

    unique_file = base_a_data["FileName"].unique()
    
    if base_a_data.empty==True or base_p_data.empty==True:
        raise Exception("No data to be filtered")
    else:
        pass

    fp_count = 0
    for file_name in unique_file:
        afile_data = base_a_data[base_a_data["FileName"] == file_name]
        pfile_data = base_p_data[base_p_data["FileName"] == file_name]
        
        for p_row in pfile_data.itertuples(index=False):
            match_per = 0
            max_per = 0

            for a_row in afile_data.itertuples(index=False):
                match_per = fuzz.ratio(a_row.PredictedCitation, p_row.PredictedCitation)

                if max_per <= match_per:
                    max_per = match_per
                    
            #print("Max Percentage: ", max_per) 
            
            if max_per < 100:
                fp_count += 1
    
    ## calculating precision, recall
    if Condition=="L":
        tp_count=tp_L_count
        fn_count=fn_L_count
    elif Condition=="S":
        tp_count=tp_S_count
        fn_count=fn_S_count
    else:
        tp_count=tp_count
        fn_count=fn_count

    precision = tp_count / (tp_count + fp_count) * 100
    recall = tp_count / (tp_count + fn_count) * 100
    
    matrix_data = {
        "precision": precision,
        "recall": recall,
        "tp_count": tp_count,
        "fp_count": fp_count,
        "tn_count": tn_count,
        "fn_count": fn_count
    }
    
    with open('matrix_value.json', 'w') as outfile:
        json.dump(matrix_data, outfile)
    
    print(matrix_data)
    return matrix_data
    
path="D:/LexisNexis/Spacy_predict/"
generate_confusion_matrix_value(path+'base_actual_file.csv',path+'base_predicted_file.csv',90,"ALL")


### Calling function to compare actual predict and generated csv file containg match percentage
all_data_file = "all_data.csv"
result_file = "result_25Sep_225_475_100_ab_Files.csv"
compare_actual_predict(all_data_file, result_file)


### Genrating recall, precision
base_actual_file = "base_actual.csv"
base_predicted_file = "base_predicted.csv"
threshold = 90
generate_confusion_matrix_value(base_actual_file, base_predicted_file, threshold)






