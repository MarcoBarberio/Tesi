from model_and_tokenizer import get_model_and_tokenizer
import torch
import torch.nn.functional as F
import json

dictionary = [
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
#funzione che restituisce una rappresentazione complessiva del dizionario
def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0]
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

def create_centroid():
    model,tokenizer=get_model_and_tokenizer()
    inputs = tokenizer(dictionary, padding=True, truncation=True, return_tensors="pt") #restituisce tensori di pytorch
    with torch.no_grad(): #permette di risparmiare memoria, in quanto non calcola i gradienti (non stiamo addestrando il modello)
        output=model(**inputs) #l'output del modello
    centroid = mean_pooling(output, inputs['attention_mask'])
    centroid = F.normalize(centroid, p=2, dim=1).mean(dim=0).numpy()
    centroid_list=centroid.tolist()
    with open("centroid.json","w") as f:
        json.dump(centroid_list,f)