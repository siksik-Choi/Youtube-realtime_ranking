#!/bin/bash

cd elasticsearch-7.6.2/
./bin/elasticsearch -d
cd

chmod +x soup.py
chmod +x app.py

for var in 1 2 3
do
 echo start
 ./app.py
 sleep 1m
done
