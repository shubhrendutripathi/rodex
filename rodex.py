#!/usr/bin/python

"""
* The MIT License (MIT)
*
* Copyright (c) 2017 Shubhrendu Tripathi
*
* Permission is hereby granted, free of charge, to any person obtaining a copy
* of this software and associated documentation files (the "Software"), to deal
* in the Software without restriction, including without limitation the rights
* to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
* copies of the Software, and to permit persons to whom the Software is
* furnished to do so, subject to the following conditions:
*
* The above copyright notice and this permission notice shall be included in all
* copies or substantial portions of the Software.
*
* THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
* IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
* FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
* AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
* LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
* OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
* SOFTWARE.
*
"""

import csv
import codecs
import io
from reportlab.platypus import (
								BaseDocTemplate, 
								Frame, 
								Paragraph, 
								PageBreak, 
								PageTemplate
)
from reportlab.lib.styles import getSampleStyleSheet
import random
import os
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.colors import (
    black,
    purple,
    white,
    yellow,
    grey,
    lightgrey
)
from reportlab.pdfbase.pdfmetrics import registerFont, registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont

registerFont(TTFont('Lato-Black', 'fonts/Lato-Black.ttf'))

def stylesheet():
    styles= {
        'default': ParagraphStyle(
            'default',
            fontName='Times-Roman',
            fontSize=10,
            leading=12,
            leftIndent=0,
            rightIndent=0,
            firstLineIndent=0,
            alignment=TA_LEFT,
            spaceBefore=0,
            spaceAfter=0,
            bulletFontName='Times-Roman',
            bulletFontSize=10,
            bulletIndent=0,
            textColor= black,
            backColor=None,
            wordWrap=None,
            borderWidth= 0,
            borderPadding= 0,
            borderColor= None,
            borderRadius= None,
            allowWidows= 1,
            allowOrphans= 0,
            textTransform=None,  # 'uppercase' | 'lowercase' | None
            endDots=None,         
            splitLongWords=1,
        ),
    }
    styles['title'] = ParagraphStyle(
        'title',
        parent=styles['default'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=42,
        alignment=TA_CENTER,
        textColor=purple,
    )
    styles['alert'] = ParagraphStyle(
        'alert',
        parent=styles['default'],
        leading=14,
        backColor=yellow,
        borderColor=black,
        borderWidth=1,
        borderPadding=5,
        borderRadius=2,
        spaceBefore=10,
        spaceAfter=10,
    )
    styles['title-letter'] = ParagraphStyle(
        'title-letter',
        parent=styles['default'],
        fontName='Lato-Black',
        fontSize=16,
        leading=42,
        alignment=TA_CENTER,
        textColor=black,
    )
    styles['contact-name'] = ParagraphStyle(
        'contact-name',
								parent=styles['default'],
								fontName='Lato-Black',
								fontSize=10,
								leading=14,
								backColor=lightgrey,
								borderColor=black,
								borderWidth=1,
								borderPadding=1,
								borderRadius=1,
								spaceBefore=10,
								spaceAfter=10,
    )
    return styles


def build_flowables(stylesheet):
    return [
        Paragraph("I'm a title!", stylesheet['title']),
        Paragraph('some text. ' * 30, stylesheet['default']),
        Paragraph('This is important!', stylesheet['alert']),
        Paragraph('more text. ' * 30, stylesheet['default']),
    ]

def build_flowables_1(stylesheet):
								Elements = []
								Elements.append(Paragraph("J", stylesheet['title-letter']))
								Elements.append(Paragraph("John Smith", stylesheet['contact-name']))
								Elements.append(Paragraph('some text. ' * 300, stylesheet['default']))
								Elements.append(Paragraph("Jane Smith", stylesheet['contact-name']))
								Elements.append(Paragraph('another writing. ' * 300, stylesheet['default']))
								return Elements

def build_addEntry(entry, type, stylesheet):
								return [Paragraph(entry, stylesheet[type])]

def build_pdf(filename, flowables):
								doc = BaseDocTemplate(filename, showBoundary=1)

								words = "lorem ipsum dolor sit amet consetetur sadipscing elitr sed diam nonumy eirmod tempor invidunt ut labore et".split()

								styles=getSampleStyleSheet()
								#Elements=[]

								#two columns
								frame1 = Frame(doc.leftMargin, doc.bottomMargin, doc.width/2-6, doc.height, id='col1')
								frame2 = Frame(doc.leftMargin+doc.width/2+6, doc.bottomMargin, doc.width/2-6, doc.height, id='col2')

								doc.addPageTemplates([PageTemplate(id='TwoCol',frames=[frame1,frame2]), ])

								#Elements.append(Paragraph(" ".join([random.choice(words) for i in range(1000)]),styles['Normal']))
								
								#start the construction of the pdf
								#doc.build(Elements)
								doc.build(flowables)

def row_decode(reader, encoding='utf8'):
								for row in reader:
																yield [col.decode('utf8') for col in row]

if __name__ == "__main__": 
								###############
								##convert the default google.csv utf16 encoding to utf8
								##write the file to another file
								###############
								
								#get rid of unicode errors
								import sys
								reload(sys)
								sys.setdefaultencoding('utf-8')
								#get rid of unicode errors - end
								
								csvfile = open('google-utf8.csv', 'wb')
								writer = csv.writer(csvfile)
								with io.open('google.csv', encoding='utf16') as f:
																wrapped = codecs.iterencode(f, 'utf8')
																reader = csv.reader(wrapped, delimiter=',')
																for row in row_decode(reader):
																								print row
																								writer.writerow(row)
								
								print "##################################################################################################"
								
								##############
								##extract the relevant contacts details
								##for printing and populate the Elements list
								##############
								
								

								##############
								##build the pdf
								##############
								build_pdf('contacts.pdf', build_flowables_1(stylesheet()))
								#build_pdf('contacts.pdf', build_addEntry("John Smith", "contact-name", stylesheet()))
								
								###############
								## use external program xpdf to view the generated pdf
								###############
								os.system("zathura contacts.pdf")
