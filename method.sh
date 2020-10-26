#!/bin/bash
# Author:       Andrew J. S. 2020
# License:      GPLv2

cd /root/news/nlg-articles-rewriter-develop/

case "${METHOD}" in
    rewrite_translate )     poetry run python rewrite_translate.py "./to_do/${FILE_NAME}"
        ;;
    get_news )              python news.py "${OVERRIDE}"
        ;;
    paraphrase_services )   export SCRAPY_PROJECT=paraphrase_services
                            poetry run scrapy crawl quillbot -a source="./to_do/${FILE_NAME}"
        ;;
    articles_scrapers )     alembic upgrade head
                            export SCRAPY_PROJECT=articles_scrapers
                            scrapy crawl nytimesbot
        ;;
    * )                     echo "Missing something to do"
        ;;
esac

    