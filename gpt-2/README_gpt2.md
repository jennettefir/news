# gpt-2
Repository: https://github.com/shawwn/gpt-2

To use this repository you should install dependencies from **requirements.txt**:
```
pip install -r requirements.txt
```
## Fine tuning on custom datasets

To retrain GPT-2 1558M model on a custom text dataset:

```
PYTHONPATH=src ./train.py --dataset <file|directory|glob> --model_name 1558M
```

If you want to precompute the dataset's encoding for multiple runs, you can instead use:

```
PYTHONPATH=src ./encode.py <file|directory|glob> /path/to/encoded.npz --model_name 1558M
PYTHONPATH=src ./train.py --dataset /path/to/encoded.npz --model_name 1558M
```

## MSR Twitter Model
To rewrite texts, the 1558M has trained on several datasets:
- https://lanwuwei.github.io/Twitter-URL-Corpus/
- https://www.microsoft.com/en-us/download/details.aspx?id=52398

These datasets were merged and then filtered using https://tfhub.dev/google/universal-sentence-encoder-large/5 и https://en.wikipedia.org/wiki/Cosine_similarity

Each dataset record contains 2 sentences: the original and the rewrited,
for example:
```
ORIGINAL_SENT: Melania Trump and Michelle Obama sit down for tea in the White House. >>>>> Michelle Obama and Melania Trump drink tea at the White House
```

The result is a dataset with 3.6k of rephrased sentences. You can download it here: https://drive.google.com/file/d/10ehetcaZkyrBQYQjR2QHD94FYhz3yiFy/view?usp=sharing

The model is available by this link: https://drive.google.com/file/d/1fEW0Vn0alPTGCLSZOIpMiUShqPUuy6RW/view?usp=sharing

## Text rewrite
**text_rewrite.py** 
is created for rewriting text. It works in such a way:
1. The text is divided into sentences using spaCy.
2. For each sentence, N rewrited sentences are generated (depending on the batch_size parameter).
3. Using USE (Universal Sentence Encoder) we determine the most appropriate sentence.

Launch example:
```
PYTHONPATH=src python3 text_rewrite.py --input_filepath {file_with_text_to_rewrite} --output_filepath {rewritten_text} --restore_from {path_to_model}
```
To start using TPU, add **--init_tpu**. parameter

## USE Model
Work with the USE model is implemented using the HTTP API, which is deployed separately in the Docker, this is due to differences in tensorflow versions.
Files required to run the API are in the use_api directory.

To start the container you should:
1. Build image: ```docker build -t {image_name} .```
2. Start the container: ```docker run -d -p 3434:8000 {image_name}```.
After that, you can access the server:
```
curl -X POST \
  'http://localhost:3434/detect_similarity?=' \
  -H 'Content-Type: application/json' \
  -d '[
	"Hello world",
	"Hello universe"
]'
```
As a result, the matrix of similarity of sentences is returned.

By default, **text_rewrite.py** refers to the server using the address http://localhost:3434/detect_similarity , but you can redefine this parameter with the environment variable **SIMILARITY_DETECT_URL**:
```
export SIMILARITY_DETECT_URL=http://{server_addr}:{server_port}/detect_similarity
```

## Rewrite docker image
It's possible to build a docker image, launch it and generate rewrite using HTTP API.
For this:
```
docker build -t {image_name} -f Dockerfile.gpu.
```
Make sure that USE model is launched and works.
Container can be started after that:
```
docker run -d --restart unless-stopped -p 8001:8000 --gpus all -e SIMILARITY_DETECT_URL={similarity_detect_url} {image_name}
```
Wait for some time until model gets loaded (status can be checked via docker logs)
Call the server after that:
```
curl -X POST \
  http://localhost:8001/text_rewrite \
  -H 'Content-Type: application/json' \
  -d '{
	"text": "Hello world!"
}'
```
Expected response:
```
{
    "output": "Hello universe!"
}
```
"output" contains generated rewrite.
