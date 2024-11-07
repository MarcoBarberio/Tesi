from transformers import AutoTokenizer, AutoModel
import torch
import os 
import json
from sklearn.metrics.pairwise import cosine_similarity

class Model():
    
    _instance = None 
    def __new__(cls): #Permette di creare un unico modello in singleton. Viene chiamato da init per istanziare una istanza senza attributi
        if cls._instance is None:
            cls._instance = super(Model, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'model'): #nel caso sia la prima volta che viene chiamato il costruttore l'istanza non ha attributi
            self.model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
            self.tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
            
    def create_dictionary_embeddings(self): #Permette di calcolare gli embeddings di una serie di parole caricate su un json insieme ad un peso che ha ogni parola 
        with open("dictionary.json","r") as f:
            dictionary=json.load("dictionary.json",f)
        embeddings={}
        for word,rate in dictionary:
            embedding=self.get_embedding(word)
            embeddings[word]=(embedding.tolist(),rate) #gli embeddings vengono salvati in un file json, insieme al peso che hanno
        with open("dictionary_embeddings.json","w") as f:
            json.dump(embeddings,f)
            
    def get_embedding(self,word): #metodo per calcolare gli embedding di una parola
        input = self.tokenizer(word, padding=True, truncation=True, return_tensors="pt") #La parola viene tokenizzata e per ogni token viene restituito un tensore di pytorch
        with torch.no_grad(): #permette di risparmiare memoria, in quanto non calcola i gradienti (non stiamo addestrando il modello)
            output=self.model(**input) #gli embedding della parola
        
        #l'output contiene gli embedding dei token, quindi si effettua un'operazione di mean pooling per ottenere il significato complessivo dei token (quindi della parola)
        token_embeddings = output[0]
        input_mask_expanded =input['attention_mask'].unsqueeze(-1).expand(token_embeddings.size()).float()
        embedding = torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)
        
        return embedding
    
    def get_similarity(self,word): #per il calcolo della similarità di una parola con le parole del dizionario si fa una media pesata delle tre singole similarità tra la parola e le parole del dizionario con valore più alto 
        if not os.path.exists("dictionary_embeddings.json"):
            self.create_dictionary_embeddings()
        dictionary_embeddings_list=[]
        with open("dictionary_embeddings.json","r") as f:
            dictionary_embeddings_list=json.load(f) 
        if dictionary_embeddings_list is None:
            return -1
        
        embedding=self.get_embedding(word)
        reshaped_word_embedding=embedding.reshape(1,-1) #reshape dell'embedding per il calcolo della similarità (formato da una riga e da un numero di colonne calcolato automaticamente)
        
        #media pesata
        similarity=0
        sum_weight=0
        similarities=[]
        for embedding in dictionary_embeddings_list.values():
            dictionary_embedding=torch.tensor(embedding[0]) #embedding[0] contiene l'embedding stesso sottoforma di array, quindi va convertito in tensore pytorch
            reshaped_dictionary_embedding=dictionary_embedding.reshape(1,-1)
            single_similarity=cosine_similarity(reshaped_word_embedding,reshaped_dictionary_embedding)[0][0] #somiglianza tra centroide e vettore di parole calcolata come il coseno dell'angolo tra i tensori
            similarities.append((single_similarity,embedding[1])) #embedding[1] contiene il peso dell'embedding
        
        similarities.sort(key=lambda x:x[0],reverse=True)
        for i in range(4): #i valori di similarità vengono ordinati e vengono presi i 3 con valore più alto
            similarity+=similarities[i][0]*similarities[i][1]
            sum_weight+=similarities[i][1]
        similarity/=sum_weight
        return similarity