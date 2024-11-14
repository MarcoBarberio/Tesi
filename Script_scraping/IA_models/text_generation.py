from transformers import AutoTokenizer, AutoModelForCausalLM
from .text_generation_interface import Text_generator_interface
import os
import torch.cuda as cuda
class Text_generator(Text_generator_interface):
     #il modello deve essere creato in singleton. 
    _instance = None 
    def __new__(cls): 
        #Viene chiamato da init per istanziare una istanza senza attributi
        if cls._instance is None:
            cls._instance = super(Text_generator, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        #nel caso sia la prima volta che viene chiamato il costruttore l'istanza non ha attributi
        if not hasattr(self, 'model'): 
            self.model = AutoModelForCausalLM.from_pretrained("google/gemma-2-2b-it")
            # con cuda si sposta il modello sulla gpu se abilitata
            if os.getenv("USE_GPU"): 
                if cuda.is_available():
                    self.model.to("cuda")
            self.tokenizer = AutoTokenizer.from_pretrained("google/gemma-2-2b-it")
            self.tokenizer.pad_token_id=self.tokenizer.eos_token_id
    
    def query(self,prompt):
        # si prepara l'input tokenizzandolo e trasformandolo in tensori di torch
        # con cuda si sposta il carico delle operazioni sulla gpu se abilitata
        input=self.tokenizer(prompt,return_tensors="pt",padding=True)
        # si prepara l'output. La temperatura è settata a 0 e non supporta sampling,
        # quindi le risposte generate saranno sempre quelle più probabili, senza casualità
        output=self.model.generate(
            input.input_ids,
            attention_mask=input.attention_mask,
            max_new_tokens=100,
            temperature=0,
            do_sample=False,
            top_p=0,
        )
        # output è un insieme di token, quindi va decodificato
        return self.tokenizer.decode(output[0], skip_special_tokens=True)