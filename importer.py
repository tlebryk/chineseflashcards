import card
import json
import os
import re 

# index of opening parenthesis corresponding to a trailing parenthesis
def paren_match(myStr): 
    stack = []
    for ind, letter in enumerate(myStr[:-1]): 
        if letter == "(":
            stack.append(ind)
        elif letter == ")":
            if len(stack) > 0: 
                stack.pop()
    if stack and len(stack) ==1: 
        return stack[0]
    else:
        return None



trailingpara = 0

# fields from my anki deck
fields = ["chars", "color", "pinyin", "English" ]

path = input("Input the relative path and filename to json: ")

with open(path, 'r', encoding='utf-8') as outfile: 
    data=json.load(outfile)

card_list = []
counter = 0
for note in data['notes']: 
    counter +=1
    card = {}
    card["chars"] = note["fields"][0]
    # skip color which is empty
    card["pinyin"] = re.sub("[\<].*?[>]", "", note["fields"][2])
    eng_str = note["fields"][3].strip()
    eng_str=re.sub("[\<].*?[>]", "", eng_str)
    # replace Chinese parenthesis with standard English parenthesis
    eng_str=re.sub("（", "(", eng_str)
    eng_str=re.sub("）", ")", eng_str)


    # when leading parenthesis, it is a repeat of pinyin section; remove
    if eng_str[0] == '(': 
        ind = eng_str.find(')')
        if ind > 0: 
            eng_str = eng_str[ind+1:]
    # when trailing parenthesis, parse for example sentences
    if eng_str[-1] == ")": 
        open_paren = paren_match(eng_str)
        if open_paren: 
            tail_str = eng_str[open_paren:]
            # find indices of chinese characters to add to examples
            ch_iter = re.finditer(r'[\u4e00-\u9fff]+', tail_str)
            if ch_iter: 
                ch_inds = [m.span() for m in ch_iter]
                i=0
                # Add up to three examples to fields
                while i < min(len(ch_inds)-1, 2):
                    card["example_ch"+str(i)] = tail_str[ch_inds[i][0]:ch_inds[i][1]]
                    card["example_eng"+str(i)] = tail_str[ch_inds[i][1]+1: ch_inds[i+1][0]]
                    i +=1
                card["example_ch"+str(i)] = tail_str[ch_inds[i][0]:ch_inds[i][1]]
                card["example_eng"+str(i)] = tail_str[ch_inds[i][1]+1: -1]
                # slice off anything in tail parenthesis
                eng_str=eng_str[:open_paren-1]
    card['english'] = eng_str
    card_list.append(card)
print(card_list)

# Filepath for convenience: 
# anki_decks\new\deck.json
