from model_and_tokenizer import get_model_and_tokenizer
import torch
import torch.nn.functional as F
import json
from create_dictionary_embeddings import create_dictionary_embeddings
import os
import json
from sklearn.metrics.pairwise import cosine_similarity
import numpy
def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0]
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)
    
def get_similarity(word):
    if not os.path.exists("dictionary_embeddings.json"):
            create_dictionary_embeddings()
    dictionary_embeddings_list=[]
    with open("dictionary_embeddings.json","r") as f:
        dictionary_embeddings_list=json.load(f) 
    if dictionary_embeddings_list is None:
        return -1
    model,tokenizer=get_model_and_tokenizer()
    inputs = tokenizer(word, padding=True, truncation=True, return_tensors="pt")    
    with torch.no_grad():
        outputs=model(**inputs)
    word_embedding = mean_pooling(outputs, inputs['attention_mask'])
    word_embedding = F.normalize(word_embedding, p=2, dim=1).squeeze().numpy()
    reshaped_word_embedding=word_embedding.reshape(1,-1)
    
    similarity=0
    sum_weight=0
    for embedding in dictionary_embeddings_list.values():
        dictionary_embedding=numpy.array(embedding[0])
        reshaped_dictionary_embedding=dictionary_embedding.reshape(1,-1)
        single_similarity=cosine_similarity(reshaped_word_embedding,reshaped_dictionary_embedding)[0][0] #somiglianza tra centroide e vettore di parole calcolata come il coseno dell'angolo tra i tensori
        similarity+=single_similarity*embedding[1]
        sum_weight+=embedding[1]
    similarity=float(similarity/sum_weight)
    return similarity