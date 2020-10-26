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
Для рерайта текстов модель 1558M дообучалась на нескольких датасетах:
- https://lanwuwei.github.io/Twitter-URL-Corpus/
- https://www.microsoft.com/en-us/download/details.aspx?id=52398

Эти датасетаы были объединены, а затем отфильтрованы с помощью https://tfhub.dev/google/universal-sentence-encoder-large/5 и https://en.wikipedia.org/wiki/Cosine_similarity

В каждой записи датасета хранится 2 предложения: оригинал и его рерайт,
например:
```
ORIGINAL_SENT: Melania Trump and Michelle Obama sit down for tea in the White House. >>>>> Michelle Obama and Melania Trump drink tea at the White House
```

В результате получился датасет, в котором есть 3.6к перефразированных предложений. Вы можете скачать его отсюда https://drive.google.com/file/d/10ehetcaZkyrBQYQjR2QHD94FYhz3yiFy/view?usp=sharing

Модель доступна по этой ссылке https://drive.google.com/file/d/1fEW0Vn0alPTGCLSZOIpMiUShqPUuy6RW/view?usp=sharing

## Text rewrite
**text_rewrite.py** 
предназначен для переписывания текста. Он работает по такому принципу:
1. Текст разбивается на предложения с помощью spaCy
2. Для каждого предложения генерируется N рерайтов (зависит от параметра batch_size)
3. С помощью USE (Universal Sentence Encoder) определяем наиболее подходящее предложение.

Пример запуска:
```
PYTHONPATH=src python3 text_rewrite.py --input_filepath {file_with_text_to_rewrite} --output_filepath {rewritten_text} --restore_from {path_to_model}
```
Для, запуска с использованием TPU, следует добавить **--init_tpu**
параметр

Работа с USE моделью введется с помощью HTTP API, который поднимается отдельно в докере, это сделано из-за различий в версиях tensorflow.
Файлы необходимые для запуска АПИ находятся в директории use_api.

Для того, что бы запустить контейнер следует
1. Собрать образ: ```docker build -t {image_name} .```
2. Запустить контейнер: ```docker run -d -p 3434:8000 {image_name}```.
После этого, вы можете обращатся к серверу:
```
curl -X POST \
  'http://localhost:3434/detect_similarity?=' \
  -H 'Content-Type: application/json' \
  -d '[
	"Hello world",
	"Hello universe"
]'
```
В результате возвращается матрица похожести предложений.

По умолчанию, **text_rewrite.py** обращается к серверу, по адресу http://localhost:3434/detect_similarity , но вы можете переопределить этот параметр с помощью переменной окружения **SIMILARITY_DETECT_URL**:
```
export SIMILARITY_DETECT_URL=http://{server_addr}:{server_port}/detect_similarity
```
