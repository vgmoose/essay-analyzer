#!/usr/bin/python

import os

try:
    from nltk import pos_tag, word_tokenize
except:
    print("the nltk module isn't available.")

#configure folders
samples = "../samples"
output = "../output"

pos_tag(word_tokenize("starting nltk"))

for name in os.listdir(samples):
    new_file = open(output + "/"+name+".pos", "w");
    file = open(samples+"/"+name, "r")
    for line in file:
        new_file.write(str(pos_tag(word_tokenize(line))))
        new_file.write("\n")