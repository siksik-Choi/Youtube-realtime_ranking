#!/bin/bash

cd elasticsearch-7.6.2/
./bin/elasticsearch -d
cd

chmod +x soup.py
chmod +x app.py

./app.py

