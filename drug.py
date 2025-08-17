from fastapi import FastAPI,HTTPException,Query 
from fastapi.responses import JSONResponse
from typing_extensions import Annotated
from pydantic import BaseModel,Field,field_validator,model_validator
import joblib
import pandas as pd
import numpy as np
from  gensim.models import Word2Vec
import xgboost as xgb

app = FastAPI()

#data loading for validation
#data = pd.read_csv('label_encoded.csv')

label_file = pd.read_excel('data\DDI_types_merged.xlsx')
label_file.columns = label_file.columns.str.strip()
idx = label_file['merged DDI type index']
intrxn_type = label_file['type name']
id2label = dict(zip(idx,intrxn_type))

w2v = Word2Vec.load('W2Vec_model.model')
validation_drug = set(w2v.wv.key_to_index.keys())

ML_model = joblib.load('xgb_model.pkl')

#pydentic class for data validation 
class Drug(BaseModel):
    drug1 : Annotated[str,Field(...,description='Enter Drug 1 name:',examples=['Bivalirudin'])]
    drug2 : Annotated[str,Field(...,description='Enter Drug name with which you want to see interaction',examples=['Simvastatin'])]

    @field_validator('drug1','drug2')
    @classmethod
    #validating drug in dataset 
    def check_existance(cls,value:str):
        if not isinstance(value,str) or not value.strip():
            raise ValueError('Drug must be a non empty string')
        name = value.strip()

        if name not in validation_drug:
                raise ValueError(f"{name} Drug not found in database")
        else:
            return name
        
    @model_validator(mode='after')
    def drug_must_diff(self):
        if self.drug1 == self.drug2:
            raise ValueError("drug1 and drug2 must be different")
        return self

#converting drug to vec  
def pair_to_vec(drug:Drug,w2v):
    for d in [drug.drug1, drug.drug2]:
        if d not in w2v.wv:
            raise HTTPException(status_code=400, detail=f"{d} not in embedding vocabulary")
    vec1 = w2v.wv[drug.drug1]
    vec2 = w2v.wv[drug.drug2]

    conc = np.concatenate([vec1,vec2])
    #Feature engineering
    diff_vec = np.abs(vec1-vec2)
    multi_vec = vec2*vec1
    return np.concatenate([conc,diff_vec,multi_vec])

#Nodes 
@app.get('/home')
def greeting():
    return {'message':'Hello welcome to Program which Finds drug to Drug interaction type'}

@app.get('/about')
def about():
    return {'message':'This is a drug to drug interaction finding program with more than 86"%" accuracy'}

@app.post('/Drug_interaction')
def drug_intraction(
    drug1: str = Query(..., description="Drug 1 name"),
    drug2: str = Query(..., description="Drug 2 name")
):
    try:
        drugs = Drug(drug1=drug1, drug2=drug2)  # validate with Pydantic
            
        vec = pair_to_vec(drugs,w2v).reshape(1, -1)
        pred = ML_model.predict(xgb.DMatrix(vec))
        pred_class = int(pred.argmax(axis=1)[0])
        
        return JSONResponse(status_code=200,content={"interaction_type_index": pred_class,"interaction_type_label": id2label[pred_class]})
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))





