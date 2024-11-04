from model_and_tokenizer import get_model_and_tokenizer
import torch
import torch.nn.functional as F
import json
from create_centroid import create_centroid
import os
import json
from sklearn.metrics.pairwise import cosine_similarity
import numpy
def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0]
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

def get_similarity(word):
    if not os.path.exists("centroid.json"):
            create_centroid()
    centroid_list=[]
    with open("centroid.json","r") as f:
        centroid_list=json.load(f) 
    centroid=numpy.array(centroid_list)
    if centroid is None:
        return -1
    model,tokenizer=get_model_and_tokenizer()
    inputs = tokenizer(word, padding=True, truncation=True, return_tensors="pt")    
    with torch.no_grad():
        outputs=model(**inputs)
    word_embedding = mean_pooling(outputs, inputs['attention_mask'])
    word_embedding = F.normalize(word_embedding, p=2, dim=1).squeeze().numpy()

    reshaped_word_embedding=word_embedding.reshape(1,-1)
    
    similarity=cosine_similarity(reshaped_word_embedding,centroid)[0][0] #somiglianza tra centroide e vettore di parole calcolata come il coseno dell'angolo tra i tensori
    return similarity