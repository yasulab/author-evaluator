#!/usr/bin/python
#! -*- coding: utf-8 -*-

import sys
import re
import os
import math, random

COUNTER = 0
WORD = 1

def read_file(filename):
    if os.path.exists('./'+filename) == False:
        print "No such a file."
        return        
    input = open(filename, "r")
    return input.read()        

def get_num_of_words(given_text):
    return len(get_word_list(given_text))

def pick_rand(word_dict, last_word):
    next_word = ""
    if word_dict.has_key(last_word):
        rand = random.random() * len(word_dict[last_word])
        index = int(math.floor(rand))
        counter = 0
        for i,word in enumerate(word_dict[last_word]):
            counter += word_dict[last_word][word]
            if counter >= rand:
                next_word = word
                break
    else:
        next_word = "There are no possible words."
    return next_word

def get_dict_length(word_dict):
    """
    num_of_words = 0.0
    for count,word in word_dict:
        num_of_words += count
    """
    return len(word_dict)

def show_all_dict(word_dict):
    num_of_words = get_dict_length(word_dict)
    sum_prob = 0
    for i,word in enumerate(word_dict):
        print "\tCOUNT |\tPROB[%]   | NEXT_WORD\t"
        print word
        for pw in word_dict[word]:
            print "\t%5d | %1f | %s" % (word_dict[word][pw],
                                        float(word_dict[word][pw]) / \
                                        float(len(word_dict[word]))*100,
                                        pw)
        print
    print
    
def get_word_list(text):
    p = re.compile(r'\W+')
    return  p.split(text)

def get_unigram(given_text, given_num_of_words):
    word_list = get_word_list(given_text)
    word_dict = dict()
    num_of_words = 0.0
    for word in word_list:
        if not word:
            continue
        word = word.lower()
        word_dict[word] = word_dict.get(word, 0) + 1
        num_of_words += 1.0
        #print num_of_words, given_num_of_words
        if given_num_of_words == 0:
            continue
        elif num_of_words > float(given_num_of_words):
            break
    # sort by count
    word_dict = [(v,k) for k,v in word_dict.items()]
    word_dict.sort()
    word_dict.reverse()
    return word_dict

def get_bigram(given_text, given_num_of_words):
    word_list = get_word_list(given_text)
    word_dict = dict()
    num_of_words = 0.0
    prev_word = ""
    for word in word_list:
        if not word:
            continue
        word = word.lower()
        if not word_dict.has_key(prev_word):
            #print word
            word_dict[prev_word] = dict()
        #print "DUP: ", word
        word_dict[prev_word][word] = \
             word_dict.get(prev_word, WORD).get(word, COUNTER) + 1
        num_of_words += 1.0
        prev_word = word
        #print num_of_words, given_num_of_words
        if given_num_of_words == 0:
            continue
        elif num_of_words > float(given_num_of_words):
            break
    # sort by count
    #print word_dict
    """
    word_dict = [(v,k) for k,v in word_dict.items()]
    word_dict.sort()
    word_dict.reverse()
    """
    """
    for i in range(len(word_dict)):
        print word_dict[i][0]
        temp_dict = word_dict[i][0].items()
        print temp_dict
        temp_dict = [(v,k) for v,k in temp_dict]
        print temp_dict
        word_dict[i][0].update(temp_dict)
        print word_dict[i][0]
    #print word_dict
    #exit()
    """
    return word_dict

def get_last_sentence(given_text, given_num_of_words):
    word_list = get_word_list(given_text)
    if not given_num_of_words == 0:
        word_list = word_list[:given_num_of_words]
    for i,word in enumerate(word_list):
        if not word:
            word_list.pop(i)
    word_list.reverse()
    sentence = []
    for word in word_list:
        sentence.append(word)
        if not word:
            continue
        if word[0].isupper():
            break
    sentence.reverse()
    return sentence

def get_reversed_given_num(given_text, given_num_of_words):
    word_list = get_word_list(given_text)
    if given_num_of_words < 0:
        return len(word_list) + given_num_of_words
    else:
        return given_num_of_words
    
if __name__ == "__main__":
    argv_len = len(sys.argv)
    if not argv_len == 3:
        print "Usage: python main.py FILENAME NUM_OF_WORDS"
        exit()
    filename = sys.argv[1]
    given_num_of_words = int(sys.argv[2])
    #print given_num_of_words
    #prompt()
    given_text = read_file(filename) # init text
    given_num_of_words = get_reversed_given_num(given_text, given_num_of_words)
    word_dict = get_bigram(given_text, given_num_of_words)
    show_all_dict(word_dict)
    last_sentence = get_last_sentence(given_text, given_num_of_words)
    print "Last Sentence:",
    for word in last_sentence:
        print word,
    print
    last_word = last_sentence[len(last_sentence)-1]
    #print last_word
    print "Next word:", pick_rand(word_dict, last_word)
    
    








