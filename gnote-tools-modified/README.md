Translate gnotes to .xml files
=========
Tested and worked in RHEL7 desktop client (source codes are download from [github of: whyoh](https://github.com/whyoh)

Usage
---------
1. Download the files from github:
https://github.com/whyoh/pyContent
and
https://github.com/whyoh/gnote-tools
and put all the files in a single directory;

2. Translate the tab character into 4-blank-space character for every .py file, by running command of:
./tab2space.py

3. Convert gnote files to .xml, and store in the running directory by running command of:
./notewiki.py -m export -s note-html.xsl

All the .xml files will be generated in current working directory

