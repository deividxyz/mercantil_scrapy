#!/bin/bash
echo Iniciando tor...
service tor start
sleep 5
echo Iniciando privoxy...
service privoxy start
sleep 5
echo Calentando motores...
sleep 3
scrapy crawl mercantil36 -o mercantil.csv
