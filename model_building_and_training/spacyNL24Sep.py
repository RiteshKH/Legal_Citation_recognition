import pandas as pd
import spacy
from spacy.util import minibatch, compounding
import plac
import random 
from pathlib import Path 
import pandas as pd
import re 
 
df =  pd.read_csv("train_data_and_labels.csv")
df = df.dropna()

len(df)
training_data1 = []
for index, row in df.iterrows():
    content =str( row["content"])
    entity = row["entity"]
    #print (content)
    entities = []
    entityList = entity.split(",")
    for elist in entityList:
        lstDetail = elist.strip().split(" ")
        if(lstDetail[0].strip() != ""):
            keybeg = int(lstDetail[0])
            keyend = int(lstDetail[1])
            citation_type = str(lstDetail[2])
            entities.append((keybeg, keyend ,citation_type.strip()));
        #subText = str1[beg:end] 
        #print("Beg: ", beg , " End: ", end)
        #print(subText)
    training_data1.append((content, {"entities" : entities})) 

def trim_entity_spans(data: list) -> list:
    """Removes leading and trailing white spaces from entity spans.

    Args:
        data (list): The data to be cleaned in spaCy JSON format.

    Returns:
        list: The cleaned data.
    """
    invalid_span_tokens = re.compile(r'\s')

    cleaned_data = []
    for text, annotations in data:
        entities = annotations['entities']
        valid_entities = []
        for start, end, label in entities:
            valid_start = start
            valid_end = end
            while valid_start < len(text) and invalid_span_tokens.match(text[valid_start]):
                valid_start += 1
                break
            while valid_end > 1 and invalid_span_tokens.match(text[valid_end - 1]):
                valid_end -= 1
                break
            valid_entities.append([valid_start, valid_end, label])
        cleaned_data.append([text, {'entities': valid_entities}])
    return cleaned_data

out=trim_entity_spans(training_data1)        
#TR_DATA =  training_data1[0:100]
#indexes=[i for i in range(0,400)]+[j for j in range(450,len(out))]
#TR_DATA =  [out[i] for i in indexes]
#TR_DATA=training_data1[0:100]
TR_DATA=training_data1[200:400]

print(len(TR_DATA))

## Step 1 Create ner pipline
nlp = spacy.blank("en") 
if "ner" not in nlp.pipe_names:
    print("1")
    ner = nlp.create_pipe("ner")
    nlp.add_pipe(ner, last=True)
    # otherwise, get it so we can add labels
else:
    print("2")
    ner = nlp.get_pipe("ner")
    
for _, annotations in TR_DATA:
    for ent in annotations.get("entities"):
        ner.add_label(ent[2])
        
print("Step 1 Completed") 

# Step 2 - Train the model

other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
other_pipes
#n_iter=100
n_iter=40
with nlp.disable_pipes(*other_pipes):  # only train NER
        nlp.begin_training()
        #print("3*****")
        for itn in range(n_iter):
            print("Iteration:" , itn)
            #print("Iteration# " , itn)
            random.shuffle(TR_DATA)
            #print("2")
            losses = {}
            # batch up the examples using spaCy's minibatch
            #print("4*****")
            #print("3")
            batches = minibatch(TR_DATA, size=compounding(4.0, 32.0, 1.001))
            #print("batches len:",size)
            #print(type(batches))
            #print("4")
            #cnt=1
            for batch in batches:
                #print("current batch:",cnt)
                #print("5")
                texts, annotations = zip(*batch)
                #print(texts)
                #print("##########")
                #print(annotations)
                #print("*****")
                #print("6")
                nlp.update(
                    texts,  # batch of texts
                    annotations,  # batch of annotations
                    drop=0.5,  # dropout - make it harder to memorise data
                    losses=losses,
                )
                #cnt+=1
            #print(cnt)
            #print("Losses", losses)

print("Step 2 Completed")        


output_dir="./"
if output_dir is not None:
    output_dir = Path(output_dir)
    if not output_dir.exists():
        output_dir.mkdir()
    nlp.to_disk(output_dir)
    print("Saved model to", output_dir)

print("Step 3 Completed")


'''
print("Loading from", output_dir)
nlp2 = spacy.load(output_dir)

test_text = training_data1[320][0]

#test_text = str1
doc2 = nlp(test_text)
for ent in doc2.ents:
    print(ent.label_, ent.text)

'''