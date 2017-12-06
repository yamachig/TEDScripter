# -*- coding: utf-8 -*-

from pyquery import PyQuery as pq
import requests
import re

def get_script_data(talk_id, lang):

    page = pq(f'https://www.ted.com/talks/{talk_id}/transcript?language={lang}')
    transcript = requests.get(f'https://www.ted.com/talks/{talk_id}/transcript.json?language={lang}').json()

    times = [
        cue['time']
        for paragraph in transcript['paragraphs']
        for cue in paragraph['cues']
    ]

    data = {
        'description': page('meta[itemprop=description]').attr('content'),
        'title': page('title').text().split('|')[0].strip(),
        'script': [
            [
                (cue['time'], cue['text'])
                for cue in paragraph['cues']
            ]
            for paragraph in transcript['paragraphs']
        ],
        'times': times,
    }

    return data

def get_talk(talk_id):

    langs = ['ja', 'en']
    data = {}
    for lang in langs:
        script = get_script_data(talk_id, lang)
        for key, value in script.items():
            if not key in data:
                data[key] = {}
            data[key][lang] = value

    metadata = requests.get(f'https://hls.ted.com/talks/{talk_id}.json').json()

    data['start_time'] = metadata['timing']['content']['start']
    data['talk_id'] = talk_id

    m3u8 = requests.get(f'https://hls.ted.com/talks/{talk_id}.m3u8').text
    match0 = re.search(r'^#EXT-X-MEDIA:TYPE=AUDIO.*?URI="(.+?\.m3u8).*?$', m3u8, re.MULTILINE)
    if match0:
        audio_m3u8 = requests.get(f'https://hls.ted.com{match0[1]}').text
        match1 = re.search(r'^https://pb.tedcdn.com/talk/hls/audio/.*?\.aac$', audio_m3u8, re.MULTILINE)
        if match1:
            data['audio_url'] = match1[0].strip()

    return data