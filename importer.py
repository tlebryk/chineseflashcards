import card
import json
import os
import re 

# fields from my anki deck
fields = ["chars", "color", "pinyin", "English" ]

path = input("Input the relative path and filename to json: ")

with open(path, 'r', encoding='utf-8') as outfile: 
    data=json.load(outfile)

for note in data['notes'][:10]: 
    card = {}
    card["chars"] = note["fields"][0]
    # skip color which is empty
    card["pinyin"] = note["fields"][2]
    eng_str = note["fields"][3].strip()
    # when leading parenthesis, it is a repeat of pinyin section; remove
    if eng_str[0] == '(': 
        ind = eng_str.find(')')
        if ind > 0: 
            eng_str = eng_str[ind+1]
    # when trailing parenthesis, parse to find examples
    if eng_str[-1] == ")":
        start = eng_str.rfind('(')
        if start > 0: 
            # find all chinese characters and indices
            chin_iter = re.finditer(r'[\u4e00-\u9fff]+', eng_str[start:])
            if chin_iter: 
                ch_inds = [(m.span(), m[0]) for m in chin_iter]
                last = ch_inds[0][1]
                i=0
                while i < len(ch_inds)-1 and i < 3:
                    card["example_ch"+str(i+1)] = ch_inds[i][1]
                    card["example_eng"+str(i+1)] = eng_str[start:][last: ch_inds[i+1][0][0]]
                    print("ch ex", card["example_ch"+str(i+1)])
                    print("eng ex", card["example_eng"+str(i+1)])
                    last = eng_str[start:][last: ch_inds[i+1][0][1]]
                    i+=1
                # card["example_ch"+str(i+1)] = ch_inds[i][1]
                # card["example_eng"+str(i+1)] = eng_str[start:][last:-1]
                # print(card["example_ch"+str(i)])
                # print(card["example_eng"+str(i)])


            

            # for i in range(max(len(ch_inds),3)): 
            #     card["example_ch"+str(i)] = ch_inds[i][1]
            #     card["example_eng"+str(i)] = eng_str[start:][last]
            # print(ch_inds)
            # eng_inds = [(ch_inds[i][1], ch_inds[i+1][0]) for i in range(len(ch_inds-1))]
            # eng_exs_inds.append(ch_inds[i][1+1], -1)
            # for i in range(max(3,len(ch_inds))):
            #     card["example_ch"+str(i)] = eng_str[start:][ch_inds[i][0]:ch_inds[i][1]]
            #     card["example_eng"+str(i)] = eng_str[start:][eng_inds[i][0]:eng_inds[i][1]]
            #     print(card["example_ch"+str(i)])
            #     print(card["example_eng"+str(i)])



            # eng_ex
            # for ind, ex in enumerate(chin_ex):
            #     card["example_ch"+str(ind)] = ex
             

        

    # print(eng_str)

        

# Extract all Chinese characters in utf_line
# chars = re.findall(r'[\u4e00-\u9fff]+',utf_line)

#relative path: 
# anki_decks/new/deck.json


# print(list(data.keys))