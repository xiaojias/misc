#!/usr/bin/python
# -*- coding: utf-8 -*-

# docHierarchy adds non-overlap requirement and associated tricks to the richText content editor class

from richText import richText

class docHierarchy(richText):

    def __init__(self):
        richText.__init__(self)
        self._splitMergeFilter = lambda tag : True

    def setSplitMergeFilter(self, callback):
        self._splitMergeFilter = callback

    def _tidy(self):
        richText._tidy(self)
        # fix the order before attempting anything hierarchy-related
        self._styles.sort(key = lambda style: [style['start'], - style['end']])
        # tidy everything up
        isClean = False
        while not isClean:
            isClean = True
            toRemove = []
            for n, style in enumerate(self._styles):
                if not n: continue
                previous = n - 1
                while previous >= 0 and (previous in toRemove  or previous > 0 and self._styles[previous]['end'] <= self._styles[previous - 1]['end']): previous -= 1
                if previous < 0: continue
                if style['name'] == self._styles[previous]['name'] and self._splitMergeFilter(style['name']):
                    if style['start'] == self._styles[previous]['end']: # merge adjacent matching elements
                        # don't merge if the result would overlap a parent
                        parent = previous - 1
                        while parent >= 0 and (parent in toRemove or (self._styles[parent]['end'] != style['start'])): parent -= 1
                        if parent == -1:
                            self._styles[previous]['end'] = style['end']
                            toRemove.append(n)
                    elif style['start'] < self._styles[previous]['end']: # merge matching child elements
                        toRemove.append(n)
            if toRemove:
                isClean = False # well, it might be now - we'll find out next time
                for n in reversed(toRemove):
                    del self._styles[n]
                # and fix the order again if any merged elements should become a parent
                self._styles.sort(key = lambda style: [style['start'], - style['end']])

    def add(self, tag, start, end, **kwargs):
        # split styles where necessary
        splits = []
        for m, style in enumerate(reversed(self._styles)):
            splitOn = None
            if style['start'] < start and style['end'] > start and style['end'] < end: splitOn = start
            if style['start'] < end and style['end'] > end and style['start'] > start: splitOn = end
            if splitOn:
                    if not self._splitMergeFilter(style['name']): return
                    else: splits.append((len(self._styles) - 1 - m, splitOn))
        for n, splitOn in splits:
            firstHalf = self._styles[n].copy()
            firstHalf['end'] = splitOn
            secondHalf = self._styles[n].copy()
            secondHalf['start'] = splitOn
            self._styles = self._styles[:n] + [firstHalf, secondHalf] + self._styles[n + 1:]
        # and insert the item
        richText.add(self, tag, start, end, **kwargs)
        self._tidy()

    def removeAll(self, tag):
        richText.removeAll(self, tag)
        self._tidy()

    def delete(self, start, end):
        richText.delete(self, start, end)
        self._tidy()
