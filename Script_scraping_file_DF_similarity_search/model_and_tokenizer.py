from transformers import AutoTokenizer, AutoModel
model = None
tokenizer=None

def get_model_and_tokenizer():
    global model,tokenizer
    if model is None or tokenizer is None:
        model= AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
        tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
    return model,tokenizer
