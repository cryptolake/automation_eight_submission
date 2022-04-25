#!/bin/bash
cat ./before.json > ./test.json
python3 ./fileB.py & python3 ./fileA.py ./test.json & sleep 5 && cat ./after.json > ./test.json
