#!/usr/bin/python
#-*- coding: utf-8 -*-

from Tkinter import Tk
import gspread
from gspread.utils import a1_to_rowcol, rowcol_to_a1
from oauth2client.service_account import ServiceAccountCredentials


def getPageData(copyData):
	copyData = copyData.encode("utf-8").strip()

	pageData = {}
	pageData["until date"] = copyData.split("—")[1].split("\n")[1]
	print pageData["until date"]

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

	rankTupleList = []

	for idx in range(0,len(rankingData),5):
		rankTupleList.append((rankingData[idx], int(rankingData[idx+2])))

	pageData['rankings'] = rankTupleList

	return pageData


def openClient():
	scope = ['https://spreadsheets.google.com/feeds']
	creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
	client = gspread.authorize(creds)
	return client

def placeRowInSheet(pageData, client):
	print "Populating data sheet"
	dataSheet = client.open("socioscrape").get_worksheet(0)
	labels = [x for x in dataSheet.row_values(1)[1:] if x]
	dateRow = dataSheet.find(pageData['until date']).row
	col = 2
	for label in labels:
		dataSheet.update_cell(dateRow, col, pageData[label])
		col += 1
	
def placeRankingsInSheet(pageData, client):
	print "Populating ranking sheet"
	rankingSheet = client.open("socioscrape").get_worksheet(1)
	labels = [x for x in rankingSheet.row_values(1)[1:] if x] 
	dateRow = rankingSheet.find(pageData['until date']).row
	rankings = pageData['rankings']
	labelCount = len(labels) + 1
	for ranking in rankings:
		try:
			nameCol = labels.index(ranking[0])
		except Exception as e:
			labelCount += 1
			if labelCount == rankingSheet.col_count:
				rankingSheet.resize(cols = labelCount * 2)
			rankingSheet.update_cell(1, labelCount, ranking[0])
			rankingSheet.update_cell(dateRow, labelCount, ranking[1])
		else:
			rankingSheet.update_cell(dateRow, nameCol+2, ranking[1])
			




if __name__ == '__main__':
	copyData = Tk().clipboard_get()
	client = openClient()
	pageData = getPageData(copyData)
	placeRowInSheet(pageData, client)
	placeRankingsInSheet(pageData, client)
