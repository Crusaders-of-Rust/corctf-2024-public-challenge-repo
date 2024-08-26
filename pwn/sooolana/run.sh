#!/bin/bash

input_string=""

IFS= read -r -d '|' input_string
echo "$input_string" | stdbuf -i0 -o0 -e0 ./challenge
