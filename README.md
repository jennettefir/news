### Requirements
To run translations/service based paraphrasing:  
python ^3.6 (3.8 is preferable)  
poetry

## setup env
```bash
SCRAPY_PROJECT=articles_scrapers|paraphrase_services

MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=user
MYSQL_PASSWORD=12345678
MYSQL_DATABASE=nlg-articles

TEXTFILE_STORE_PATH='./files'
RSS_FEED_URLS="https://rss.nytimes.com/services/xml/rss/nyt/US.xml
https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml
https://rss.nytimes.com/services/xml/rss/nyt/Science.xml
https://rss.nytimes.com/services/xml/rss/nyt/Movies.xml
https://rss.nytimes.com/services/xml/rss/nyt/NYRegion.xml"

PROXIES="https://proxy1.com:9966
https://proxy2.com:9966"

LOG_LEVEL="DEBUG"
RETRY_TIMES=2
CONCURRENT_REQUESTS=16

GPT2_MODEL_API="http://localhost:8000"
```

### Install  
```BASH
# build the docker
docker build -t articles .

# to translate, put a file in in ./to_do/file.txt local folder
# run translator

docker run --rm -it \
    -v $(pwd)/to_do:/root/news/nlg-articles-rewriter-develop/to_do \
    -e METHOD=rewrite_translate \
    news:latest

# to paraphrase, put content in ./to_do folder
# run paraphrase
docker run --rm -it \
    -v $(pwd)/to_do:/root/news/nlg-articles-rewriter-develop/to_do \
    -e METHOD=paraphrase_services \
    news:latest


# to articles_scrapers, put content in ./to_do folder
# run articles_scrapers
docker run --rm -it \
    -v $(pwd)/to_do:/root/news/nlg-articles-rewriter-develop/to_do \
    -e METHOD=articles_scrapers \
    news:latest

```

##### Run rewriting via translate transitions  
by default bing and google translators are used with following sequence:  
EN -> DE -> ES -> DE -> EN (Bing -> Google -> Bing -> Google)
```
poetry run python rewrite_translate.py path_to_input_file.txt
```
"set SCRAPY_PROJECT=articles_scrapers" or  "set SCRAPY_PROJECT=paraphrase_services" for windows

##### Run rewriting via quillbot service
```
export SCRAPY_PROJECT=paraphrase_services
poetry run scrapy crawl quillbot -a source=path_to_input_file.txt
```

##### Run nytimes article scraper
Script scrapes RSS feed by links declared in .env variable "RSS_FEED_URLS". It then stores the data in database, "articles" table. 

Need to create .env file. See example in .env.example.

run alembic migrations and set **SCRAPY_PROJECT** environment variable:
```
alembic upgrade head
export SCRAPY_PROJECT=articles_scrapers
```

Run nytimesbot:
```
scrapy crawl nytimesbot
```

##### GPT2
GPT-2 management is done via HTTP API. More details about the model and its configurations can be gound in src/gpt-2/README.md

##### Sending rewrite articles to Wordpress API
Command generate_rewrite_command sends the rewrites.
Before launch, it's required to create a file endpoints.config.json by an example of endpoints.config.example.json
Make sure that the variable **SCRAPY_PROJECT** is set to "articles_scrapers"

After that run the command:
```
poetry run scrapy generate_rewrite_command --rewrite_type=translate --num_workers=1
```
**rewrite_type** - rewrite type (gpt2, translate, quillbot)
**num_workers** - the number of simultaneously processing articles. Not recommended to set it > 1, unless reliable proxies have been connected.

Command picks all unprocessed articles from the database based on the selected type, generates rewrite for it and sends to API endpoints stated in "endpoints.config.json" file. 

"rewrites" table stores processing status of the article. 
