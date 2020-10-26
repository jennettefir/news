import numpy as np
import tensorflow_hub as hub

from fastapi import FastAPI
from sklearn.metrics.pairwise import cosine_similarity


def cos_sim(input_vectors):
    similarity = cosine_similarity(input_vectors)
    return similarity


app = FastAPI()
model = hub.load("https://tfhub.dev/google/universal-sentence-encoder-large/5")


@app.post("/detect_similarity")
def detect_similarity(sentences: list):
    embeddings = model(sentences)
    similarity_matrix = cos_sim(np.array(embeddings))
    return similarity_matrix.astype(float).tolist()
