import numpy
from transformers import XLMRobertaTokenizer, XLMRobertaModel
import torch
import json

dizionary = [
    "Bilancio di sostenibilità",
    "Report di sostenibilità",
    "Sustainability report",
    "Corporate Social Responsibility",
    "CSR",
    "ESG report",
    "Bilancio ambientale",
    "Bilancio sociale",
    "Sostenibilità aziendale",
    "Impatto ambientale",
    "Impatto sociale",
    "Gestione ambientale",
    "Environmental report",
    "Social report",
    "Governance report",
    "Sviluppo sostenibile",
    "Sustainability management",
    "Sustainability balance",
    "Bilancio integrato",
    "Rapporto ambientale",
    "Rapporto sociale",
    "Analisi ESG",
    "Politica ambientale",
    "Politica CSR",
    "Politica ESG",
    "Governance aziendale",
    "Strategia di sostenibilità",
    "Performance ambientale",
    "Performance sociale",
    "Performance di governance",
    "Rapporto CSR",
    "Corporate governance",
    "Report di impatto",
    "Climate report",
    "Sustainable development goals",
    "SDG",
    "Green finance",
    "Green bond",
    "Decarbonizzazione",
    "Carbon footprint",
    "Neutralità climatica",
    "Riduzione emissioni",
    "Emissioni di CO2",
    "Transizione energetica",
    "Economia circolare",
    "Riciclo",
    "Rifiuti zero",
    "Risparmio energetico",
    "Energia rinnovabile",
    "Biodiversità",
    "Ripristino ambientale",
    "Economia verde",
    "Integrazione sociale",
    "Impatto positivo",
    "Responsabilità etica",
    "Investimento responsabile",
    "Valutazione ESG",
    "Materialità",
    "Coinvolgimento degli stakeholder",
    "Stakeholder engagement",
    "Trasparenza",
    "Accesso all'informazione",
    "Dichiarazione non finanziaria",
    "Diversity and inclusion",
    "Gender equality",
    "Diversità di genere",
    "Parità di genere",
    "Equità salariale",
    "Tutela ambientale",
    "Green economy",
    "Valore condiviso",
    "Resilienza aziendale",
    "Investimento sostenibile",
    "Prodotti eco-friendly",
    "Servizi eco-compatibili",
    "Compensazione delle emissioni",
    "Uso responsabile delle risorse",
    "Supply chain sostenibile",
    "Catena di fornitura sostenibile",
    "Reportistica integrata",
    "Rischi ambientali",
    "Rischi sociali",
    "Impatto comunitario",
    "Protezione della salute",
    "Sicurezza sul lavoro",
    "Ecodesign",
    "Educazione ambientale",
    "Formazione e sviluppo",
    "Wellness aziendale",
    "Progetti comunitari",
    "Filantropia aziendale",
    "Sviluppo economico locale",
    "Collaborazione con ONG",
    "Programmi di volontariato",
    "Engagement dei dipendenti",
    "Corporate citizenship",
    "Efficienza delle risorse",
    "Analisi del ciclo di vita",
    "Life Cycle Assessment",
    "Certificazione ambientale",
    "Certificazione ISO 14001",
    "Standard di sostenibilità",
    "Climate action",
    "Biodiversity report"
]

def create_centroid():
    tokenizer=XLMRobertaTokenizer.from_pretrained("xlm-roberta-base") #alcune stringhe possono essere composte da più parole separate da un token
    model=XLMRobertaModel.from_pretrained("xlm-roberta-base")
    embeddings=[]
    for word in dizionary:
        inputs=tokenizer(word,return_tensors="pt") #restituisce tensori di pytorch
        with torch.no_grad(): #permette di risparmiare memoria, in quanto non calcola i gradienti (non stiamo addestrando il modello)
            outputs=model(**inputs) #l'output del modello
            #si estraggono i vettori di embedding per ciascun token, se ne calcola la media, si eliminano dimensioni inutili e si converte il tensore torch in numpy
        word_embedding=outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
        embeddings.append(word_embedding)
    if embeddings:
        centroid=numpy.mean(embeddings,axis=0)
        centroid_list=centroid.tolist()
        with open("centroid.json","w") as f:
            json.dump(centroid_list,f)