from transformers import AutoTokenizer, LlamaForCausalLM
from .text_generation_interface import Text_generator_interface

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
            self.model = LlamaForCausalLM.from_pretrained("meta-llama/Llama-3.2-1B")
            self.tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-1B")
            self.tokenizer.pad_token_id=self.tokenizer.eos_token_id
    
    def query(self,prompt):
        # si prepara l'input tokenizzandolo e trasformandolo in tensori di torch
        input=self.tokenizer(prompt,return_tensors="pt",padding=True)
        # si prepara l'output. La temperatura è settata a 0 e non supporta sampling,
        # quindi le risposte generate saranno sempre quelle più probabili, senza casualità
        output=self.model.generate(
            input.input_ids,
            attention_mask=input.attention_mask,
            max_new_tokens=100,
            temperature=0.0,
            top_p=1,
            do_sample=False
        )
        return self.tokenizer.decode(output[0], skip_special_tokens=True)