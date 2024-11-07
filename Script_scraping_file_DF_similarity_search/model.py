from transformers import AutoTokenizer, AutoModel
import torch
import os 
import json
from sklearn.metrics.pairwise import cosine_similarity
import numpy

class Model():
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Model, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'model'):
            self.model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
            self.tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
            
    def create_dictionary_embeddings():
        with open("dictionary.json","r") as f:
            dictionary=json.load("dictionary.json",f)
        model=Model()
        embeddings={}
        for word,rate in dictionary:
            embedding=model.get_embedding(word)
            embeddings[word]=(embedding.tolist(),rate)
        with open("dictionary_embeddings.json","w") as f:
            json.dump(embeddings,f)
            
    def get_embedding(self,word):
        input = self.tokenizer(word, padding=True, truncation=True, return_tensors="pt") #restituisce tensori di pytorch
        with torch.no_grad(): #permette di risparmiare memoria, in quanto non calcola i gradienti (non stiamo addestrando il modello)
            output=self.model(**input) #l'output del modello
        #mean pooling
        token_embeddings = output[0]
        input_mask_expanded =input['attention_mask'].unsqueeze(-1).expand(token_embeddings.size()).float()
        embedding = torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)
        return embedding
    
    def get_similarity(self,word):
        if not os.path.exists("dictionary_embeddings.json"):
            self.create_dictionary_embeddings()
        dictionary_embeddings_list=[]
        with open("dictionary_embeddings.json","r") as f:
            dictionary_embeddings_list=json.load(f) 
        if dictionary_embeddings_list is None:
            return -1
        input = self.tokenizer(word, padding=True, truncation=True, return_tensors="pt")    
        with torch.no_grad():
            output=self.model(**input)
        token_embeddings = output[0]
        input_mask_expanded =input['attention_mask'].unsqueeze(-1).expand(token_embeddings.size()).float()
        embedding = torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)
        reshaped_word_embedding=embedding.reshape(1,-1)
        
        similarity=0
        sum_weight=0
        similarities=[]
        for embedding in dictionary_embeddings_list.values():
            dictionary_embedding=numpy.array(embedding[0])
            reshaped_dictionary_embedding=dictionary_embedding.reshape(1,-1)
            single_similarity=cosine_similarity(reshaped_word_embedding,reshaped_dictionary_embedding)[0][0] #somiglianza tra centroide e vettore di parole calcolata come il coseno dell'angolo tra i tensori
            similarities.append((single_similarity,embedding[1]))
        similarities.sort(key=lambda x:x[0],reverse=True)
        
        for i in range(4):
            similarity+=similarities[i][0]*similarities[i][1]
            sum_weight+=similarities[i][1]
        similarity/=sum_weight
        return similarity