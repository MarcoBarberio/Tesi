import numpy
from transformers import XLMRobertaTokenizer, XLMRobertaModel
import torch
import json

dizionary = ["Sostenibilità", "ESG"]
def create_centroid():
    tokenizer=XLMRobertaTokenizer.from_pretrained("xlm-roberta-base") #alcune stringhe possono essere composte da più parole separate da un token
    model=XLMRobertaModel.from_pretrained("xlm-roberta-base")
    embeddings=[]
    for word in dizionary:
        inputs=tokenizer(word,return_tensors="pt") #restituisce tensori di pytorch
        with torch.no_grad(): #permette di risparmiare memoria, in quanto non calcola i gradienti (non stiamo addestrando il modello)
            outputs=model(**inputs) #l'output del modello
            #si estraggono i vettori di embedding per ciascun token, se ne calcola la media, si eliminano dimensioni inutili e si converte il tensore torch in numpy
        word_embedding=outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
        embeddings.append(word_embedding)
    if embeddings:
        centroid=numpy.mean(embeddings,axis=0)
        centroid_list=centroid.tolist()
        with open("centroid.json","w") as f:
            json.dump(centroid_list,f)