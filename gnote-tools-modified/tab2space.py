#!/usr/bin/python
# -*- coding: utf-8 -*-
# xiaojias@cn.ibm.com intial version  Aug, 2018

# translate tab character to 4 blank space characters

import os

lineList = []

# types of files to be processed
postfixes = ['.py', '.java', '.c', '.cpp', '.h']

def deal_lines(fileName):
    cmd = "dos2unix -ascii %s" %fileName
    os.system(cmd)
    with open(fileName, 'r') as f:
        for line in f:
            str = line.replace('\t', '    ').rstrip()
            yield str + "\n"

def format_covert(filePath):
    for path, dirs, files in os.walk(filePath):
        for fileName in files:
            fullPath = os.path.join(path, fileName)
            normPath = os.path.normpath(os.path.abspath(fullPath))

            modifyFileFlag = any([normPath.endswith(postfix) for postfix in postfixes])
            if modifyFileFlag:
                for line in deal_lines(normPath):
                    lineList.append(line)
                with open(normPath, 'w+') as f:
                    for index in range(0, len(lineList)):
                        f.write(lineList[index])
                del lineList[:]

if __name__ == '__main__':
    filePath = raw_input('Please input a file path: ')
    format_covert(filePath)
