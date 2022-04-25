#!/bin/bash
cat ./before.json > ./test.json &&
python3 ./fileB.py &
python3 ./fileA.py ./test.json &
sleep 2 && echo "Updating APs..." && sleep 4 && cat ./after.json > ./test.json &&
sleep 3 && pkill -P $$
