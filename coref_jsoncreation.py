import json
from fuzzywuzzy import fuzz 
#from fuzzywuzzy import process 

def getcorefjson():
    #get json file
#    json_path="C:/Users/726094/Desktop/analysis/coref_json_creation/"
    filename='outputs/result_citation_data.json'
    with open(filename) as _file:
        pred_json=json.load(_file)
        
        
    for i in range(0,len(pred_json['citation'])):
        if pred_json['citation'][i]['anaphoric']['status']=='T':
    #        print(pred_json['citation'][i]['anaphoric']['co-ref'])
            text_start_id=pred_json['citation'][i]['citation_textstartid']
            name=pred_json['citation'][i]['name']
    #        print(text_start_id,"\n",name)
    #        print(pred_json['citation'][i]['anaphoric']['co-ref'])
            strt_name_lst=[(pred_json['citation'][j]['citation_textstartid'],pred_json['citation'][j]['name'],pred_json['citation'][j]['citation_id']) for j in range(0,len(pred_json['citation']))  if pred_json['citation'][j]['citation_textstartid'] < text_start_id and pred_json['citation'][j]['anaphoric']['status']=='F' ]
            strt_name_lst=list(set(strt_name_lst))
            strt_name_lst.sort(key=lambda x:x[0],reverse=True)
            #strt_name_lst_10=strt_name_lst[0:10]
            #print(strt_name_lst_10)
            match_lst=[(fuzz.partial_ratio(name,top_name[1]),top_name[1],top_name[2]) for top_name in strt_name_lst if fuzz.partial_ratio(name,top_name[1])>60] 
            if match_lst:
                #get the highest score one
                max_score=max(match_lst,key=lambda item: item[0])
                pred_json['citation'][i]['anaphoric']['co-ref']=max_score[2]

    
#    outfile_path="C:/Users/726094/Desktop/analysis/coref_json_creation/"
#    filename = filename.replace('.json','')
    with open('outputs/result_citation_data_coref_out.json', 'w') as outfile:
        json.dump(pred_json, outfile)
    
    print('Intermediate file - JSON with co-refs generated')
        
#fuzz.partial_ratio('id  02-0520497S','Landmark Development v. East Lyme Zoning Commission, Superior Court, judicial district of New Britain, docket no. CV 02-0520497S, 2004 Conn. Super. LEXIS 2566')                






