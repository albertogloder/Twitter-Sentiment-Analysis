# -*- coding: utf-8 -*-
#'''
#               (`.         ,-,
#               `\ `.    ,;' /
#                \`. \ ,'/ .'
#          __     `.\ Y /.'
#       .-'  ''--.._` ` (
#     .'            /   `
#    ,           ` '   Q '
#    ,         ,   `._    \
#    |         '     `-.;_'
#    `  ;    `  ` --,.._;
#    `    ,   )   .'
#     `._ ,  '   /_
#        ; ,''-,;' ``-
#         ``-..__\``--`  ag
#'''
# Uni NLTK Project, this one loads the featureVectors from the CVS file, loads the classifier and classifies the tweets.
# http://ravikiranj.net/posts/2012/code/how-build-twitter-sentiment-analyzer/
# was very helpful while buildin this.

import pickle
import nltk, nltk.classify.util, nltk.metrics, nltk.data
from nltk.classify import NaiveBayesClassifier
import csv

#start extract_features
def extract_features(tweet):
    tweet_words = set(tweet)
    features = {}
    for word in featureList:
        features['contains(%s)' % word] = (word in tweet_words)
    return features
#end 

hashtag = raw_input("Please enter the hashtag of the test file (just the hashtag! without #!) ")
test_file = csv.reader(open('tester/processed_data/' + hashtag + '.csv', 'rb'), delimiter=',', quotechar='"')
up_file = open('tester/processed_data/'+ hashtag + '.txt', 'r')
line = up_file.readline()


#c_name = raw_input("Please feed me the classifier (Naive Bayes vs Max Entropy), (nb/me) "
clssfr = pickle.load(open('trainer/nb_classifier.pickle'))
#clssfr = pickle.load(open('trainer/' + c_name + '_classifier.pickle'))
#f = open('trainer/' + c_name + '_classifier.pickle')
#classifier = pickle.load(f)
#f.close()

featureList = pickle.load(open('trainer/fList.pickle'))
#loopy loopy
#n=0
for row in test_file:
    features = row
    #featureList = list(set(featureList))       #not going to check for duplicates
    prediction = clssfr.classify(extract_features(features))
    #n = n + 1
    print "Tweet:" + line + "\nPrediction:" + prediction + "\n"
    line = up_file.readline()
    