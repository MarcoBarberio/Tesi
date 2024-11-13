from transformers import AutoTokenizer, AutoModel
import torch
import os 
import json
from sklearn.metrics.pairwise import cosine_similarity
from .text_embedding_interface import Text_embedder_interface
class Text_embedder(Text_embedder_interface):
    #il modello deve essere creato in singleton. 
    _instance = None 
    def __new__(cls): 
        #Viene chiamato da init per istanziare una istanza senza attributi
        if cls._instance is None:
            cls._instance = super(Text_embedder, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        #nel caso sia la prima volta che viene chiamato il costruttore l'istanza non ha attributi
        if not hasattr(self, 'model'): 
            self.model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
            self.tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
    
    #Permette di calcolare gli embeddings di una serie di parole caricate su un json insieme ad un peso che ha ogni parola
    def _create_dictionary_embeddings(self):  
        with open(os.getenv("DICTIONARY"),"r") as f:
            dictionary=json.load(f)
        embeddings={}
        for word,rate in dictionary:
            embedding=self.__get_embedding(word)
            #gli embeddings vengono salvati in un file json, insieme al peso che hanno
            embeddings[word]=(embedding.tolist(),rate) 
        with open(os.getenv("DICTIONARY_EMBEDDINGS"),"w") as f:
            json.dump(embeddings,f)
            
    #metodo per calcolare gli embedding di una parola
    def _get_embedding(self,word): 
        #La parola viene tokenizzata e per ogni token viene restituito un tensore di pytorch
        input = self.tokenizer(word, padding=True, truncation=True, return_tensors="pt") 
        #torch.no grad permette di risparmiare memoria, in quanto non calcola i gradienti (non stiamo addestrando il modello)
        with torch.no_grad(): 
            output=self.model(**input) #gli embedding della parola
        
        #l'output contiene gli embedding dei token, quindi si effettua un'operazione di mean pooling per ottenere il significato complessivo dei token (quindi della parola)
        token_embeddings = output[0]
        input_mask_expanded =input['attention_mask'].unsqueeze(-1).expand(token_embeddings.size()).float()
        embedding = torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)
        
        return embedding
    
    #per il calcolo della similarità di una parola con le parole del dizionario si fa 
    #una media pesata delle tre singole similarità tra la parola e le parole del dizionario con valore più alto
    def get_similarity(self,word):  
        if not os.path.exists(os.getenv("DICTIONARY_EMBEDDINGS")):
            self.__create_dictionary_embeddings()
        dictionary_embeddings_list=[]
        with open(os.getenv("DICTIONARY_EMBEDDINGS"),"r") as f:
            dictionary_embeddings_list=json.load(f) 
        if dictionary_embeddings_list is None:
            return -1
        
        embedding=self.__get_embedding(word)
        #reshape dell'embedding per il calcolo della similarità 
        #(formato da una riga e da un numero di colonne calcolato automaticamente)
        reshaped_word_embedding=embedding.reshape(1,-1) 
        
        #media pesata
        similarity=0
        sum_weight=0
        similarities=[]
        for embedding in dictionary_embeddings_list.values():
            #embedding[0] contiene l'embedding stesso sottoforma di array, quindi va convertito in tensore pytorch
            dictionary_embedding=torch.tensor(embedding[0]) 
            reshaped_dictionary_embedding=dictionary_embedding.reshape(1,-1)
            #somiglianza tra embeddings calcolata come il coseno dell'angolo tra i tensori
            single_similarity=cosine_similarity(reshaped_word_embedding,reshaped_dictionary_embedding)[0][0] 
            #embedding[1] contiene il peso dell'embedding
            similarities.append((single_similarity,embedding[1])) 
                    
        #i valori di similarità vengono ordinati e vengono presi i 3 con valore più alto
        similarities.sort(key=lambda x:x[0],reverse=True)
        for i in range(4): 
            similarity+=similarities[i][0]*similarities[i][1]
            sum_weight+=similarities[i][1]
        similarity/=sum_weight
        return similarity