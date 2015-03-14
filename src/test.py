'''
Created on Mar 14, 2015

@author: jalexander
'''

import menu_object

import json
import os 

menu = menu_object.menuObject()
for daykey in menu.days.iterkeys():
    for mealkey in menu.days[daykey].meals.iterkeys():
        menu.days[daykey].meals[mealkey].categories['hot food'] = "baaaaannnnnnnaaaaaaannnnnaaaaaaa"
        
if os.path.isfile('json_test.json'):
    os.remove('json_test.json')
outfile = open('json_test.json', 'w')
outfile.write(json.dumps(menu, default=lambda o: o.__dict__, sort_keys=True, indent=4, separators=(',', ': ')))
outfile.flush()
outfile.close()