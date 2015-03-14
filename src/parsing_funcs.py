'''
Created on Mar 14, 2015

@author: jalexander
'''
from itertools import islice
def nth(iterable, n, default=None):
    "Returns the nth item or a default value"
    return next(islice(iterable, n, None), default)

import menu_object
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure, LTComponent, LTText, LTTextBoxHorizontal
from pdfminer.pdfpage import PDFTextExtractionNotAllowed

menu = menu_object.menuObject()

mondayPos = -1
tuesdayPos = -1
wednesdayPos = -1
thursdayPos = -1
fridayPos = -1
saturdayPos = -1
sundayPos = -1

def getDayPos(layout):
    """Function to recursively parse each page."""
    for lt_obj in layout:
        global mondayPos
        global tuesdayPos
        global wednesdayPos
        global thursdayPos
        global fridayPos
        global saturdayPos
        global sundayPos
        
        if issubclass(lt_obj.__class__, LTTextBox) or isinstance(lt_obj, LTTextBox):
            if "Monday" in lt_obj.get_text() and mondayPos == -1:
                mondayPos = lt_obj.x0
            elif "Tuesday" in lt_obj.get_text() and tuesdayPos == -1:
                tuesdayPos = lt_obj.x0
            elif "Wednesday" in lt_obj.get_text() and wednesdayPos == -1:
                wednesdayPos = lt_obj.x0
            elif "Thursday" in lt_obj.get_text() and thursdayPos == -1:
                thursdayPos = lt_obj.x0
            elif "Friday" in lt_obj.get_text() and fridayPos == -1:
                fridayPos = lt_obj.x0
            elif "Saturday" in lt_obj.get_text() and saturdayPos == -1:
                saturdayPos = lt_obj.x0
            elif "Sunday" in lt_obj.get_text() and sundayPos == -1:
                sundayPos = lt_obj.x0
        else:
            if mondayPos == -1 or tuesdayPos == -1 or wednesdayPos == -1 or thursdayPos == -1 or fridayPos == -1 \
            or saturdayPos == -1 or sundayPos == -1:
                if isinstance(lt_obj, LTFigure):
                    getDayPos(lt_obj)  # Recursive
            else:
                break
            
def buildMenuPage(layout):
    mondayPos = -1
    tuesdayPos = -1
    wednesdayPos = -1
    thursdayPos = -1
    fridayPos = -1
    saturdayPos = -1
    sundayPos = -1
    
    getDayPos(layout)

def printAll(layout, result=""):
    """Function to recursively print the layout tree."""
    for lt_obj in layout:
        result += ("\n" + lt_obj.__class__.__name__)
        if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
            result += (" (" + str(lt_obj.x0) + ", " + str(lt_obj.y0) + ")" + "\n")
            result += (lt_obj.get_text())
        elif isinstance(lt_obj, LTFigure):
            printAll(lt_obj, result)  # Recursive
    return result