# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 08:43:18 2019

@author: Jana
"""

from nltk.corpus.reader import mte
import string


def clean_untagged(sents):
    s_clean = []
    
    for se in sents:
        missing = False
        for w in se:
            if w[0] not in string.punctuation and w[1] == '':
                missing = True
        if not missing:
            s_clean.append(se)
            
    return s_clean
        

def tags_only(corpus):
    res = []
    
    for sent in corpus:
        cand = []
        for word in sent:
            sig = ""
            if word[0] not in string.punctuation:
                sig = shorten(word[1])
                cand.append(sig.upper())
        if cand not in res:
            res.append(cand)
            
    return res
            
            
def shorten(word):
    sig = ""
    
    if word[0] == "#":
        if word[1] == "N":
            sig = word[1] + word[3] + word[4] + word[6]
        elif word[1] == "V":
            sig = word[1] + word[2] + word[3] + word[4] + word[5]
            for i in [6,7,8,14]:
                if len(word) >= i+1:
                    sig += word[i]
        elif word[1] == "A":
            if len(word) == 8:
                sig = word[1] + word[4] + word[5] + word[7]
            if len(word) == 7:
                sig = word[1] + word[4] + word[5] + word[6]
        elif word[1] == "P":
            sig = word[1] + word[2] + word[3] + word[4] + \
            word[5] + word[6]
            for i in [9,12]:
                if len(word) >= i+1:
                    sig += word[i]
        elif word[1] == "M":
            sig = word[1] + word[3] + word[4]
            for i in [7]:
                if len(word) >= i+1:
                    sig += word[i]
        elif word[1] == "R":
            sig = "ADV"
        elif word[1] == "S":
            sig = "ADP"
        elif word[1] == "C":
            sig = word[1] + word[3]
        elif word[1] == "Q":
            sig = "PART"
        elif word[1] == "I":
            sig = "I"
        elif word[1] == "Y":
            sig = "ABBR"
        elif word[1] == "X":
            sig = "RES"
    else:
        if word[0] == "N":
            sig = word[0] + word[2] + word[3] + word[5]
        elif word[0] == "V":
            sig = word[0] + word[1] + word[2] + word[3] + word[4]
            for i in [5,6,7,13]:
                if len(word) >= i+1:
                    sig += word[i]
        elif word[0] == "A":
            if len(word) == 7:
                sig = word[0] + word[3] + word[4] + word[6]
            if len(word) == 6:
                sig = word[0] + word[3] + word[4] + word[5]
        elif word[0] == "P":
            sig = word[0] + word[1] + word[2] + word[3] + \
            word[4] + word[5]
            for i in [8,11]:
                if len(word) >= i+1:
                    sig += word[i]
        elif word[0] == "M":
            sig = word[0] + word[2] + word[3]
            for i in [6]:
                if len(word) >= i+1:
                    sig += word[i]
        elif word[0] == "R":
            sig = "ADV"
        elif word[0] == "S":
            sig = "ADP"
        elif word[0] == "C":
            sig = word[0] + word[2]
        elif word[0] == "Q":
            sig = "PART"
        elif word[0] == "I":
            sig = "I"
        elif word[0] == "Y":
            sig = "ABBR"
        elif word[0] == "X":
            sig = "RES"
            
    return sig.upper()


def base_rules(tags, d):
    for w in tags:
        if len(w[1]) >= 1:
            short = shorten(w[1])
            if short in d and w[0].lower() not in d[short]:
                d[short].append(w[0].lower())
            elif short not in d:
                d[short] = [w[0].lower()]
                
                
'''
for i in range(len(t_str)):
    if len(t[i]) == 1:
        gr_dict["S"].append(t_str[i])
    else:
 ''' 

def find_w(w, grt):
    res = []
    for nt in grt:
        if w in grt[nt]:
            res.append(nt)
    return res


def check_sent(sent, grnt, grt):
    temp_gr = grnt[:]
    temp_gr2 = grnt[:]
    i = 0
    while temp_gr != [] and i < len(sent):
        word = sent[i]
        start = find_w(word, grt)
        for s in temp_gr:
            if i < len(s) and s[i] not in start:
                temp_gr2.remove(s)
        temp_gr = temp_gr2[:]
        i += 1
    if temp_gr != [] and i == len(sent):
        return True
    return False
        
        
def add_w(tag,word,d):
    if tag in d:
        d[tag].append(word)
    else:
        d[tag] = word
        
def add_r(new_rule, rules):
    if new_rule not in rules:
        rules.append(new_rule)
        
def main():
    f = open("all.txt", "r", encoding="utf8")
    lines = f.readlines()
    grnt = []
    grt = dict()
    for line in lines:
        sp = line.split(" --> ")
        if sp[0] == "S":
            grnt.append(sp[1][1:-1].split(" "))
        else:
            grt[sp[0]] = []
            sp2 = sp[1].split(" | ")
            for i in range(len(sp2)-1):
                grt[sp[0]].append(sp2[i])
            grt[sp[0]].append(sp2[len(sp2)-1][:-1])
    task = input("Enter task (check/add word/add sent): ")
    if task == "check":
        sent = input("Enter sentence: ")
        to_test = sent[-1].split(" ")
        to_test = [w.lower() for w in to_test]
        if check_sent(to_test, grnt, grt):
            print("Sentence is correct.")
        else:
            print("Sentece not found.")
    if task == "add word":
        tag = input("Enter tag: ")
        word = input("Enter word: ")
        add_w(tag, word, grt)
        print("Word added.")
    if task == "add sent":
        new_rule = input("Enter sent: ")
        add_r(new_rule, grnt)
        print("Sentence added.")
