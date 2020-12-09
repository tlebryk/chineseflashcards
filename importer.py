import card
import json
import os
import re 
import example_gen

path = input("Input the relative path and filename to json: ")
parse_yn = input("Enter '1' to do Theo specific string parsing.\n \
Enter anything else to skip string parsing: ")
with open(path, 'r', encoding='utf-8') as outfile: 
    data=json.load(outfile)

card_list = []
for note in data['notes']: 
    cd = {}
    cd["chars"] = note["fields"][0]
    # skip note["fields"][1], color, which is empty
    cd["pinyin"] = re.sub(r"[\<].*?[>]", "", note["fields"][2])
    eng_str = note["fields"][3].strip()
    eng_str=re.sub(r"[\<].*?[>]", "", eng_str)
    # replace Chinese parenthesis with standard English parenthesis
    eng_str=re.sub("（", "(", eng_str)
    eng_str=re.sub("）", ")", eng_str)
    # print(parse_yn)
    # print(parse_yn=='1')
    if parse_yn == '1': 
        cd.update(example_gen.gen_ex(eng_str))
    else: 
        cd['english'] = eng_str
    print(card.card(**cd))
    card_list.append(card)
# for card in card_list:
#     print(card)

# Filepath for convenience: 
# anki_decks\new\deck.json
