#!/usr/bin/python
#-*- coding: utf-8 -*-

from Tkinter import Tk

copyData = Tk().clipboard_get()
copyData = copyData.encode("utf-8").strip()

pageData = {}
pageData['until date'] = copyData.split("—")[1].split("\n")[0]

print copyData
topData = copyData.split("—")[1].split("\n")[3]
pageData["posts"] = int(topData.split("posts")[0])
pageData["authors"] = int(topData.split("posts")[1].split("authors")[0])
pageData["commenters"] = int(topData.split("authors")[1].split("commenters")[0])
pageData["reactors"] = int(topData.split("commenters")[1].split("reactors")[0])

afterGraphIdx = copyData.split("\n").index("Total/Per post")

print copyData.split("\n")[afterGraphIdx+1]

# def numSpliter(joinedNum, denom):
	

print pageData