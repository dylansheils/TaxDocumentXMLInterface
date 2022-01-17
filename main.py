RPISchool = True # Set to false if you want your school's data
                 # MAKE SURE TO DOWNLOAD ALL XML Tax Documents you want for YOUR school
                 #


#################################### SKIP ALL THIS NERD STUFF ####################################################


import sys
import os
import subprocess

# In case you don't have these libraries already installed
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
## Uncomment to add necessary libraries, if you are NOT using Spyder
#install("pandas")
#install("numpy")
#install("openpyxl")
#install("lxml")

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

def findCateogryIndexQuiet(node, title):
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

def goToCateogryQuiet(node, title):
    global treeProgression
    treeProgression.append(node)
    index = findCateogryIndexQuiet(node, title)
    if "IRS990" in title:
        return node[1][index]
    else:
        if(len(node[index]) == 0):
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
            randomVar = goToCateogryQuiet(currentNodeTemp, j)
            here.append(randomVar)
        result.append(here)
    return result























########################### YOUR APPLICATION ######################################

###########################################
# HOW TO NAVIGATE
###########################################
# 0-9 => 2010 + index
currentNode = years2010[0].getroot()
# let's see what categories the IRS document for 2010 has
printSubCategories(currentNode)

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


##############################
# Print out Repeated Cateogry
##############################
print("--------------------------------ALL PEOPLE IN 2010 990 Part VII Section A-------------------------------------------------------------")
print("990 Part VII Section A: Disclose the names of the organization’s officers, directors, trustees and associated hours for Nonprofits")
# Sure wish there was a way to automate this...oh wait...Dylan has got that covered
subCategories = ["NamePerson", "AverageHoursPerWeek"]
printAllOccurences(startingIndex, "Form990PartVIISectionA", subCategories)


##############################
# Extract Data from ALL years
##############################

# Because there might be repetitions
peopleHoursWorked = {}
# Let's culminate this data from multiple different tax forms
for i in range(len(years2010)):
    # 0-9 => 2010 + index
    currentNode = years2010[i].getroot()

    #Tell it how to get to section (remember it gave us that warning, how about we don't get that anymore by using Quiet functions?)
    currentNodeTemp = goToCateogryQuiet(currentNode, "IRS990")
    currentNode = currentNodeTemp
    currentNodeTemp = goToCateogryQuiet(currentNodeTemp, "Form990PartVIISectionA")

    # Oh, repeated Category it says, we got the first entry, let's make sure we can get to the other instances
    startingIndex = goBack()

    # What data within that section do you want?
    subCategories = ["NamePerson", "AverageHoursPerWeek"]
    temp = getAllOccurences(startingIndex, "Form990PartVIISectionA", subCategories)
    for j in temp:
        if j[0] in peopleHoursWorked:
            people, hours = j[0], j[1]
            peopleHoursWorked[people] += float(hours)
        else:
            miniDictionary = {j[0] : float(j[1])}
            peopleHoursWorked.update(miniDictionary)

