import joblib
from sentence_transformers import SentenceTransformer
Encoder = SentenceTransformer('all-MiniLM-L6-v2')
Model = joblib.load('Models/log_classifier.joblib')

def classify_with_bert(log_message):
    embeddings = Encoder.encode([log_message])
    probabilities = Model.predict_proba(embeddings)[0]
    if max(probabilities) < 0.5 : 
        return "Unknown"
    return Model.predict(embeddings)[0]

