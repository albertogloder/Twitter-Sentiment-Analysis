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
import csv


#initialize stopWords
stopWords = []

#builds the list of stopwords, loading them from a file since hardcoding would be terrible
def buildStopWordList(stopWordListFileName):    
    #stopwords string
    stopWords = []
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
    
    
#Processing function, turning tweets in feature vectors we can give to our nltk program
def processTweet(tweet):
    
    featureVector = []
    #We need TWEETS to be lowercase ... also to match with stopWords..
    tweet = tweet.lower()
    
    #Convert www.* or https?://* to nothin      #re.sub(pattern, repl, string, count=0, flags=0) Return the string obtained by replacing the leftmost non-overlapping occurrences of pattern in string by the replacement repl.
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', ' ', tweet) #' '
    
    #Convert @username to nothin
    tweet = re.sub('@[^\s]+', ' ', tweet) #' '
    
    #We don't need too many white spaces
    tweet = re.sub('[\s]+', ' ', tweet)
    
    #We don't like hashtags
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    
    #trim
    tweet = tweet.strip('\'"')
    
    #now playing INSIDE words
    #splitting the tweet into words
    words = tweet.split()
    for w in words:
    
        #replacing two or more with two occurrences eg. daaaaaamn
        pattern = re.compile(r"(.)\1{1,}", re.DOTALL) 
        w = pattern.sub(r"\1\1", w)
        
        #kill punctuation
        w = w.strip('\'"?,.')
        
        #If the word does not start with some alphabetic stuff it's useless
        val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*[a-zA-Z]+[a-zA-Z0-9]*$", w)
        #so we'll be skipping writing on the vector if the word is a stopWord or it's a non-alphabetic element
        if(w in stopWords or val is None):
            continue
        else:
            featureVector.append(w)
    
    return featureVector



#Loading the stopwords..
st = open('features/stopwords.txt', 'r')
stopWords = buildStopWordList('features/stopwords.txt')

#Read the RAW tweets one by one and process it.. asking for hashtag coz easier use
hashtag = raw_input("Please enter the hashtag of the raw data .txt (just the hashtag! without #!) ")
raw_file = open('raw_data/tweets_'+ hashtag +'.txt', 'r')
line = raw_file.readline()

#Creating / Updatin the processed file
pro_filename = 'processed_data/'+ hashtag +'.csv'

#Usual 'dircheck' -> makedir
try:                                        #we want to delete the old file if it's there.
  #os.makedirs(os.path.dirname(pro_filename))
  open(pro_filename, 'wb').close()
except OSError as exc: # Python >2.5
  if exc.errno == errno.EEXIST and os.path.isdir(pro_filename):
    pass
  else: raise
#Creating / Updatin the raw tweet file
up_filename = 'processed_data/'+ hashtag +'.txt'
#Usual 'dircheck' -> makedir
try:                                        #we want to delete the old file if it's there.
  #os.makedirs(os.path.dirname(pro_filename))
  open(up_filename, 'w').close()
except OSError as exc: # Python >2.5
  if exc.errno == errno.EEXIST and os.path.isdir(up_filename):
    pass
  else: raise
  
#loopy loopy
while line:
    featureVector = processTweet(line)
    #if the list object comes empty we don't want to print anything
    if not featureVector:
        line = raw_file.readline()
    else:
        print featureVector
        #this tweet is readable.. so i am saving it for the final comparison
        with open (up_filename, 'a') as text_file:
            text_file.write(line)
            text_file.flush()
        with open (pro_filename, 'a') as csvfile:
            spamWriter = csv.writer(csvfile, delimiter=',',
                            quotechar='"', lineterminator='\n')#, quoting=csv.QUOTE_MINIMAL)
            #writing off the processed tweet in a new file, line per line
            spamWriter.writerow(featureVector)
            #text_file.write(', '.join(featureVector) + "\n")
            #text_file.flush()
        line = raw_file.readline()

raw_file.close()
print "\n\nDone. Saved items to /"+ up_filename + " and /" + pro_filename