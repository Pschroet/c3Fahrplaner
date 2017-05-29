'''
Created on 18.08.2016

A collection of different support functions

@author: Philipp Schroeter
'''

import os

#checks if the given file exists
#  if it does not exist, but the directory can be written to the file will be created
def checkFile(fileToCheck, create):
    directory = os.path.dirname(os.path.realpath(fileToCheck))
    #print "[util.checkFile] Directory " + directory
    if os.path.exists(directory):
        if os.path.isfile(fileToCheck):
            #print "[util.checkFile] Object " + fileToCheck + " found"
            return True
        else:
            if create:
                #print "[util.checkFile] Object " + fileToCheck + " does not exist, it will be created"
                openedFile = open(fileToCheck, "w")
                openedFile.close()
                return True
            else:
                #print "[util.checkFile] Object " + fileToCheck + " does not exist"
                return False
    else:
        #print "[util.checkFile] Directory of file " + fileToCheck + " does not exist or cannot be accessed"
        return False
    #to ensure something is returned
    return False

def write2File(filename, content, mode):
    f = open(filename, mode)
    f.write(content.encode('utf-8'))
    f.close()

def get_files_in_directory(directory, recursive):
    output = []
    content = os.listdir(directory)
    for item in content:
        tmp = directory + "/" + item
        if os.path.isfile(tmp):
            output.append(item)
        elif os.path.isdir(tmp) and recursive:
            output = output + get_files_in_directory(tmp, True)
    return output

#filters all elements from a list, where the given filter is found as part of a regex
#returns a list with the elements removed
def filter_files_from_list(file_list, expr):
    output = []
    for elem in file_list:
        if not re.match(".*" + expr + ".*", elem):
            output.append(elem)
    return output

#returns the content of a file as a list or "" if there is no content
# note: removes line separators
def readFileContentAsList(fileToRead):
    if checkFile(fileToRead, False):
        openedFile = open(fileToRead, "r")
        content = openedFile.readlines()
        #remove newlines
        for i in range(0, len(content)):
            content[i] = content[i].rstrip(os.linesep)
        openedFile.close()
        return content
    return ""

#returns the content of a file as a String or "" if there is no content
def readFileContentAsString(fileToRead):
    if checkFile(fileToRead, False):
        openedFile = open(fileToRead, "r")
        contentLines = openedFile.readlines()
        content = ""
        #concat lines
        for i in range(0, len(contentLines)):
            content = content + contentLines[i]
        openedFile.close()
        return content
    return ""

def fixUmlauts():
    pass