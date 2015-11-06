#!/usr/bin/env bash

# Shell script to execute programs, with the input directory tweet_input and output the files in the directory tweet_output
python3 ./src/tweets_cleaned.py ./tweet_input/tweets.txt ./tweet_output/ft1.txt
python3 ./src/average_degree.py ./tweet_input/tweets.txt ./tweet_output/ft2.txt
