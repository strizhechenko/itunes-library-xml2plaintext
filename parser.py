#!/usr/bin/python
# -*- coding: utf-8 -*-
""" Разбирает медиатеку itunes и приводит её к plaintext списку песен """

from plistlib import readPlist

have_tags = lambda t: t.get('Artist') and t.get('Name')
unpack = lambda t: (t['Artist'], t['Name'])

tracks = readPlist('media.xml')['Tracks'].values()

for artist, name in map(unpack, filter(have_tags, tracks)):
    print artist.encode('utf-8'), '-', name.encode('utf-8')
