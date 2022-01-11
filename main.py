import sys
import os
import subprocess

# In case you don't have these libraries already installed
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
install("pandas")
install("numpy")
install("openpyxl")
install("lxml")

import openpyxl
import pandas as pd
import numpy
# importing element tree
import xml.etree.ElementTree as ET

# Stores the file names corresponding to the documents
# Excel Files if you wish
years2010Files = ['2010_990.xml.xlsx', '2011_990.xml.xlsx', '2012_990.xml.xlsx', '2013_990.xml.xlsx',
                      '2014_990.xml.xlsx', '2015_990.xml.xlsx', '2016_990.xml.xlsx', '2017_990.xml.xlsx',
                      '2018_990.xml.xlsx', '2019_990.xml.xlsx', '2020_990.xml.xlsx']

years2010FilesXML = ['2010_990.xml', '2011_990.xml', '2012_990.xml', '2013_990.xml',
                      '2014_990.xml', '2015_990.xml', '2016_990.xml', '2017_990.xml',
                      '2018_990.xml', '2019_990.xml', '2020_990.xml']

years2010Roots = []
## ^^For note, https://conversiontools.io/convert/xml-to-excel, was used to generate these, API can be used if desired
## But batched submission can occur when archieving the documents to be converted

# Stores the associated pandas dataframe (just a clever device to allow easy reading of the xlsx file
years2010 = []
for i in range(len(years2010Files)):
    years2010.append(ET.parse(years2010FilesXML[i]))

#Get root of XML file (basically, data is either an element or a category for data)
# So, in this document return is the root which has a header and data, header describes the cateogory
#   we only care about the data for the most part
# years2010[index] => Get XML data structure of year 2010 + index, note: 10 for 2020
currentNode = years2010[0].getroot()
# print the attributes of the first category

treeProgression = []

def subRoutine(node):
    categories = ""
    for i in node[1]:
        temp = str(i)
        if "<Element '{http://www.irs.gov/efile}" in temp:
            temp = temp[26:]
        if "gov/efile}" in temp:
            temp = temp[10:]
        if "' at" in temp:
            indexToRemove = temp.index('\'')
            temp = temp[:indexToRemove]
        categories += temp + " | "
    print(categories)

def printSubCategories(node):
    if node == None:
        return
    try:
        categories = ""
        if("ReturnHeader" in str(node[0])):
            subRoutine(node)
            return
        for i in node:
            temp = str(i)
            if "<Element '{http://www.irs.gov/efile}" in temp:
                temp = temp[26:]
            if "gov/efile}" in temp:
                temp = temp[10:]
            if "' at" in temp:
                indexToRemove = temp.index('\'')
                temp = temp[:indexToRemove]
            categories += temp + " | "
        print(categories)
    except:
        subRoutine(node)
        pass


def findCateogryIndex(node, title):
    occurences = 0
    index = -1
    if "IRS990" in title:
        values = node[1]
        for i in range(len(values)):
            if title in str(values[i]):
                if (occurences == 0):
                    index = i
                occurences += 1
    else:
        values = node
        for i in range(len(values)):
            if title in str(values[i]):
                if (occurences == 0):
                    index = i
                occurences += 1
    if occurences > 1 and "Schedule" not in title and "IRS990" not in title:
        print("\n\nWARNING: Multiple Entries of this cateogry, will return first usage, type startingNode = goBack() first to"
              " \nsave your progress in the tree, and type tempNode = goToCateogryIndexed(startingNode, title, num) to get"
              " \nthe num-th instance of the title\n\n")
    return index

def goToCateogryIndexed(node, title, num):
    num = num - 1
    index = -1
    for i in range(len(node)):
        if title in str(node[i]):
            if(num == 0):
                index = i
                num -= 1
            else:
                num -= 1
    return node[index]

def getOccurences(node, title):
    occurences = 0
    for i in range(len(node)):
        if title in str(node[i]):
            occurences += 1
    return occurences

def goBack():
    temp = treeProgression[len(treeProgression)-1]
    treeProgression.pop()
    return temp

def goToCateogry(node, title):
    global treeProgression
    treeProgression.append(node)
    index = findCateogryIndex(node, title)
    if "IRS990" in title:
        return node[1][index]
    else:
        if(len(node[index]) == 0):
            print(title, " | Value: ", node[index].text)
            return node[index].text
        return node[index]

def printAllOccurences(node, title, subcategoriesGiven):
    goUpToOccurences = getOccurences(node, title)
    for i in range(1, goUpToOccurences + 1):
        currentNodeTemp = goToCateogryIndexed(node, title, i)
        for j in subcategoriesGiven:
            randomVar = goToCateogry(currentNodeTemp, j)

def getAllOccurences(node, title, subcategoriesGiven):
    result = []
    goUpToOccurences = getOccurences(node, title)
    for i in range(1, goUpToOccurences + 1):
        here = []
        currentNodeTemp = goToCateogryIndexed(node, title, i)
        for j in subcategoriesGiven:
            randomVar = goToCateogry(currentNodeTemp, j)
            here.append(randomVar)
        result.append(here)
    return result

# let's see what categories the IRS document for 2010 has
printSubCategories(currentNode)

# let's look at IRS990 instead
currentNodeTemp = goToCateogry(currentNode, "IRS990")
printSubCategories(currentNodeTemp)

# You Know, GrossReceipts sounds interesting...
currentNodeTemp = goToCateogry(currentNodeTemp, "GrossReceipts")
printSubCategories(currentNodeTemp)

# That was kind of boring, what about Form990PartVIISectionA of the IRS990 tax document for 2010?
currentNodeTemp = goToCateogry(currentNode, "IRS990")
currentNode = currentNodeTemp
currentNodeTemp = goToCateogry(currentNodeTemp, "Form990PartVIISectionA")
printSubCategories(currentNodeTemp)

# Oh, repeated Category it says, we got the first entry, let's make sure we can get to the other instances
startingIndex = goBack()
# now, we can see what the name of the first person is and, idk, their average hours per week which, I assume, are values
randomVar = goToCateogry(currentNodeTemp, "NamePerson")
randomVar = goToCateogry(currentNodeTemp, "AverageHoursPerWeek")

# Who is the 2nd person?
currentNodeTemp = goToCateogryIndexed(startingIndex, "Form990PartVIISectionA", 2)
randomVar = goToCateogry(currentNodeTemp, "NamePerson")
randomVar = goToCateogry(currentNodeTemp, "AverageHoursPerWeek")

print("---------------------------------------------------------------------------------------------")
# Sure wish there was a way to automate this...oh wait...Dylan has got that covered
subCategories = ["NamePerson", "AverageHoursPerWeek"]
printAllOccurences(startingIndex, "Form990PartVIISectionA", subCategories)
# Note, getAllOccurences for a list of the results (each entry is a list of all the requested values per person)