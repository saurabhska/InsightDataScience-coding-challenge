import sys
import os
import re
import json
from pprint import pprint


#absolute dir the script is in
script_dir = os.path.dirname(__file__) 

#relative paths of input and output files
relativeInputPath = "tweet_input/tweets.txt"
relativeOutputPath = "tweet_output/ft1.txt"

#absolute paths of input and output files
inputFile = os.path.join(script_dir, relativeInputPath)
outputFile = os.path.join(script_dir, relativeOutputPath)

#counter for tweets with unicode characters
unicodeTweetCount = 0

#python escape sequences to remove from tweets
escapes=["\\","\a","\b","\r","\n","\f","\t","\v"]

#removes non-ascii characters and escape sequences from string
def removeNonASCIIAndEscapes(text):
	global escapes
	global unicodeTweetCount
	containsUnicodeFlag=False
	result=""
	for i in text:
		if ord(i) < 128:
			if i not in escapes:
				result+=i
		else:
			containsUnicodeFlag=True
	if containsUnicodeFlag:
		unicodeTweetCount+=1	
	return result
	#return ''.join([i if ((ord(i) < 128) and (i not in escapes)) else '' for i in text])

#function to parse input json line and extract tweet text and created_at field
def getTextAndCreateFields(inputText):
	tweetText=""
	tweetCreateDTTM=""
	jsonData = json.loads(inputText)
	if "text" in jsonData and "created_at" in jsonData:
		tweetText = jsonData["text"]
		#print(tweetText)
		tweetText = removeNonASCIIAndEscapes(tweetText)
		tweetCreateDTTM = jsonData["created_at"]
	return tweetText, tweetCreateDTTM


def getOutputString(tweetText, tweetCreateDTTM,unicodeTweetCount,outputFlag):
	if outputFlag==0:
		return tweetText + " " + "(timestamp:" + " " + tweetCreateDTTM + ")" +"\n"
	if outputFlag==1:
		return str(unicodeTweetCount) + " tweets contained unicode."
	return None

#function to read, clean escape and unicode characters and count tweets with unicode
def cleanCountUnicodeTweets(inputFile):
	global unicodeTweetCount
	with open(inputFile, "r") as inFile, open(outputFile, "w") as outFile:
		for line in inFile:
			tweetText, tweetCreateDTTM = getTextAndCreateFields(line)
			outputString = getOutputString(tweetText,tweetCreateDTTM,0,0)
			outFile.write(outputString)
		outFile.write("\n")
		outputString = getOutputString(None,None,unicodeTweetCount,1)
		outFile.write(outputString)

#main() driver program
def main():
	global inputFile
	global outputFile
	cleanCountUnicodeTweets(inputFile)

if __name__ == '__main__':
	main() 
