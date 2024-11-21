from tensorflow.keras.models import load_model
import tensorflow as tf
from .text_classificator_interface import Text_classificator_interface
import os
from utilities import download_pdf,get_pdf_text

class Text_classicator(Text_classificator_interface):
    #il modello deve essere creato in singleton. 
    _instance = None 
    def __new__(cls): 
        #Viene chiamato da init per istanziare una istanza senza attributi
        if cls._instance is None:
            cls._instance = super(Text_classicator, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        #nel caso sia la prima volta che viene chiamato il costruttore l'istanza non ha attributi
        if not hasattr(self, 'model'): 
            def custom_standardization(input_data):
                lowercase = tf.strings.lower(input_data)
                stripped_html = tf.strings.regex_replace(lowercase, '<br />', ' ')
                sanitized_text = tf.strings.regex_replace(
                    stripped_html, r'[^a-zA-Z0-9\s]', '') 
                return sanitized_text
            self.model =load_model(
                    os.getenv("TEXT_CLASSIFICATOR_PATH"),
                    custom_objects={"custom_standardization": custom_standardization})

    def get_prediction(self, text):
        #fa la predizione di una sola parola
        return self.model.predict(tf.constant([text]))[0,0]
    
    def get_prediction_from_file(self,file_url):
        #fa la predizione su un intero file
        predictions=[]
        pdf_file=download_pdf(file_url)
        if not pdf_file:
            return 0 # se il file è vuoto non è un bilancio di sostenibilità
        file_text=get_pdf_text(pdf_file)
        if not file_text:
            return 0
        #si fanno predizioni su sottostringhe di massimo 5000 caratteri
        chunk_size=5000
        for i in range(0,len(file_text),chunk_size):
            predictions.append(self.get_prediction(file_text[i:chunk_size+i]))
        
        if len(predictions)<3:
            return 0 # un pdf composto da meno di 15000 caratteri non può essere un bilancio di sostenibilità
        
        #si calcola la predizione su una media delle migliori 3 predizioni
        predictions.sort()
        
        prediction=sum(predictions[0:2]) / 3
        return prediction