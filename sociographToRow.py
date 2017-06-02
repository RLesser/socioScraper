#!/usr/bin/python
#-*- coding: utf-8 -*-

from Tkinter import Tk
import gspread


copyData = Tk().clipboard_get()
copyData = copyData.encode("utf-8").strip()

pageData = {}
pageData["until date"] = copyData.split("—")[1].split("\n")[0]

# print copyData
topData = copyData.split("—")[1].split("\n")[3]
pageData["posts"] = int(topData.split("posts")[0])
pageData["authors"] = int(topData.split("posts")[1].split("authors")[0])
pageData["commenters"] = int(topData.split("authors")[1].split("commenters")[0])
pageData["reactors"] = int(topData.split("commenters")[1].split("reactors")[0])

afterGraphIdx = copyData.split("\n").index("Total/Per post")

def numSpliter(joinedNumStr, denom):
	for idx in range(1,len(joinedNumStr)):
		if int(joinedNumStr[:idx])/denom == int(joinedNumStr[idx:]):
			return idx
	print "numSpliter ERROR!"
	exit(1)

rawReactionsNum = copyData.split("\n")[afterGraphIdx+1]
reactionsSplit = numSpliter(rawReactionsNum, pageData["posts"])
pageData["reactions"] = int(rawReactionsNum[:reactionsSplit])

rawSharesNum = copyData.split("\n")[afterGraphIdx+4]
sharesSplit = numSpliter(rawSharesNum, pageData["posts"])
pageData["shares"] = int(rawSharesNum[:sharesSplit])

rawCommentsNum = copyData.split("\n")[afterGraphIdx+7]
commentsSplit = numSpliter(rawCommentsNum, pageData["posts"])
pageData["comments"] = int(rawCommentsNum[:commentsSplit])

pageData["photos"] = copyData.split("\n")[afterGraphIdx+11]
pageData["videos"] = copyData.split("\n")[afterGraphIdx+14]
pageData["links"] = copyData.split("\n")[afterGraphIdx+17]
pageData["statuses"] = copyData.split("\n")[afterGraphIdx+20]
pageData["events"] = copyData.split("\n")[afterGraphIdx+23]

rankingsStartIdx = copyData.split("\n").index("incoming	Comment likes in")+2
rankingsEndIdx = copyData.split("\n").index("Next page")

rankingData = copyData.split("\n")[rankingsStartIdx:rankingsEndIdx]

# print rankingData

rankTupleList = []

for idx in range(0,len(rankingData),5):
	rankTupleList.append((rankingData[idx], int(rankingData[idx+2])))

print rankTupleList

pageData['rankings'] = rankTupleList

# idx = rankingsStartIdx
# while idx < rankingsEndIdx:


print pageData