import card
import json
import os
import re 
import example_gen
from datetime import datetime

today = datetime.today()


path = input("Input the relative path and filename to json: ")
parse_yn = input("Enter '1' to do Theo specific string parsing.\n \
Enter anything else to skip string parsing: ")
with open(path, 'r', encoding='utf-8') as outfile: 
    data=json.load(outfile)

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
      "example_eng2" : " ",
    }
    cd["chars"] = note["fields"][0]
    # skip note["fields"][1], color, which is empty
    cd["pinyin"] = re.sub(r"[\<].*?[>]", "", note["fields"][2])
    eng_str = note["fields"][3].strip()
    eng_str=re.sub(r"[\<].*?[>]", "", eng_str)
    # replace Chinese parenthesis with standard English parenthesis
    eng_str=re.sub("（", "(", eng_str)
    eng_str=re.sub("）", ")", eng_str)
    if parse_yn == '1': 
        cd.update(example_gen.gen_ex(eng_str))
    else: 
        cd['english'] = eng_str
    card.Card.conn.execute(
        '''INSERT INTO vocabulary 
        (chars, pinyin, english, 
        example_eng0, example_eng1, example_eng2,
        example_ch0, example_ch1, example_ch2, 
        interval, next, ease, learning) 
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?, ?) ''', 
        [cd["chars"], cd["pinyin"], cd["english"],
        cd["example_eng0"], cd["example_eng1"], cd["example_eng2"],
        cd["example_ch0"], cd["example_ch1"], cd["example_ch2"],
        0, today, 0, True])

card.db.close(card.Card.conn)
    # card_list.append(cd)


# for c in card_list:
#     for member in c.__dict__.iteritems():
#         if not member[1]:
#             int(member[0])

# for i,c in enumerate(card_list): 
#     print(c)
    # card_list[i] = (c['chars'], c['pinyin'], c['english'],
    # c['example_eng0'], c['example_eng1'], c['example_eng2'],
    # c['example_ch0'], c['example_ch1'], c['example_ch2'],
    # today, 0, True )

# for cd in card_list: 
#     [print(r) for r in cd]


    
    
    # card_list)


# for card in card_list:
#     print(card)

# Filepath for convenience: 
# anki_decks\new\deck.json
