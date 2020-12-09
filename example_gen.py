'''
My Anki cards are written in a very specific way with leading pinyin within parenthesis, 
then the english definition
then optional sample sentence.  
This file takes in an english field with all the above fields, deletes the pinyin, 
and returns the definition (separated out) and up to three examples found within parenthesis as a dictionary. 
'''

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

def gen_ex(eng_str):
    card = {}
    # when leading parenthesis, it is a repeat of pinyin section; remove
    if eng_str[0] == '(': 
        ind = eng_str.find(')')
        if ind > 0: 
            eng_str = eng_str[ind+1:]
    # when trailing parenthesis, parse for example sentences
    if eng_str[-1] == '.':
        eng_str = eng_str[:-1]

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
                eng_str=eng_str[:open_paren]
    card['english'] = eng_str

    return card