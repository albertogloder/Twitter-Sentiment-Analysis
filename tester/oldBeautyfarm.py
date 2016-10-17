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
# Uni NLTK Project, this one gets rid of useless data that would not provide any value and would make the classifier worse.
# feature selection reducing dimensionality
# we don't want stopwords (es conjunctions), repeating letters (daaaamn), punctuation (not always useless but too hard) or numbers
# http://ravikiranj.net/posts/2012/code/how-build-twitter-sentiment-analyzer/
# was very helpful while buildin this.

#import regex to be able to process..
import re
import os, errno



#initialize stopWords
stopWords = []

#builds the list of stopwords, loading them from a file since hardcoding would be terrible
def buildStopWordList(stopWordListFileName):    
    #stopwords string
    stopWords = []
    stopWords.append('AT_USER')
    stopWords.append('URL')
    #opens stopwords.txt
    fp = open(stopWordListFileName, 'r')
    line = fp.readline()
    #for every line..
    while line:
        word = line.strip() #to avoid the newline char messing around
        stopWords.append(word)
        line = fp.readline()
    fp.close()
    return stopWords
    
    
#Processing function
def processTweet(tweet):

    #We need them lowercase
    tweet = tweet.lower()
    #Convert www.* or https?://* to URL
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',tweet)
    #Convert @username to AT_USER
    tweet = re.sub('@[^\s]+','AT_USER',tweet)
    #We don't need too many white spaces
    tweet = re.sub('[\s]+', ' ', tweet)
    #We don't like hashtags
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    #trim
    tweet = tweet.strip('\'"')
    return tweet

#The processed file
pro_filename = 'processeddata/'+ hashtag +'.txt'
#Usual 'dircheck' -> makedir
if not os.path.exists(os.path.dirname(pro_filename)):
  try:
    os.makedirs(os.path.dirname(pro_filename))
  except OSError as exc: # Python >2.5
    if exc.errno == errno.EEXIST and os.path.isdir(path):
      pass
    else: raise
    
    
#Read the tweets one by one and process it.. asking for hashtag coz easier use
hashtag = raw_input("Please enter the hashtag of the raw data .txt (just the hashtag! without #!) ")
raw_file = open('rawdata/tweets_'+ hashtag +'.txt', 'r')
line = raw_file.readline()


#loopy loopy
while line:
    processedTweet = processTweet(line)
    print processedTweet
    with open (pro_filename, 'a') as text_file:
        text_file.write(processedTweet + "\n")
        text_file.flush()
    line = raw_file.readline()

raw_file.close()
print "\n\nDone."