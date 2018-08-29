#!/usr/bin/python
# -*- coding: utf-8 -*-

# richText class manages a block of text and a list of items with ranges of the text to which they apply.
# the items are dicts so you can add your own properties to them.  'name', 'start' and 'end' are reserved.
# items may cover zero or more characters within the text (one or more if allowEmpties is false)

# TODO could use a networkx network instead of a list of dicts for the items for added functionality

from copy import deepcopy

class richText:

    def __init__(self, text = "", allowEmpties = True):
        self._styles = []
        self._text = text
        self._allowEmpties = allowEmpties

    def _tidy(self):
        if self._allowEmpties: return
        toRemove = list(m for m, style in enumerate(self._styles) if style['start'] == style['end'])
        for m in reversed(toRemove): del self._styles[m]

    def _checkRange(self, start, end):
        assert start < end or start == end and self._allowEmpties
        assert end <= len(self._text)

    def add(self, tag, start, end, **kwargs):
        self._checkRange(start, end)
        item = deepcopy(kwargs)
        item['name'] = tag
        item['start'] = start
        item['end'] = end
        self._styles.append(item)

    def removeAll(self, tag):
        toRemove = list(m for m, style in enumerate(self._styles) if style['name'] == tag)
        for m in reversed(toRemove): del self._styles[m]

    def getRanges(self, tag):
        ranges = []
        for style in self._styles:
            if style['name'] == tag: ranges.append([style['start'], style['end']])
        return ranges

    def getText(self):
        return self._text

    def insert(self, text, offset):
        assert offset <= len(self._text)
        self._text = self._text[:offset] + text + self._text[offset:]
        for n, style in enumerate(self._styles):
            if style['start'] >= offset: style['start'] += len(text)
            if style['end'] > offset: style['end'] += len(text)

    def delete(self, start, end):
        self._checkRange(start, end)
        self._text = self._text[:start] + self._text[end:]
        removed = end - start
        for n, style in enumerate(self._styles):
            if style['start'] > start: style['start'] = max(start, style['start'] - removed)
            if style['end'] > start: style['end'] = max(start, style['end'] - removed)
        self._tidy()
