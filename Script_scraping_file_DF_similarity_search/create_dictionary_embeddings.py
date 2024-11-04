from model_and_tokenizer import get_model_and_tokenizer
import torch
import torch.nn.functional as F
import json

dictionary= [
    ("Bilancio di sostenibilità", 5),
    ("Report di sostenibilità", 5),
    ("Sustainability report", 5),
    ("Corporate Social Responsibility", 4),
    ("CSR", 4),
    ("ESG report", 4),
    ("Bilancio ambientale", 4),
    ("Bilancio sociale", 4),
    ("Sostenibilità aziendale", 5),
    ("Impatto ambientale", 4),
    ("Impatto sociale", 4),
    ("Gestione ambientale", 4),
    ("Environmental report", 4),
    ("Social report", 4),
    ("Governance report", 3),
    ("Sviluppo sostenibile", 5),
    ("Sustainability management", 4),
    ("Sustainability balance", 4),
    ("Bilancio integrato", 4),
    ("Rapporto ambientale", 4),
    ("Rapporto sociale", 4),
    ("Analisi ESG", 4),
    ("Politica ambientale", 4),
    ("Politica CSR", 4),
    ("Politica ESG", 4),
    ("Governance aziendale", 3),
    ("Strategia di sostenibilità", 5),
    ("Performance ambientale", 4),
    ("Performance sociale", 4),
    ("Performance di governance", 3),
    ("Rapporto CSR", 4),
    ("Corporate governance", 3),
    ("Report di impatto", 4),
    ("Climate report", 4),
    ("Sustainable development goals", 5),
    ("SDG", 5),
    ("Green finance", 4),
    ("Green bond", 4),
    ("Decarbonizzazione", 4),
    ("Carbon footprint", 4),
    ("Neutralità climatica", 5),
    ("Riduzione emissioni", 4),
    ("Emissioni di CO2", 4),
    ("Transizione energetica", 5),
    ("Economia circolare", 4),
    ("Riciclo", 3),
    ("Rifiuti zero", 4),
    ("Risparmio energetico", 4),
    ("Energia rinnovabile", 5),
    ("Biodiversità", 4),
    ("Ripristino ambientale", 4),
    ("Economia verde", 4),
    ("Integrazione sociale", 3),
    ("Impatto positivo", 4),
    ("Responsabilità etica", 4),
    ("Investimento responsabile", 4),
    ("Valutazione ESG", 4),
    ("Materialità", 3),
    ("Coinvolgimento degli stakeholder", 3),
    ("Stakeholder engagement", 3),
    ("Trasparenza", 4),
    ("Accesso all'informazione", 3),
    ("Dichiarazione non finanziaria", 3),
    ("Diversity and inclusion", 3),
    ("Gender equality", 3),
    ("Diversità di genere", 3),
    ("Parità di genere", 3),
    ("Equità salariale", 3),
    ("Tutela ambientale", 4),
    ("Green economy", 4),
    ("Valore condiviso", 4),
    ("Resilienza aziendale", 3),
    ("Investimento sostenibile", 4),
    ("Prodotti eco-friendly", 3),
    ("Servizi eco-compatibili", 3),
    ("Compensazione delle emissioni", 4),
    ("Uso responsabile delle risorse", 4),
    ("Supply chain sostenibile", 4),
    ("Catena di fornitura sostenibile", 4),
    ("Reportistica integrata", 4),
    ("Rischi ambientali", 4),
    ("Rischi sociali", 4),
    ("Impatto comunitario", 4),
    ("Protezione della salute", 4),
    ("Sicurezza sul lavoro", 3),
    ("Ecodesign", 3),
    ("Educazione ambientale", 4),
    ("Formazione e sviluppo", 3),
    ("Wellness aziendale", 3),
    ("Progetti comunitari", 3),
    ("Filantropia aziendale", 3),
    ("Sviluppo economico locale", 3),
    ("Collaborazione con ONG", 3),
    ("Programmi di volontariato", 3),
    ("Engagement dei dipendenti", 3),
    ("Corporate citizenship", 3),
    ("Efficienza delle risorse", 4),
    ("Analisi del ciclo di vita", 4),
    ("Life Cycle Assessment", 4),
    ("Certificazione ambientale", 4),
    ("Certificazione ISO 14001", 4),
    ("Standard di sostenibilità", 4),
    ("Climate action", 4),
    ("Biodiversity report", 4)
]

#funzione che restituisce una rappresentazione complessiva del dizionario
def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0]
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

def create_dictionary_embeddings():
    model,tokenizer=get_model_and_tokenizer()
    embeddings={}
    for word,rate in dictionary:
        input = tokenizer(word, padding=True, truncation=True, return_tensors="pt") #restituisce tensori di pytorch
        with torch.no_grad(): #permette di risparmiare memoria, in quanto non calcola i gradienti (non stiamo addestrando il modello)
            output=model(**input) #l'output del modello
        embedding = mean_pooling(output, input['attention_mask'])
        embedding = F.normalize(embedding, p=2, dim=1).squeeze().numpy()
        embeddings[word]=(embedding.tolist(),rate)
    with open("dictionary_embeddings.json","w") as f:
        json.dump(embeddings,f)