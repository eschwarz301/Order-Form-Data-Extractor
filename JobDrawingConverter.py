__author__ = 'eschwarz'
'''
Iterates through a unicode file, extracts the Size Drawings necessary to fulfill the Customer Order into a nested list "outputList" while ignoring headers and duplicate drawings.
'''

import codecs
import re

class File_Reader(object):

    def __init__(self):
        self.line_data = [] # Holds the processed data from each line.
        self.output_list = [] # Holds each lineData that has been checked for duplicates in a nested list of the format [[Quantity,Drawing Number,Revision (if any),Drawing Description],...]
        self.header = True # Tells us if we are in a header.

    def open_file(self,file_name):
        with codecs.open(file_name, 'r', encoding='utf-16-le') as f: # Open a file with UTF-16LE encoding.
            self.read_file(f)
        if f.closed == False:
            f.close()

    def read_file(self,file):
        line = file.readline()
        while line != "":
            if line.find("PAGE") >=0: # Because of the way the header is laid out in these documents we can use "PAGE" to find the beginning of the header, and we must check this every line because each page has a new header.
                self.header = True
            self.extract_drawing(line)
            self.dupe_check()
            if line.find("QUANTITY") >=0: # We can+ use "QUANTITY" to find the end of the page header and then grab the next line of text knowing it contains drawing information.
                self.header = False
            self.line_data = []
            line = file.readline()        

    def extract_drawing(self,line):
        if self.header == False:
            temp=[x.start() for x in re.finditer(('\S+ \S+'),line)] # Find words in the Drawing Description and return their starting indices.
            self.line_data = re.findall('\S+',line[0:temp[0]]) # Add all strings except Drawing Description to the list line_data.
            self.line_data.append(' '.join(re.findall('\S+',line[temp[0]:]))) # Join all strings in the Drawing Description together with spaces and append it to lineData.

    def dupe_check(self):
        if self.line_data != []:
            if (self.line_data in self.output_list) == False:
                self.output_list.append(self.line_data)
        return()

# Program
run = File_Reader()
run.open_file('JSOutput.txt')
print(run.output_list)
    
