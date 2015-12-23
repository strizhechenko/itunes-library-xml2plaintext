#!/usr/bin/python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as etree

tree = etree.parse('media.xml')
root = tree.getroot()
artist = name = 0

for track in root.findall("./dict/dict/dict/"):
	if track.tag == "key" and track.text == "Name":
		name = 1
	if track.tag == "string" and name == 1:
		nametext = track.text
		name = 0
	if track.tag == "key" and track.text == "Artist":
		artist = 1
	if track.tag == "string" and artist == 1:
		line = u'%s - %s' % (track.text, nametext)
		print line.encode('utf-8')
		artist = 0

