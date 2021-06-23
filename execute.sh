#!/bin/bash

cd
cd elasticsearch-7.6.2/
./bin/elasticsearch -d
cd

cd osp_fri_5
chmod +x soup.py
chmod +x app.py

./app.py
