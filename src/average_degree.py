import sys
import os
import re
import json
import itertools
from pprint import pprint
from datetime import datetime 
from time import strptime
from collections import Counter

#global dictionary. Key: created at timestamp of tweet, Value: hastags in tweet
timeHashtagDictionary = dict()

#global list for current edges in graph
graphEdgesList = list()

#function to format the JSON timestamp in datetime standard format
#return: formated DTTM
def formatDTTM(tweetCreateDTTM):
	elements = tweetCreateDTTM.split(" ")
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

#function to get hashtags and created timestamp from tweet data
#return: list of hashtags in tweet and its create timestamp
def getHashtagsAndCreateFields(inputText):
	tweetHashtags = list()
	tweetCreateDTTM = ""
	jsonData = json.loads(inputText)
	#take all hashtags, make them lower case and remove duplicates
	if "entities" in jsonData:
		tweetEntities = jsonData["entities"]
		if "hashtags" in tweetEntities:
			hashtagList = tweetEntities["hashtags"]
			if hashtagList:		
				tweetHashtags = [item['text'] for item in hashtagList]
				tweetHashtags = [tag.lower() for tag in tweetHashtags]
				tweetHashtags = list(set(tweetHashtags))
	#take created_at timestamp and convert into datetime format
	if "created_at" in jsonData:
		tweetCreateDTTM = jsonData["created_at"]
		tweetCreateDTTM = formatDTTM(tweetCreateDTTM)
	return tweetHashtags, tweetCreateDTTM

#function to get all possible edges from a list of hashtags
#return: a list of edges for input tweetHashtags
def getEdges(tweetHashtags):
	tweetHashtags = sorted(set(tweetHashtags))
	return list(itertools.combinations(tweetHashtags, 2))

#function to remove invalid edges from graph
#return: updated graph
def evictInvalidEdges():
	global graphEdgesList
	global timeHashtagDictionary
	invalidTimestamps=[]
	#find invalid timestamps
	latestTimestamp = max(timeHashtagDictionary.keys())
	originalTimestamps=timeHashtagDictionary.keys()
	for timestamp in originalTimestamps:
		if not isValidTimeDifference(timestamp,latestTimestamp):
			#for each invalid tweet with respect to timestamp, find its edges and remove them from graph
			invalidHashtagsList=timeHashtagDictionary[timestamp]
			invalidEdges=getEdges(invalidHashtagsList)
			graphEdgesList=list(set(graphEdgesList)-set(invalidEdges))
			invalidTimestamps.append(timestamp)
	#update global dictionary to store only the createDTTM and hashtags of valid tweets
	timeHashtagDictionary = dict( (k, v) for k,v in timeHashtagDictionary.items() if k not in invalidTimestamps)


#function to add edges of new tweet's hashtags and remove invalid edges
#return: updated graph with new edges added to it and old edges removed
def updateGraph(tweetHashtags,tweetCreateDTTM):
	global graphEdgesList
	if len(tweetHashtags)>=2:
		edges=getEdges(tweetHashtags)
		graphEdgesList = list(set(graphEdgesList + edges))
	evictInvalidEdges()

#function to calculate the average degree of graph
#return: average degree of node
def calAvgDegreeOfGraph():	
	global graphEdgesList
	uniqueNodesInGraphList=list()
	allNodesInEdges=list()
	nodeDegreeDict=dict()
	nodeDegreeList=list()
	allNodesInEdges=list(itertools.chain(*graphEdgesList))
	#find total nodes in graph
	uniqueNodesInGraphList=list(set(allNodesInEdges))
	totalNodesInGraph=len(uniqueNodesInGraphList)
	#find sum of degrees of all nodes and average degree
	nodeDegreeDict=Counter(allNodesInEdges)
	nodeDegreeList=nodeDegreeDict.values()
	sumNodeDegree=sum(nodeDegreeList)
	if totalNodesInGraph == 0:
		avgDegree = 0
	else:	
		avgDegree=sumNodeDegree/totalNodesInGraph
	return "%.2f" % avgDegree

#driver function to read tweets and compute edges, graph and average degree of graph
#return: output file in specified format
def processTweets(inputFile,outputFile):
	global timeHashtagDictionary	
	global graphEdgesList 		
	with open(inputFile, "r") as inFile, open(outputFile, "w") as outFile:
		for line in inFile:
			#for each tweet, compute and store hashtags and createDTTM, update graph with edges from new tweet's hashtags
			#and calculate average degree of graph
			tweetHashtags, tweetCreateDTTM = getHashtagsAndCreateFields(line)
			#if there are hashtags in tweet, update the graph and record average degree in output file else do nothing	
			if tweetCreateDTTM:
				timeHashtagDictionary[tweetCreateDTTM]=tweetHashtags
			updateGraph(tweetHashtags,tweetCreateDTTM)
			avgDegree=calAvgDegreeOfGraph()
			outFile.write(str(avgDegree)+'\n')

#main() driver program
def main():
	if len(sys.argv) != 3:
		print ('usage: python3 ./src/average_degree.py ./tweet_input/tweets.txt ./tweet_output/ft2.txt')
		sys.exit(1)
	inputFile = sys.argv[1]
	outputFile = sys.argv[2]
	processTweets(inputFile,outputFile)

if __name__ == '__main__':
	main() 