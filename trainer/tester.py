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
# Uni NLTK Project, this one tests classifiers we already have built on a small test dataset
# http://ravikiranj.net/posts/2012/code/how-build-twitter-sentiment-analyzer/
# was very helpful while buildin this.

import pickle
import re
import os, errno
import csv
import nltk, nltk.classify.util, nltk.metrics
from nltk.classify import NaiveBayesClassifier
from veryScaryTrainer import buildStopWordList, processTweet, extract_features, tester

    
# ASKING USER IF HE WANTS TO TEST
# ASKING USER IF HE WANTS TO TEST
answer = 'y'
answer =  raw_input("Do we want to test how well a classifier does (y/n)? ")
if (answer == 'y'):
    while (answer == 'y'):
        folderino = raw_input("Please insert the folder for the classifier. ")
        classifier = pickle.load(open(folderino+'/nb_classifier.pickle'))
        featureList = pickle.load(open(folderino+'/fList.pickle'))
        #we want to reset featureList and tweets everytime, getting them ready for the testdata
        tweets = []
        #featureList = []
        print "Testing on pre-labeled SENTIMENT140 testing data.."
        testTweets = csv.reader(open('datasets/testdata.manual.2009.06.14.csv', 'rb'), delimiter=',', quotechar='"')
        for row in testTweets:
            #gotta make the two datasets like eachother
            if row[0] == '2':
                pass
            else:
                if (row[0] == '0'):
                    sentiment = row[0]
                elif (row[0] == '4'):
                    #sentiment = row[0]
                    sentiment = '1'
                #sentiment = row[0]
                status_text = row[5]
                featureVector = processTweet(status_text.decode('utf-8'))
                #featureList.extend(featureVector)
                tweets.append((featureVector, sentiment))
                #sentiment = NBClassifier.classify(extract_features(buildFeatureVector(processedTestTweet, stopWords)))
                #print "testTweet = %s, sentiment = %s\n" % (testTweet, sentiment)
        print "\n\nCreating test set"
        #featureList = list(set(featureList))
        #bulk extraction
        test_set = nltk.classify.util.apply_features(extract_features, tweets)
        tester (classifier, test_set)
        answer = raw_input("\nDo you wish to test on more classifiers (y/n)? ")
else:
    pass
