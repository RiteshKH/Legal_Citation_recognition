# Citation_recognization
Application to read a text document and highlight the citations among the text for easier navigation and impact analysis

Here's a quick guide to each of the files and information:
Final command:: python main.py <filename>.txt 
Ex - python main.py CT-4VYR-5YH0-TXFN-T263-00000-00.txt
spaCy version    2.1.8
Python version   3.7.4

Working of the files explained: 

1.	predict_citation.py 
This takes a single raw text file as input and passes on through the model for prediction. 
Latest model folder: Output2_250_500
Raw text file used: CT-4VYR-5YH0-TXFN-T263-00000-00.txt
Output is generated in csv format: result_citation.csv
(the result contains filenames, citation text)

2.	json_making.py
This file builds the json from the csv file generated from the predicted csv.
Conditions used:
Consider valid citation if(startid != -1 and length < 150)
If duplicate citations present, check for all values positional indexes.

3.	Coref_jsoncreation.py
This file takes in the initial json data and adds anaphoric information (Whether the short citations are refering to some other citation and details of the same).

4.	Json_to_text_doc.py
This file takes in the final json data and raw text file as input.
It generates the output as a text file as required .
The word file generation is commented in main.py

5.	Citationhtmlutils.py
This takes in the raw text file and the text generated from Json_to_text_doc.py as input
Out is the html text with highlighted citations 
