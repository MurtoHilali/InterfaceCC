#!/bin/bash

curl -O https://pioneer.yulab.org/static/predictions/very_high/human.txt
mv human.txt human-very-high.tsv

curl -O https://pioneer.yulab.org/static/predictions/high/human.txt
mv human.txt human-high.tsv