import sys
import os
import re
import json
import itertools
from pprint import pprint
from datetime import datetime 
from time import strptime
from collections import Counter

#absolute dir the script is in
script_dir = os.path.dirname(__file__) 

#relative paths of input and output files
relativeInputPath = "tweet_input/tweets.txt"
relativeOutputPath = "tweet_output/ft2.txt"

#absolute paths of input and output files
inputFile = os.path.join(script_dir, relativeInputPath)
outputFile = os.path.join(script_dir, relativeOutputPath)

#dictionary to store timestamp-hashtaglist for every tweet
timeHashtagDictionary = dict()

#List of edges in graph
graphEdgesList = list()

#function to format the JSON timestamp in datetime standard format
def formatDTTM(tweetCreateDTTM):
	elements = tweetCreateDTTM.split(" ")
	#print(elements)
	year=int(elements[-1])
	month=int(strptime(elements[1],'%b').tm_mon)
	date=int(elements[2])
	time=elements[3].split(":")
	hour=int(time[0])
	minute=int(time[1])
	second=int(time[2])
	return datetime(year,month,date,hour,minute,second)

#function to check if the time difference between timestamps is less than 60 seconds
def isValidTimeDifference(timestamp1,timestamp2):
	difference = (timestamp2-timestamp1).total_seconds()	
	if difference < 60:
		return True
	return False

#function to get hashtags and created timestamp from tweet
def getHashtagsAndCreateFields(inputText):
	tweetHashtags = list()
	tweetCreateDTTM = ""
	jsonData = json.loads(inputText)
	#print('abs')
	if "entities" in jsonData and "created_at" in jsonData:
		tweetEntities = jsonData["entities"]
		if "hashtags" in tweetEntities:
			hashtagList = tweetEntities["hashtags"]
			tweetCreateDTTM = jsonData["created_at"]
			if hashtagList:		
				tweetHashtags = [ item['text'] for item in hashtagList]
				tweetHashtags = [tag.lower() for tag in tweetHashtags]
				tweetHashtags = list(set(tweetHashtags))
				tweetCreateDTTM = formatDTTM(tweetCreateDTTM)
	return tweetHashtags, tweetCreateDTTM

#function to get all possible edges from a list of hashtags
def getEdges(tweetHashtags):
	tweetHashtags = sorted(set(tweetHashtags))
	return list(itertools.combinations(tweetHashtags, 2))

def evictInvalidEdges():
	global graphEdgesList
	global timeHashtagDictionary
	invalidTimestamps=[]
	latestTimestamp = max(timeHashtagDictionary.keys())
	originalTimestamps=timeHashtagDictionary.keys()
	for timestamp in originalTimestamps:
		if not isValidTimeDifference(timestamp,latestTimestamp):
			invalidHashtagsList=timeHashtagDictionary[timestamp]
			invalidEdges=getEdges(invalidHashtagsList)
			#print("removing invalidEdges...")
			#print(invalidEdges)
			graphEdgesList=list(set(graphEdgesList)-set(invalidEdges))
			invalidTimestamps.append(timestamp)
	#print("invalidTimestamps")
	#print(invalidTimestamps)
	#print("before")
	#print(timeHashtagDictionary)
	timeHashtagDictionary = dict( (k, v) for k,v in timeHashtagDictionary.items() if k not in invalidTimestamps)
	#print("after")
	#print(timeHashtagDictionary)


#function to add edges of new tweet's hashtags, remove invalid edges and calculate average degree of graph
def updateGraph(tweetHashtags,tweetCreateDTTM):
	global graphEdgesList
	#print("tweetHashtags")
	#print(tweetHashtags)
	#print("tweetCreateDTTM")
	#print(tweetCreateDTTM)
	if len(tweetHashtags)>=2:
		edges=getEdges(tweetHashtags)
		#print("edges")
		#print(edges)
		graphEdgesList = list(set(graphEdgesList + edges))
		#print("graphEdgesList")
		#print(graphEdgesList)
	evictInvalidEdges()

#function to calculate the average degree of graph
def calAvgDegreeOfGraph():	
	global graphEdgesList
	uniqueNodesInGraphList=list()
	allNodesInEdges=list()
	nodeDegreeDict=dict()
	nodeDegreeList=list()
	allNodesInEdges=list(itertools.chain(*graphEdgesList))
	uniqueNodesInGraphList=list(set(allNodesInEdges))
	totalNodesInGraph=len(uniqueNodesInGraphList)
	nodeDegreeDict=Counter(allNodesInEdges)
	nodeDegreeList=nodeDegreeDict.values()
	sumNodeDegree=sum(nodeDegreeList)
	avgDegree=sumNodeDegree/totalNodesInGraph
	return "%.2f" % avgDegree


#function to read, clean escape and unicode characters and count tweets with unicode
def processTweets(inputFile):
	global timeHashtagDictionary
	global graphEdgesList
	with open(inputFile, "r") as inFile, open(outputFile, "w") as outFile:
		for line in inFile:
			tweetHashtags, tweetCreateDTTM = getHashtagsAndCreateFields(line)
			#print(tweetHashtags)
			#print(tweetCreateDTTM)
			timeHashtagDictionary[tweetCreateDTTM]=tweetHashtags
			updateGraph(tweetHashtags,tweetCreateDTTM)
			avgDegree=calAvgDegreeOfGraph()
			print(avgDegree)
	print(graphEdgesList)

#main() driver program
def main():
	global inputFile
	global outputFile
	processTweets(inputFile)

if __name__ == '__main__':
	main() 
