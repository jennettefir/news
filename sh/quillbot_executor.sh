#!/bin/bash
export SCRAPY_PROJECT=paraphrase_services
echo "poetry run scrapy crawl quillbot -a source=$1"