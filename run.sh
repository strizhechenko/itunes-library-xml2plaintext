#!/bin/bash

python parser.py > media.tmp
sort -u media.tmp > plaintext_library.txt
rm -f media.tmp
