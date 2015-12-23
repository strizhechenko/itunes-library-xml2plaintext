__author__ = 'oleg'
# coding:utf-8

import pylast
import xml.etree.ElementTree as etree
from config import api_key, api_secret, username, password_hash
from time import time



def get_scrobbler():
    network = pylast.LastFMNetwork(api_key = api_key,
                                   api_secret = api_secret,
                                   username = username,
                                   password_hash = password_hash)
    return network


def parse_itunes_xml(source):
    artist = 0
    name = 0
    track_id = 0
    count = 0
    tree_root = etree.parse(source).getroot()
    tracks = {}
    for track in tree_root.findall("./dict/dict/"):
        if track.tag == 'dict':
            track_info = {
                "artist": None,
                "track": None,
                "track_id": None,
                "count": None
            }
            for node in track:
                if node.tag == 'key':
                    if node.text == 'Artist':
                        artist = 1
                    elif node.text == 'Name':
                        name = 1
                    elif node.text == 'Track ID':
                        track_id = 1
                    elif node.text == 'Play Count':
                        count = 1
                    else:
                        continue

                if node.tag == 'integer' and track_id == 1:
                    track_info['track_id'] = int(node.text)
                    track_id = 0
                elif node.tag == 'string' and artist == 1:
                    track_info['artist'] = node.text.lower()
                    artist = 0
                elif node.tag == 'string' and name == 1:
                    track_info['track'] = node.text.lower()
                    name = 0
                elif node.tag == 'integer' and count == 1:
                    track_info['count'] = int(node.text)
                    count = 0

                if track_info['artist'] and track_info['track'] and track_info['count'] and track_info['track_id']:
                    tracks[track_info['track_id']] = track_info
                    break
    return tracks


def diff_itunes(old, new):
    diff = {}
    for track in new:
        if track in old:
            if old[track]['count'] == new[track]['count']:
                continue
            diff[track] = new[track]
            diff[track]['count'] = new[track]['count'] - old[track]['count']
        else:
            diff[track] = new[track]
    return diff


def scrobble(track, scrobbler):
    scrobbler.scrobble(artist=track['artist'], title=track['track'], timestamp=str(int(time())))

def scrobble_them(diff):
    for track in diff:
        for listen in range(0, diff[track]['count']):
            scrobble(diff[track], get_scrobbler())
    return None


def main():
    track_dict_old = parse_itunes_xml('itunes_old.xml')
    track_dict_new = parse_itunes_xml('itunes_new.xml')
    track_dict_diff = diff_itunes(track_dict_old, track_dict_new)
    scrobble_them(track_dict_diff)


main()
