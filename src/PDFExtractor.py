'''
Created on Mar 13, 2015

@author: jalexander
'''

import menu_object
import parsing_funcs
import utils

import json
import os 

from itertools import islice
def nth(iterable, n, default=None):
    "Returns the nth item or a default value"
    return next(islice(iterable, n, None), default)

from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure, LTComponent, LTText, LTTextBoxHorizontal
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
import os

theFile = open('dlg.pdf', 'rb')
parser = PDFParser(theFile)
document = PDFDocument(parser)
if not document.is_extractable:
    raise PDFTextExtractionNotAllowed

rsrcmgr = PDFResourceManager()
laparams = LAParams()
device = PDFPageAggregator(rsrcmgr, laparams=laparams)
interpreter = PDFPageInterpreter(rsrcmgr, device)
    
'''    if os.path.isfile('menu_text.txt'):
        os.remove('menu_text.txt')
    outfile = open('menu_text.txt', 'w')
    outfile.write(utils.printAll(layout))
    outfile.flush()
    outfile.close()'''
    
menu = menu_object.menuObject()

i = 0
page = nth(PDFPage.create_pages(document), i)

while page != None:
    interpreter.process_page(page)
    layout = device.get_result()
    
    parsing_funcs.buildMenuPage(layout, menu.halls['dlg'])
    i += 1
    page = nth(PDFPage.create_pages(document), i)


if os.path.isfile('data.json'):
    os.remove('data.json')
outfile = open('data.json', 'w')
outfile.write(json.dumps(menu, default=lambda o: o.__dict__, sort_keys=True, indent=4, separators=(',', ': ')))
outfile.flush()
outfile.close()