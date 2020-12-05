#!/bin/sh

python3 -m speech-to-text
/bin/sh -c "sleep 300"
curl -s -X POST localhost:10001/quitquitquit
