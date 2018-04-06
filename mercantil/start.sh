#!/bin/bash
service tor start
service privoxy start
scrapy crawl mercantil36 -o mercantil.csv
