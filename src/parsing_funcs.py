'''
Created on Mar 14, 2015

@author: jalexander
'''
from itertools import islice
from cgitb import text
from pickle import FALSE
def nth(iterable, n, default=None):
    "Returns the nth item or a default value"
    return next(islice(iterable, n, None), default)

import menu_object
import utils

from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure, LTComponent, LTText, LTTextBoxHorizontal
from pdfminer.pdfpage import PDFTextExtractionNotAllowed

dayPos = []
for i in range(7):
    dayPos.append(-1)

meal = "@"

upperLimit = 10000
lowerLimit = -1

categoryPos = []

def getDayPos(layout):
    """Function to find the positions of the various days.
        Also sets the meal variable by finding the first instance of a meal name"""
    global mondayPos
    global tuesdayPos
    global wednesdayPos
    global thursdayPos
    global fridayPos
    global saturdayPos
    global sundayPos
    global meal
    for lt_obj in layout:        
        if issubclass(lt_obj.__class__, LTTextBox) or isinstance(lt_obj, LTTextBox):
            if lt_obj.get_text().startswith("Monday") and dayPos[0] == -1:
                dayPos[0] = lt_obj.x0
            elif lt_obj.get_text().startswith("Tuesday") and dayPos[1] == -1:
                dayPos[1] = lt_obj.x0
            elif lt_obj.get_text().startswith("Wednesday") and dayPos[2] == -1:
                dayPos[2] = lt_obj.x0
            elif lt_obj.get_text().startswith("Thursday") and dayPos[3] == -1:
                dayPos[3] = lt_obj.x0
            elif lt_obj.get_text().startswith("Friday") and dayPos[4] == -1:
                dayPos[4] = lt_obj.x0
            elif lt_obj.get_text().startswith("Saturday") and dayPos[5] == -1:
                dayPos[5] = lt_obj.x0 
            elif lt_obj.get_text().startswith("Sunday") and dayPos[6] == -1:
                dayPos[6] = lt_obj.x0
            else:
                if meal == "@":
                    if lt_obj.get_text().strip().startswith("Breakfast"):
                        meal = "breakfast"
                    elif lt_obj.get_text().strip().startswith("Brunch"):
                        meal = "brunch"
                    elif lt_obj.get_text().strip().startswith("Lunch"):
                        meal = "lunch"
                    elif lt_obj.get_text().strip().startswith("Dinner"):
                        meal = "dinner"
                    elif lt_obj.get_text().strip().startswith("Late Night"):
                        meal = "late_night"
                    elif lt_obj.get_text().strip().startswith("Gaucho Bright Meal"):
                        meal = "bright_meal"
                    
        else:
            if isinstance(lt_obj, LTFigure):
                repeat = False
                for i in range(0, 6):
                    if dayPos[i] == -1:
                        repeat = True
                        break
                if repeat:
                    getDayPos(lt_obj)  # Recursive
            else:
                break

def isCategory(text):
    print "start"
    print text
    print "end"
    print text == "Bakery"
    return text == "Blue Plate Special" or "Taqueria" in text or text == "Pizza" or text == "To Order" \
            or "Salads/Deli" in text or text == "Grill (Cafe)" or text == "Bakery" or (text == "Breakfast" \
            and meal == "bright_meal") or (text == "Lunch" and meal == "bright_meal") \
            or (text == "Brunch" and meal == "bright_meal") or (text == "Dinner" and meal == "bright_meal") or \
            text == "Omelet Made to Order" \
            or text == "Hot Foods" or text == "Salads" or text == "Specialty Bar" or text == "Sushi" \
            or text == "Panini/Pizza" or text == "Grilled Sandwiches to Order"

def getCategoryPos(layout):
    global categoryPos
    
    for lt_obj in layout:
        print categoryPos
        if issubclass(lt_obj.__class__, LTTextBox) or isinstance(lt_obj, LTTextBox):
            text = lt_obj.get_text().strip()
            if isCategory(text):
                print "APPENDED"
                categoryPos.append((text, lt_obj.y0))
                print categoryPos

        else:
            if isinstance(lt_obj, LTFigure):
                    getCategoryPos(lt_obj)  # Recursive
                    
def getLowerLimit(layout):
    global lowerLimit
    
    for lt_obj in layout:
        if issubclass(lt_obj.__class__, LTTextBox) or isinstance(lt_obj, LTTextBox):
            if "Instagram" in lt_obj.get_text() or "Twitter" in lt_obj.get_text() or \
                "Facebook" in lt_obj.get_text() or "CBORD" in lt_obj.get_text():
                if (lt_obj.y1 + 2) > lowerLimit:
                    lowerLimit = lt_obj.y1 + 2
        else:
            if isinstance(lt_obj, LTFigure):
                    getLowerLimit(lt_obj)  # Recursive

def insertAll(layout, commonsMenu):
    global dayPos
    global meal
    global categoryPos
    global upperLimit
    global lowerLimit
        
    for lt_obj in layout:
        if issubclass(lt_obj.__class__, LTTextBox) or isinstance(lt_obj, LTTextBox):
            if lt_obj.y0 < upperLimit and lt_obj.y0 > lowerLimit:
                text = lt_obj.get_text().strip()
                if not isCategory(text):
                    allItems = lt_obj.get_text().split("\n")
                    for item in allItems:
                        if item.strip() != "":
                            myCategory = getCategory(lt_obj.y0)
                            currentCatDict = commonsMenu.days[getDay(lt_obj.x0)].meals[meal].categories
                            if myCategory in currentCatDict:
                                currentCatDict[myCategory].append(item.strip())
                            else:
                                currentCatDict[myCategory] = []
                                currentCatDict[myCategory].append(item.strip())
                            
        else:
            if isinstance(lt_obj, LTFigure):
                    insertAll(lt_obj, commonsMenu)  # Recursive

def getDay(xPos):
    global dayPos
    for i in range(0, len(dayPos)):
        if xPos <= dayPos[i]:
            return utils.numToDay(i)
    raise Exception("Overly large value " + str(xPos) + " passed to getDay().")

def getCategory(catPos):
    global categoryPos
    for i in range(0, len(categoryPos)):
        if catPos <= categoryPos[i][1]:
            return categoryPos[i][0]
            
def buildMenuPage(layout, commonsMenu):
    global dayPos
    global meal
    global categoryPos
    global upperLimit
    global lowerLimit
    
    dayPos = []
    for i in range(7):
        dayPos.append(-1)
    meal = "@"
    upperLimit = 10000
    lowerLimit = -1
    categoryPos = []
    
    if not isinstance(commonsMenu, menu_object.diningHall):
        raise Exception("Second argument to buildMenuPage was not a dining hall.")
    
    getDayPos(layout)
    getCategoryPos(layout)
    print categoryPos
    getLowerLimit(layout)
    
    categoryPos= sorted(categoryPos, key=lambda tup: tup[1])
    print(categoryPos)
    
    if len(categoryPos) == 0:
        raise Exception("Blank page, no categories.")
        
    upperLimit = categoryPos[len(categoryPos) - 1][1] - 2
    
    insertAll(layout, commonsMenu)
    
    print(meal)