## Citation_recognition
Python application to read a legal case document in text format and highlight the citations among the text for easier navigation and impact analysis.

Legal citation is the practice of crediting and referring to authoritative documents and sources. The most common sources of authority cited are court decisions (cases), statutes, regulations, treaties, and scholarly writing.
Typically, a proper legal citation will inform the reader about a source's authority, how strongly the source supports the writer's proposition, its age, and other, relevant information. This is an example citation to a United States Supreme Court court case:
<br /> `Griswold v. Connecticut, 381 U.S. 479, 480 (1965).`
<br />However in very long documents, searching for citations is a time consuming process. It is also a difficult task in NLP to find out the pattern of citation text and predict them. We have used a 'spacy' deep learning model for this purpose.

![approach](https://user-images.githubusercontent.com/38212000/68930565-add2c300-07b4-11ea-9a06-4757945917b9.JPG)

Here's a quick guide to each of the files and information:

* `input` folder: Keep the document in txt format in this folder
* `outputs` folder: Contains the generated output files. The highlighted text can be found in html and word document. The txt file here lists out the predicted citations.

Final command:: `python main.py input/<filename>.txt`
<br />Ex - `python main.py input/sample_input.txt`

Use the following command to install ans satisfy all requirements:
`pip install --user --requirement requirements.txt`

### Working of the files explained: 

* `spacyNL24Sep.py` : This is the code for building the spacy model, separately kept in `model_building_and_training` folder. For building the model on your own, put the files `train_data_and_labels.csv` and `test_data.csv` in the same folder and tweak the python script according to the dataframe.

* `predict_citation.py` : This module takes a single raw text file as input and passes on through the model for prediction. Output is generated in csv format: result_citation.csv
(the result contains filenames, citation text)

* `json_making.py` : This module builds the json from the csv file generated from the predicted csv.
Conditions used: Consider valid citation if(startid != -1 and length < 150)
If duplicate citations are present, we check for all the citations's positional indexes and keep the record accordingly.

* `Coref_jsoncreation.py` :  This file takes in the initial json data and adds anaphoric information (Whether the short citations are refering to some other citation and details of the same).

* `Json_to_text_doc.py`: This file takes in the final json data and raw text file as input. It generates the output as a text file as required . It also generates a docx file which contains all the highlighted citations

* `Citationhtmlutils.py` : This takes in the raw text file and the text generated from `Json_to_text_doc.py` as input, and generates the html text with highlighted citations 

### Sample input
![input](https://user-images.githubusercontent.com/38212000/68931813-541fc800-07b7-11ea-85c1-7b1ea7592bd5.JPG)
### Generated Outputs
### Command line output:
![cmd_output](https://user-images.githubusercontent.com/38212000/68931897-83ced000-07b7-11ea-8e56-842d03e25ae3.JPG)
<br /> 
### Predicted citations in json:
![json_output](https://user-images.githubusercontent.com/38212000/68932100-eaec8480-07b7-11ea-8877-632c07075271.JPG)
<br /> 
### Highlighted text:
![html_output](https://user-images.githubusercontent.com/38212000/68932142-ffc91800-07b7-11ea-9734-559f6e00bf65.JPG)

### Future work : 
The precision and recall currently is not good enough, and many citations are still not detected.
Need to try other techniques such as LSTMs or BERT and try to improve the results. 
