import sys
import os
import re
import json
from pprint import pprint

#counter for tweets with unicode characters
unicodeTweetCount = 0

#python escape sequences to remove from tweets
escapes=["\\","\a","\b","\r","\n","\f","\t","\v"]

#removes non-ascii characters and escape sequences from string
#return: tweet text after removing unicode characters
def removeNonASCIIAndEscapes(text):
	global escapes
	global unicodeTweetCount
	containsUnicodeFlag=False
	result=""
	#for each tweet, clean its text to remove unicode characters
	for i in text:
		if ord(i) < 128:
			if i not in escapes:
				result+=i
		else:
			containsUnicodeFlag=True
	#if unicode characters in tweet increment global counter
	if containsUnicodeFlag:
		unicodeTweetCount+=1	
	return result

#function to parse input json line and extract tweet text and created_at fields
#return: tweetText and tweetCreateDTTM
def getTextAndCreateFields(inputText):
	tweetText=""
	tweetCreateDTTM=""
	jsonData = json.loads(inputText)
	if "text" in jsonData:
		tweetText = jsonData["text"]
		tweetText = removeNonASCIIAndEscapes(tweetText)
	if "created_at" in jsonData:
		tweetCreateDTTM = jsonData["created_at"]
	return tweetText, tweetCreateDTTM

#function to format input in required output format
#return: formatted output string
def getOutputString(tweetText, tweetCreateDTTM,unicodeTweetCount,outputFlag):
	#if flag=0 return output string for tweetText and tweetCreateDTTM
	if outputFlag==0:
		return tweetText + " " + "(timestamp:" + " " + tweetCreateDTTM + ")" +"\n"
	#if flag=1 return output string for number of tweets with unicode data
	if outputFlag==1:
		return str(unicodeTweetCount) + " tweets contained unicode."
	return None

#function to read, clean escape sequences and unicode characters and count tweets with unicode
#return : output file in required format
def cleanCountUnicodeTweets(inputFile,outputFile):
	global unicodeTweetCount
	with open(inputFile, "r") as inFile, open(outputFile, "w") as outFile:
		for line in inFile:
			#for each tweet get its cleaned text, createDTTM and write output in output format
			tweetText, tweetCreateDTTM = getTextAndCreateFields(line)
			outputString = getOutputString(tweetText,tweetCreateDTTM,0,0)
			outFile.write(outputString)
		outFile.write("\n")
		#get the number of tweets that had unicode-characters and write output
		outputString = getOutputString(None,None,unicodeTweetCount,1)
		outFile.write(outputString)

#main() driver program
def main():
	if len(sys.argv) != 3:
		print ('usage : python3 ./src/tweets_cleaned.py ./tweet_input/tweets.txt ./tweet_output/ft1.txt')
		sys.exit(1)
	inputFile = sys.argv[1]
	outputFile = sys.argv[2]
	cleanCountUnicodeTweets(inputFile,outputFile)

if __name__ == '__main__':
	main() 