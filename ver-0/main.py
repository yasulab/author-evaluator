#!/usr/bin/python
#! -*- coding: utf-8 -*-

import sys
import re
import os
import math, random

def read_file(filename):
    if os.path.exists('./'+filename) == False:
        print "No such a file."
        return        
    input = open(filename, "r")
    return input.read()        

def prompt():
    filename = "alice.txt"
    given_text = read_file(filename) # init text
    print "Text Analyzer"
    print "-------------"
    help = \
    "Commands:\n" \
    + "\trand NUMBER   : Randomly pick a word given times.\n" \
    + "\tread FILENAME : Read a given file.\n" \
    + "\tstats         : Show stats of recently read text.\n" \
    + "\thelp          : Show this.\n" \
    + "\texit          : Exit.\n"
    print help
    print "Current Text: ", filename
    print ""
    word_dict = analyze(given_text)
    while 1:
        input = raw_input("["+filename+"]> ")
        cmd_list = input.split(" ")
        if cmd_list[0] == "exit":
            exit()
        elif cmd_list[0] == "help":
            print help
        elif cmd_list[0] == "rand":
            if len(cmd_list) == 1:
                print "Give me how many times you pick."
                continue
            times = int(cmd_list[1])
            print "Number of words: %.f" % get_num_of_words(given_text)
            print
            pick_rand(given_text, times)
        elif cmd_list[0] == "read":
            if len(cmd_list) == 1:
                print "Give me a filename."
                continue
            filename = cmd_list[1]
            given_text = read_file(filename)
        elif cmd_list[0] == "stats":
            word_dict = analyze(given_text)
            print "Number of words: %.f" % get_num_of_words(given_text)
            print
            show_dict(word_dict)
        elif cmd_list[0] == "":
            continue
        else:
            print "Unknown command: " + cmd_list[0]

def get_num_of_words(given_text):
    return len(get_word_list(given_text))

def pick_rand(word_dict):
    rand = random.random() * len(word_dict)
    index = int(math.floor(rand))
    word = word_dict[index][1]
    return word

def get_dict_length(word_dict):
    num_of_words = 0.0
    for count,word in word_dict:
        num_of_words += count
    return num_of_words

def show_dict(word_dict):
    num_of_words = get_dict_length(word_dict)
    print "TOP 10 - MOST FRQUENTLY USED WORDS"
    print "COUNT\t|\tWORD\t|\tPROB [%]\t"
    for count, word in word_dict[:10]:
        print count, "\t|\t", word, "\t|\t", "%.2f" %  (count / num_of_words*100)
    print

def show_all_dict(word_dict):
    num_of_words = get_dict_length(word_dict)
    print "COUNT |\tPROB[%] | WORD\t"
    sum_prob = 0
    for count, word in word_dict:
        prob = (count / num_of_words) * 100
        print "%5d | %.2f    | %s" % \
              (count, prob, word)
        sum_prob += prob
    print
    #print sum_prob
    
def get_word_list(text):
    p = re.compile(r'\W+')
    return  p.split(text)

"""
TODO: make it log calculation.
"""
def analyze(given_text, given_num_of_words):
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
        if num_of_words > float(given_num_of_words):
            break
    # sort by count
    word_dict = [(v,k) for k,v in word_dict.items()]
    word_dict.sort()
    word_dict.reverse()
    return word_dict

def show_last_sentence(given_text, given_num_of_words):
    word_list = get_word_list(given_text)
    word_list = word_list[:int(given_num_of_words)]
    word_list.reverse()
    sentence = []
    for word in word_list:
        sentence.append(word)
        if not word:
            continue
        if word[0].isupper():
            break
    sentence.reverse()
    print "Last Sentence:",
    for word in sentence:
        print word,
    print
    
if __name__ == "__main__":
    argv_len = len(sys.argv)
    if not argv_len == 3:
        print "Usage: python text-analyzer.py FILENAME NUM_OF_WORDS"
        exit()
    filename = sys.argv[1]
    given_num_of_words = sys.argv[2]
    #print filename
    #prompt()
    given_text = read_file(filename) # init text
    word_dict = analyze(given_text, given_num_of_words)
    show_all_dict(word_dict)
    show_last_sentence(given_text, given_num_of_words)
    print "Next word:", pick_rand(word_dict)
    
    








