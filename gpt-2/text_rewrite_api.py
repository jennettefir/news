import sys
sys.path.append('src')

import os
import numpy as np
import tensorflow as tf
import tflex


import model, sample, encoder
import requests
import json
from spacy.lang.en import English
from fastapi import FastAPI
from pydantic import BaseModel

similarity_detect_url = os.getenv('SIMILARITY_DETECT_URL', 'http://localhost:3434/detect_similarity')


def extract_sent_from_model_generated(generated):
    possible_seps = ["<|e", "ORIGINAL", ">>>>"]
    for sep in possible_seps:
        parts = generated.split(sep)
        if len(parts) > 1:
            return parts[0].strip()
    return generated.strip()


def detect_sent_similarity(sentences):
    payload = json.dumps(sentences)
    headers = {
        'Content-Type': "application/json"
    }
    response = requests.request("POST", similarity_detect_url, data=payload, headers=headers)
    return response.json()


def get_best_candidate(original, generated_raw):
    generated = [extract_sent_from_model_generated(sent) for sent in generated_raw]
    sentences = [original, *generated]
    sent_similarity = detect_sent_similarity(sentences)[0]
    first_range = [score for score in sent_similarity if 0.95 >= score >= 0.85]
    first_range.sort(reverse=True)
    if first_range:
        return sentences[sent_similarity.index(first_range[0])]
    second_range = [score for score in sent_similarity if 2 >= score > 0.95]
    second_range.sort()
    return sentences[sent_similarity.index(second_range[0])]


def add_new_line(original, res):
    if res.startswith("\n"):
        return res
    if original.startswith("\n"):
        return "\n\n" + res
    else:
        return res


app = FastAPI()
nlp = English()
nlp.add_pipe(nlp.create_pipe('sentencizer'))
model_name = os.environ.get("ML_MODEL", "msr_twitter")
restore_from = None
seed = None
batch_size = 4
length = 70
temperature = 1
top_k = 0
top_p = 1
enc = encoder.get_encoder(model_name)
hparams = model.default_hparams()
with open(os.path.join('models', model_name, 'hparams.json')) as f:
    hparams.override_from_dict(json.load(f))
sess = tf.Session(graph=tf.Graph()).__enter__()
context = tf.placeholder(tf.int32, [4, None])
np.random.seed(None)
tf.set_random_seed(None)
output = sample.sample_sequence(
    hparams=hparams, length=length,
    context=context,
    batch_size=batch_size,
    temperature=temperature, top_k=top_k, top_p=top_p
)
saver = tflex.Saver()
if restore_from is None:
    restore_from = os.path.join('models', model_name)
ckpt = tflex.latest_checkpoint(restore_from)
saver.restore(sess, ckpt)


class Article(BaseModel):
    text: str


@app.post("/text_rewrite")
def text_rewrite(
    article: Article
):
    text = article.text
    result = []
    for sent in nlp(text).sents:
        sent_text = sent.text.strip()
        if not sent_text:
            continue
        model_input = "ORIGINAL_SENT: {} >>>>>".format(sent_text)
        context_tokens = enc.encode(model_input)
        print(model_input)
        print('*' * 80)
        out = sess.run(output, feed_dict={
            context: [context_tokens for _ in range(batch_size)]
        })[:, len(context_tokens):]

        texts = []
        for i in range(batch_size):
            text = enc.decode(out[i]) + "\n"
            print("SAMPLE {}".format(i))
            print(text)
            print('-' * 80)
            texts.append(text)
        rephrased = get_best_candidate(sent_text, texts)
        rephrased = add_new_line(sent.text, rephrased)
        result.append(rephrased)
        print("REPHRASED: {}".format(rephrased))
        print('=' * 80)
    return {"output": " ".join(result)}
