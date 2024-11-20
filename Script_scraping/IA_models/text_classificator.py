from tensorflow.keras.models import load_model
import tensorflow as tf
from .text_classificator_interface import Text_classificator_interface
import os

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
        input_tensor = tf.constant([text])
        return self.model.predict(input_tensor)[0,0]
    
    