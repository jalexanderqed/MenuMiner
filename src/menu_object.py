'''
Created on Mar 14, 2015

@author: jalexander
'''

class meal(object):
    def __init__(self):
        self.categories = {}

class day(object):
    def __init__(self):
        self.meals = {}
        self.meals['breakfast'] = meal()
        self.meals['lunch'] = meal()
        self.meals['dinner'] = meal()
        self.meals['late_night'] = meal()
        self.meals['bright_meal'] = meal()
        
class diningHall(object):
    def __init__(self):
        self.days = {}
        self.days['monday'] = day()
        self.days['tuesday'] = day()
        self.days['wednesday'] = day()
        self.days['thursday'] = day()
        self.days['friday'] = day()
        self.days['saturday'] = day()
        self.days['sunday'] = day()
        
class menuObject(object):
    def __init__(self):
        self.halls = {}
        self.halls['dlg'] = diningHall()
        self.halls['ortega'] = diningHall()
        self.halls['carrillo'] = diningHall()
        self.halls['portola'] = diningHall()