print("\n\n\n!!!!!!!!!!!!!!!!!!!!!!!Form990PartVIISectionA | All People & Their Hours Worked!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
for key, value in peopleHoursWorked.items():
    # Weird Python Dictionary stuff
    if(str(key).isnumeric() == False):
        print("Person: ", key, " Worked: ", value)



###############################
# Printing out extracted Data
###############################
# Okay, how about we plot them?
plottingDictionary = {}
for key, value in peopleHoursWorked.items():
    if(str(key).isnumeric() == False):
        miniDictionary = {key : value}
        plottingDictionary.update(miniDictionary)

keys = plottingDictionary.keys()
values = plottingDictionary.values()

#install("matplotlib")
import matplotlib.pyplot as plt

# Plot out hours and people in bar graph
plt.bar(keys, values)
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()



# Now, that is not particularly juicy, let us see how much Shirley gets paid :evil:
# Looking at the Form 990, I see such information is under ScheduleJPartII, let us find it
#< Form990ScheduleJPartII >
#< NamePerson > SHIRLEY ANN JACKSON < / NamePerson >
#< BaseCompensationFilingOrg > 819996 < / BaseCompensationFilingOrg >
#< BonusFilingOrg > 236589 < / BonusFilingOrg >
#< OtherCompensationFilingOrg > 135111 < / OtherCompensationFilingOrg >
#< DeferredCompFilingOrg > 548212 < / DeferredCompFilingOrg >
#< NontaxableBenefitsFilingOrg > 31969 < / NontaxableBenefitsFilingOrg >
#< TotalCompensationFilingOr

# let us start with 2010 + 0 or 2010 as most normal people call it
currentNode = years2010[0].getroot()
# What categories do I have to choose from again?
printSubCategories(currentNode)
# Oh, yeah, Schedule J
currentNode = goToCateogry(currentNode, "IRS990ScheduleJ")
# What categories again?
printSubCategories(currentNode)
# Form990ScheduleJPartII looks like what I want
currentNode = goToCateogry(currentNode, "Form990ScheduleJPartII")
printSubCategories(currentNode)


# How about I get these for everyone, for all years available?
# This time, let us see how it changes with time
hereItIs = []
# Let's culminate this data from multiple different tax forms
for i in range(len(years2010)):
    print("On Year: ", 2010 + i)
    # 0-9 => 2010 + index
    currentNode = years2010[i].getroot()

    #Tell it how to get to section (remember it gave us that warning, how about we don't get that anymore by using Quiet functions?)
    if(i <= 3):
        currentNode = years2010[i].getroot()
        currentNode = goToCateogryQuiet(currentNode, "IRS990ScheduleJ")
        currentNode = goToCateogryQuiet(currentNode, "Form990ScheduleJPartII")
    else:
        # Yeah, government or yeah RPI DECIDED TO CHANGE HOW IT FILES <-_->
        currentNode = years2010[i].getroot()
        currentNode = goToCateogryQuiet(currentNode, "IRS990ScheduleJ")
        currentNode = goToCateogryQuiet(currentNode, "RltdOrgOfficerTrstKeyEmplGrp")
    # What data within that section do you want?
    # Idk, ALL THE DATA
    currentNode = goBack()
    if(i <= 3):
        getThese = ["NamePerson", "TotalCompensationFilingOrg"]
        temp = getAllOccurences(currentNode, "Form990ScheduleJPartII", getThese)
    else:
        getThese = ["PersonNm", "TotalCompensationFilingOrgAmt"]
        temp = getAllOccurences(currentNode, "RltdOrgOfficerTrstKeyEmplGrp", getThese)
    for j in temp:
        # WHY WOULD YOU WRITE AN EXPLAINATION OF SHIRLEY'S PAY SPECIFICALLY UNDER THIS SECTION, IT FUCKS UP PARSING SO BADLY AND MAKES THIS WHOLE THING CURSED
        if("Rensselaer" not in j[0] and "is" not in j[0] and "of" not in j[0] and "Performance" not in j[0] and "Part" not in j[0] and "reported" not in j[0]):
            print("Person: ", j[0], " Value: ", j[1])
            hereItIs.append([j[0], str(2010 + i), j[1]])


peopleX = []
peopleY = []
peopleNames = []
for i in range(len(hereItIs)):
    name, year, value = hereItIs[i]
    arrX = []
    arrY = []
    if name not in peopleNames:
        peopleNames.append(name)
        arrX.append(int(year))
        arrY.append(int(value))
        for j in range(len(hereItIs)):
            if(i != j and name == hereItIs[j][0]):
                arrX.append(int(hereItIs[j][1]))
                arrY.append(int(hereItIs[j][2]))
        peopleX.append(arrX)
        peopleY.append(arrY)

import numpy as np
plt.rcParams["figure.autolayout"] = True
for i in range(len(peopleNames)):
    plt.plot(peopleX[i], peopleY[i], label=peopleNames[i])
leg = plt.legend(loc='upper left')
plt.show()

# To export to Excel follow this guide
df = pd.DataFrame({"Names: " : peopleNames, "Years " : peopleX, "Amount: " : peopleY})
install("xlsxwriter")
import xlsxwriter
excel_writer = pd.ExcelWriter('fileName.xlsx', engine='xlsxwriter')
df.to_excel(excel_writer, sheet_name='first_sheet')
excel_writer.save()

# Let us try a bubble plot with the latest Data
class BubbleChart:
    def __init__(self, area, bubble_spacing=0):
        """
        Setup for bubble collapse.

        Parameters
        ----------
        area : array-like
            Area of the bubbles.
        bubble_spacing : float, default: 0
            Minimal spacing between bubbles after collapsing.

        Notes
        -----
        If "area" is sorted, the results might look weird.
        """
        area = np.asarray(area)
        r = np.sqrt(area / np.pi)

        self.bubble_spacing = bubble_spacing
        self.bubbles = np.ones((len(area), 4))
        self.bubbles[:, 2] = r
        self.bubbles[:, 3] = area
        self.maxstep = 2 * self.bubbles[:, 2].max() + self.bubble_spacing
        self.step_dist = self.maxstep / 2

        # calculate initial grid layout for bubbles
        length = np.ceil(np.sqrt(len(self.bubbles)))
        grid = np.arange(length) * self.maxstep
        gx, gy = np.meshgrid(grid, grid)
        self.bubbles[:, 0] = gx.flatten()[:len(self.bubbles)]
        self.bubbles[:, 1] = gy.flatten()[:len(self.bubbles)]

        self.com = self.center_of_mass()

    def center_of_mass(self):
        return np.average(
            self.bubbles[:, :2], axis=0, weights=self.bubbles[:, 3]
        )

    def center_distance(self, bubble, bubbles):
        return np.hypot(bubble[0] - bubbles[:, 0],
                        bubble[1] - bubbles[:, 1])

    def outline_distance(self, bubble, bubbles):
        center_distance = self.center_distance(bubble, bubbles)
        return center_distance - bubble[2] - \
            bubbles[:, 2] - self.bubble_spacing

    def check_collisions(self, bubble, bubbles):
        distance = self.outline_distance(bubble, bubbles)
        return len(distance[distance < 0])

    def collides_with(self, bubble, bubbles):
        distance = self.outline_distance(bubble, bubbles)
        idx_min = np.argmin(distance)
        return idx_min if type(idx_min) == np.ndarray else [idx_min]

    def collapse(self, n_iterations=50):
        """
        Move bubbles to the center of mass.

        Parameters
        ----------
        n_iterations : int, default: 50
            Number of moves to perform.
        """
        for _i in range(n_iterations):
            moves = 0
            for i in range(len(self.bubbles)):
                rest_bub = np.delete(self.bubbles, i, 0)
                # try to move directly towards the center of mass
                # direction vector from bubble to the center of mass
                dir_vec = self.com - self.bubbles[i, :2]

                # shorten direction vector to have length of 1
                dir_vec = dir_vec / np.sqrt(dir_vec.dot(dir_vec))

                # calculate new bubble position
                new_point = self.bubbles[i, :2] + dir_vec * self.step_dist
                new_bubble = np.append(new_point, self.bubbles[i, 2:4])

                # check whether new bubble collides with other bubbles
                if not self.check_collisions(new_bubble, rest_bub):
                    self.bubbles[i, :] = new_bubble
                    self.com = self.center_of_mass()
                    moves += 1
                else:
                    # try to move around a bubble that you collide with
                    # find colliding bubble
                    for colliding in self.collides_with(new_bubble, rest_bub):
                        # calculate direction vector
                        dir_vec = rest_bub[colliding, :2] - self.bubbles[i, :2]
                        dir_vec = dir_vec / np.sqrt(dir_vec.dot(dir_vec))
                        # calculate orthogonal vector
                        orth = np.array([dir_vec[1], -dir_vec[0]])
                        # test which direction to go
                        new_point1 = (self.bubbles[i, :2] + orth *
                                      self.step_dist)
                        new_point2 = (self.bubbles[i, :2] - orth *
                                      self.step_dist)
                        dist1 = self.center_distance(
                            self.com, np.array([new_point1]))
                        dist2 = self.center_distance(
                            self.com, np.array([new_point2]))
                        new_point = new_point1 if dist1 < dist2 else new_point2
                        new_bubble = np.append(new_point, self.bubbles[i, 2:4])
                        if not self.check_collisions(new_bubble, rest_bub):
                            self.bubbles[i, :] = new_bubble
                            self.com = self.center_of_mass()

            if moves / len(self.bubbles) < 0.1:
                self.step_dist = self.step_dist / 2

    def plot(self, ax, labels, colors):
        for i in range(len(self.bubbles)):
            circ = plt.Circle(
                self.bubbles[i, :2], self.bubbles[i, 2], color=colors[i])
            ax.add_patch(circ)
            ax.text(*self.bubbles[i, :2], labels[i],
                    horizontalalignment='center', verticalalignment='center')

res = sorted(range(len(peopleY)), key = lambda sub: peopleY[sub])[-5:]

peopleXTop5 = [peopleX[res[0]][-1], peopleX[res[1]][-1], peopleX[res[2]][-1], peopleX[res[3]][-1], peopleX[res[4]][-1]]
peopleYTop5 = [peopleY[res[0]][-1], peopleY[res[1]][-1], peopleY[res[2]][-1], peopleY[res[3]][-1], peopleY[res[4]][-1]]
peopleNamesTop5 = [peopleNames[res[0]], peopleNames[res[1]], peopleNames[res[2]], peopleNames[res[3]], peopleNames[res[4]]]


browser_market_share = {
    'Names': peopleNamesTop5,
    'market_share': peopleYTop5,
    'color': ['#5A69AF', '#579E65', '#F9C784', '#FC944A', '#F24C00', '#00B825']
}

bubble_chart = BubbleChart(area=browser_market_share['market_share'],
                           bubble_spacing=0.1)

bubble_chart.collapse()

fig, ax = plt.subplots(subplot_kw=dict(aspect="equal"))
bubble_chart.plot(
    ax, browser_market_share['Names'], browser_market_share['color'])
ax.axis("off")
ax.relim()
ax.autoscale_view()
ax.set_title('2020 IRS 990 Total Compensation (Latest for Individuals, Top 5)')

plt.show()