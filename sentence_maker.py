# -*- coding: utf-8 -*-

import nltk
import sys
import random

def getSentenceArrays(contents):
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    return sent_detector.tokenize(contents.strip())
                                
# open the file and load its contents
file = open(sys.argv[1])
contents = file.read()

# get array of sentence arrays of words
sentences = getSentenceArrays(contents)

# tokenized sentences
tok_sents = []

for line in sentences:
    tok_sents.append(nltk.word_tokenize(line))

def draw(dict):
    total = 0
    for key in dict:
        total += dict[key]
    rando = random.uniform(0, total)
    for key in dict:
        total -= dict[key]
        if total - rando <= 0:
            return key

class Model:
    
    def __init__(self, sentences, n):
        self.sentences = sentences
        self.n = n
        self.ngrams = {}
    
        self.breakdown()
    #self.normalize()
    
    def sample_sentence(self):
        tokens = ["**START**"]*(self.n-1)
        
        while tokens[-1] != "**END**":
            prefix = tuple(tokens[-(self.n-1):])
            tokens.append(draw(self.ngrams[prefix]))

        return self.jointokens(tokens, self.n-1)


    def jointokens(self,tokens,n):
        specials = [".",",","?","!","”","'"]
        stripme = ["**START** ", " **END**"]
        sentence = ' '.join(tokens)
        for char in specials:
            sentence = sentence.replace(' '+char, char)
        sentence = sentence[10*n:]
        sentence = sentence[:-8:]
#        sentence = sentence.rstrip(" **END**")
        return sentence
    
    def normalize(self):
        for prefix in self.ngrams:
            count = 0.0
            for suffix in self.ngrams[prefix]:
                count += self.ngrams[prefix][suffix]
            for suffix in self.ngrams[prefix]:
                self.ngrams[prefix][suffix] = self.ngrams[prefix][suffix]/count

    def breakdown(self):
        for sentence in self.sentences:
            sentence = ["**START**"]*(self.n-1) + sentence + ["**END**"]*(self.n-1)
            ngram_line = nltk.ngrams(sentence, self.n)

            for ngram_pair in ngram_line:
                ngram_pair = tuple(ngram_pair)
                
                prefix = ngram_pair[:-1:]
                suffix = ngram_pair[-1]
                
                if prefix in self.ngrams:
                    self.ngrams[prefix]
                else:
                    self.ngrams[prefix] = {}
                
                if suffix in self.ngrams[prefix]:
                    self.ngrams[prefix][suffix] += 1
                else:
                    self.ngrams[prefix][suffix] = 1
                


# create statistical model for sentences
for n in range(2, 4):
    print "\nn-gram size where n="+str(n)+"\n-------------"
    model = Model(tok_sents, 3)
    for x in range(0, 10):
        print model.sample_sentence()
