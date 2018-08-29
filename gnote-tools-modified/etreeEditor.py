#!/usr/bin/python
# -*- coding: utf-8 -*-

# etreeEditor adds etree-based XML import/export to the richText content editor (via docHierarchy)

from docHierarchy import docHierarchy

class etreeEditor(docHierarchy):

    def __init__(self, document = None):
        docHierarchy.__init__(self)
        self._nsmap = None
        if document: self.parse(document)

    def add(self, tag, start, end, attrib = None):
        docHierarchy.add(self, tag, start, end, attrib = attrib)

    def parse(self, document):
        from lxml import etree
        tree = etree.fromstring(document)
        self._nsmap = tree.nsmap
        self._text, self._styles = self._deconstruct(tree)

    def _deconstruct(self, element):
        text = element.text
        if text == None: text = ""
        styles = [{'name': element.tag, 'start': 0, 'end': None, 'attrib': element.attrib}]
        if not element.attrib: styles[0]['attrib'] = None
        for ele in element:
            subtext, substyles = self._deconstruct(ele)
            for style in substyles:
                style['start'] += len(text)
                style['end'] += len(text)
                styles.append(style)
            text += subtext
        styles[0]['end'] = len(text)
        if element.tail: text += element.tail
        return text, styles

    def serialize(self, encoding = "unicode"):
        self._tidy()
        from lxml import etree
        return etree.tostring(self._construct(), encoding = encoding)

    def _construct(self, styleIndex = 0):
        from lxml import etree
        assert self._styles[0]['end'] >= self._styles[-1]['end'] # this represents one tree
        parent = None
        parentIndex = styleIndex - 1
        while parentIndex >= 0 and parent == None:
            if self._styles[parentIndex]['start'] <= self._styles[styleIndex]['start'] and self._styles[parentIndex]['end'] >= self._styles[styleIndex]['end']:
                parent = parentIndex
            parentIndex -= 1
        assert not styleIndex or parent != None
        result = etree.Element(self._styles[styleIndex]['name'], nsmap = self._nsmap)
        if not styleIndex and len(self._text) >= self._styles[styleIndex]['end']: result.tail = self._text[self._styles[styleIndex]['end']:]
        if self._styles[styleIndex]['attrib']:
            for attribute, value in self._styles[styleIndex]['attrib'].iteritems():
                result.set(attribute, value)
        if styleIndex == len(self._styles) - 1 or self._styles[styleIndex + 1]['start'] >= self._styles[styleIndex]['end']:
            result.text = self._text[self._styles[styleIndex]['start']:self._styles[styleIndex]['end']]
        else:
            result.text = self._text[self._styles[styleIndex]['start']:self._styles[styleIndex + 1]['start']]
        if not result.text: result.text = None
        doneUpTo = self._styles[styleIndex]['start']
        doneAll = True
        for n, style in enumerate(self._styles[styleIndex + 1:]):
            if style['start'] < doneUpTo: continue
            if style['start'] >= self._styles[styleIndex]['end']:
                tailTo = []
                if style['start'] > self._styles[styleIndex]['end'] and (not styleIndex or self._styles[parent]['end'] > self._styles[styleIndex]['end']):
                    tailTo.append(style['start'])
                    if styleIndex: tailTo.append(self._styles[parent]['end'])
                if tailTo:
                    result.tail = self._text[self._styles[styleIndex]['end']:min(tailTo)]
                doneAll = False
                break
            result.append(self._construct(n + styleIndex + 1))
            doneUpTo = style['end']
        if doneAll: # check if a tail needs adding
            if styleIndex and self._styles[parent]['end'] > self._styles[styleIndex]['end']: result.tail = self._text[self._styles[styleIndex]['end']:self._styles[parent]['end']]
        return result
