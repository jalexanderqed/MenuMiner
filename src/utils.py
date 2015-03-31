'''
Created on Mar 30, 2015

@author: jalexander
'''

from pdfminer.layout import LTTextBox, LTTextLine, LTFigure

days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

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

def orderedLG(arr):
    for i in range(1, len(arr)):
        if arr[i - 1] >= arr[i]:
            print(i-1, i)
            print(arr[i - 1], arr[i])
            return False
    return True

def orderedGL(arr):
    for i in range(1, len(arr)):
        if arr[i - 1] <= arr[i]:
            print(i-1, i)
            print(arr[i - 1], arr[i])
            return False
    return True

def numToDay(num):
    global days
    if num > 6:
        raise Exception("Overly large value " + str(num) + " passed to numToDay().")
    return days[num]

def hasMonth(myStr):
    return "January" in myStr or "February" in myStr or "March" in myStr or \
        "April" in myStr or "May" in myStr or "June" in myStr or \
        "July" in myStr or "August" in myStr or "September" in myStr or \
        "October" in myStr or "November" in myStr or "December" in myStr