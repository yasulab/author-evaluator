#!/usr/bin/python
#! -*- coding: utf-8 -*-

import sys
import re
import os
import copy
import math, random
from optparse import OptionParser

COUNTER = 0
WORD = 1
VFLAG = False

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

def get_ptable_len(ptable):
    num_of_words = 0.0
    for word in ptable:
        for next_word in ptable[word]:
            num_of_words += ptable[word][next_word]
    return num_of_words

def show_all_ptable(ptable):
    ptable_len = get_ptable_len(ptable)
    sum_prob = 0
    for word in ptable:
        print "WORD |\tPROB[%]  | NEXT_WORD\t"
        print word
        for nw in ptable[word]:
            print "\t%1f | %s" % ((float(ptable[word][nw]) / \
                                  float(ptable_len))*100,
                                  nw)
        print
    print
    
def get_word_list(text):
    p = re.compile(r'\W+')
    return  p.split(text)

def get_unigram(given_text, given_num_of_words):
    word_list = get_word_list(given_text)
    unigram = dict()
    num_of_words = 0.0
    for word in word_list:
        if not word:
            continue
        word = word.lower()
        unigram[word] = unigram.get(word, 0) + 1
        num_of_words += 1.0
        #print num_of_words, given_num_of_words
        if given_num_of_words == 0:
            continue
        elif num_of_words > float(given_num_of_words):
            break
    return unigram

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

def create_ptable(unigram, bigram):
    ptable = copy.deepcopy(bigram)
    for pw in bigram:
        if not pw:
            continue
        for w in bigram[pw]:
            """
            P(w|prev) = (P(prev|w)P(w)) / P(prev)
            """
            ptable[pw][w] = (bigram[pw][w] * unigram[w])/unigram[pw]
    return ptable
        
if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option(
        "-v", "--verbose",
        action="store_true",
        default=False,
        help="display information verbosely."
        )
    parser.add_option(
        "-f", "--file", 
        type="string",
        default="vicar-excerpt.txt",
        help="choose a text file for analyzing. This program uses 'vicar-excerpt.txt' by default."
        )
    parser.add_option(
        "-n", "--num", 
        type="int",
        default=0,
        help="choose how many words are input. This program reads all words  by default. Please see README for details."
        )
    (options, args) = parser.parse_args() 
    VFLAG = options.verbose
    filename = options.file
    given_num_of_words = options.num
    
    given_text = read_file(filename) # init text
    # adapt for a negative input.
    given_num_of_words = get_reversed_given_num(given_text, given_num_of_words)
    unigram = get_unigram(given_text, given_num_of_words)
    bigram = get_bigram(given_text, given_num_of_words)
    ptable = create_ptable(unigram, bigram)
    
    if VFLAG == True: show_all_ptable(ptable)
    last_sentence = get_last_sentence(given_text, given_num_of_words)
    print "Last Sentence:",
    for word in last_sentence:
        print word,
    print
    last_word = last_sentence[len(last_sentence)-1]
    #print last_word
    print "Next word:", pick_rand(bigram, last_word)
    
