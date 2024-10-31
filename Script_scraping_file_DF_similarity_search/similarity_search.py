import numpy
from transformers import XLMRobertaTokenizer, XLMRobertaModel
from sklearn.metrics.pairwise import cosine_similarity
import torch 
from create_centroid import create_centroid
import os
import json

def get_similarity(word):
    if not os.path.exists("centroid.json"):
            create_centroid()
    centroid_list=[]
    with open("centroid.json","r") as f:
        centroid_list=json.load(f) 
    centroid=numpy.array(centroid_list)
    if centroid is None:
        return -1
    tokenizer=XLMRobertaTokenizer.from_pretrained("xlm-roberta-base") #alcune stringhe possono essere composte da più parole separate da un token
    model=XLMRobertaModel.from_pretrained("xlm-roberta-base")
    inputs=tokenizer(word,return_tensors="pt")
    with torch.no_grad():
        outputs=model(**inputs)
    word_embedding=outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
    reshaped_word_embedding=word_embedding.reshape(1,-1) # con reshape si cambia la struttura del tensore in matrice a due dimensioni senza alterare i dati
    reshaped_centroid=centroid.reshape(1,-1)
    similarity=cosine_similarity(reshaped_word_embedding,reshaped_centroid)[0][0] #somiglianza tra centroide e vettore di parole calcolata come il coseno dell'angolo tra i tensori
    return similarity