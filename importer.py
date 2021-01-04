import card
import json
import os
import re 
import example_gen
from datetime import date
from datetime import timedelta
import spaced_rep

'''json_import takes a json of anki exported deck of Hanzi cards, saves it into the vocabulary database,
and returns number of cards written.
 parser parses input for examples as specified by example_gen for specially formatted "english" fields. 
Expected JSON format has all of desired information in notes['fields'] section.
Sample format: 
 {
     ...
     "notes": [
        {
            "__type__": "Note",
            "fields": [
                "变化",
                "<span class=\"tone4\">变</span><span class=\"tone4\">化</span>",
                "<span class=\"tone4\">biàn</span><span class=\"tone4\">huà</span> <!-- bian hua -->",
                "（biànhuà）<br>change <br>（v/n; 你的老家有没有变化=has your hometown changed/ is there changes）",
                "[sound:变化_google_zh-cn.mp3]"
            ],
        }, 
        ...
        ]
    }
'''

def json_import(path, parser = True):
    today = date.today()
    with open(path, 'r', encoding='utf-8') as outfile: 
        data=json.load(outfile)
    card_count = 0
    for note in data['notes']: 
        cd = {
        "chars" : " ",  
        "english" : " ",
        "pinyin" : " ",
        "example_ch0" : " ",
        "example_ch1" : " ",
        "example_ch2" : " ",
        "example_eng0" : " ",
        "example_eng1" : " ",
        "example_eng2" : " ",}
        cd["chars"] = note["fields"][0]
        # skip note["fields"][1], color, which is empty
        cd["pinyin"] = re.sub(r"[\<].*?[>]", "", note["fields"][2])
        eng_str = note["fields"][3].strip()
        eng_str=re.sub(r"[\<].*?[>]", "", eng_str)
        # replace Chinese parenthesis with standard English parenthesis
        eng_str=re.sub("（", "(", eng_str)
        eng_str=re.sub("）", ")", eng_str)
        if parser: 
            cd.update(example_gen.gen_ex(eng_str))
        else: 
            cd['english'] = eng_str


        card.Card.conn.execute(
            '''INSERT INTO vocabulary 
            (chars, pinyin, english, 
            example_eng0, example_eng1, example_eng2,
            example_ch0, example_ch1, example_ch2, 
            last, next, ease, learning) 
            VALUES(?,?,?,?,?,?,?,?,?,NULL,?,?, ?, ?,?,?) ''', 
            [cd["chars"], cd["pinyin"], cd["english"],
            cd["example_eng0"], cd["example_eng1"], cd["example_eng2"],
            cd["example_ch0"], cd["example_ch1"], cd["example_ch2"],
            today - timedelta(days=1), 0, False, 
            cd['alpha'], cd['beta'], cd['t']])

        card_count+=1
    card.db.close(card.Card.conn)
    return card_count

# Filepath for convenience: 
sample_path= "anki_decks\\new\\deck.json"