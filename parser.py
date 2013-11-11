#!/usr/bin/python

import xml.etree.ElementTree as etree

tree = etree.parse('media.xml')
root = tree.getroot()

for track in root.findall("./dict/dict/dict/"):
	artist = 0
	name = 0
	for node in track:
		if node.tag == "key" and node.text == "Name":
			name = 1
		if node.tag == "string" and name == 1:
			nametext = node.text
			name = 0
		if node.tag == "key" and node.text == "Artist":
			artist = 1
		if node.tag == "string" and artist == 1:
			print node.text, "-", nametext
			artist = 0

