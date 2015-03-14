'''
Created on Mar 13, 2015

@author: jalexander
'''

import menu_object
import parsing_funcs

import json

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

theFile = open('testmenu.pdf', 'rb')
parser = PDFParser(theFile)
document = PDFDocument(parser)
if not document.is_extractable:
    raise PDFTextExtractionNotAllowed

rsrcmgr = PDFResourceManager()
laparams = LAParams()
device = PDFPageAggregator(rsrcmgr, laparams=laparams)
interpreter = PDFPageInterpreter(rsrcmgr, device)

page = nth(PDFPage.create_pages(document), 0)

interpreter.process_page(page)
layout = device.get_result()

if os.path.isfile('menu_text.txt'):
    os.remove('menu_text.txt')
outfile = open('menu_text.txt', 'w')
outfile.write(parsing_funcs.printAll(layout))
outfile.flush()
outfile.close()

parsing_funcs.buildMenuPage(layout)
