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
# Uni NLTK Project, this one gets the trainer going. getting the handclassified tweets from sanders corpora, extracting features out of em, then classifies
# http://ravikiranj.net/posts/2012/code/how-build-twitter-sentiment-analyzer/
# was very helpful while buildin this.

#from twython import Twython
#import tweepy
import pickle
import re
import os, errno
import csv
import nltk, nltk.classify.util, nltk.metrics
from nltk.classify import NaiveBayesClassifier

#TWITTER_APP_KEY = 'pv4cMWyxHLX6wqXLMfSjNgtop'
#TWITTER_APP_KEY_SECRET = 'EtyzC6hiyrZgsjIFrFQ0rjJXa5uCtAuEwyRvi2jwFjR4TR9ISD' 
#TWITTER_ACCESS_TOKEN = '618108661-JEjjpDxjRyPsdRcrWJkoGiGL1Sdmh0sKLtJJvQ2o'
#TWITTER_ACCESS_TOKEN_SECRET = 'fJXsdbJ98zzqbE0Msmdj1hsOu5WIwD6mmSLznmRiGALSk'

#auth = tweepy.OAuthHandler(TWITTER_APP_KEY, TWITTER_APP_KEY_SECRET)
#auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)

#api = tweepy.API(auth)

#t = Twython(app_key=TWITTER_APP_KEY, 
#            app_secret=TWITTER_APP_KEY_SECRET, 
#            oauth_token=TWITTER_ACCESS_TOKEN, 
#            oauth_token_secret=TWITTER_ACCESS_TOKEN_SECRET)

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
            
#start extract_features
def extract_features(tweet):
    tweet_words = set(tweet)
    features = {}
    for word in featureList:
        features['contains(%s)' % word] = (word in tweet_words)
    return features
#end           
            
            
            
#loading the corpus..
#inpTweets = csv.reader(open('datasets/Sentiment Analysis Dataset.csv', 'rb'), delimiter=',', quotechar='"')
inpTweets = csv.reader(open('datasets/training.1600000.processed.noemoticonutf.csv', 'rb'), delimiter=',', quotechar='"')
stopWords = buildStopWordList('features/stopwords.txt')
tweets = []
featureList = []
  
#for each row of the CVS corpora we want to get the tweet and beautify it.
n = 0
i = 0
for row in inpTweets:
    i = i+1
    if (i==1590):         #limiter
        n = n + 1
        if (row[0] == '0'):
            sentiment = row[0]
        elif (row[0] == '4'):
            sentiment = '1'
        i = 0
    #sentiment = row[0]
    #sentiment = row[1]
    #statusid = row[2]
        status_text = row[5]
    #status_text = row[3]
    #try:
    #    status = api.get_status(id=statusid)
    #except tweepy.TweepError as e:
    #    print e.message[0]['code']
    #    print e.args[0][0]['code']
    #print status.text.encode('utf-8')
    #featureVector = processTweet(status.text.encode('utf-8'))
        featureVector = processTweet(status_text.decode(encoding='utf-8',errors='ignore'))
    
    #if the list object comes empty we don't want to print anything  #COMMENTED because should not be needed in the training (the handclassified stuff should be beautiful) also.. could introduce some problems (rows vs sentiment)
    #if not featureVector:
    #    pass
    #else:
    
        print n
    #print featureVector
    #we'll need both the featurelist and the tweets variable, carrying tweets and sentiments
        featureList.extend(featureVector)                       #EXTEND [1, 2, 3, 4, 5]
        tweets.append((featureVector, sentiment))              #APPEND [1, 2, 3, [4, 5]]
    #if (n > 999):                                         #limiting the corpora... else you would expect to compute for 11 hours but occur in runtime errors in reality..
    #    break
    
    
# Removing duplicates
print "\nRemoving duplicates found in featureList.."
featureList = list(set(featureList))
print "\nSaving the featureList.."
flist = open('fList.pickle', 'w')
pickle.dump(featureList, flist)
flist.close()
# Generate the training set .. it has to eat the whole set of features and the trainset
print "\nGenerating training set.."
#bulk extraction
training_set = nltk.classify.util.apply_features(extract_features, tweets)

# Train the Naive Bayes classifier
print "\nTraining the classifier.."
NBClassifier = nltk.NaiveBayesClassifier.train(training_set)
fnbc = open('nb_classifier.pickle', 'w')
pickle.dump(NBClassifier, fnbc)
fnbc.close()
# DONE WITH THE CLASSIFIER
# DONE WITH THE CLASSIFIER
# DONE WITH THE CLASSIFIER
print  "\n\nSo.. I trained the classifier and I stored it in nb_classifier.pickle"
answer = 'y'
#answer = raw_input("\nDo you wish to try the Maximum Entropy Classifier even if you have no idea what it is? (y/n) "
#if (answer == 'y'):
#    #Maximum Entropy Classifier
#    MaxEntClassifier = nltk.classify.maxent.MaxentClassifier.train(training_set, 'GIS', trace=3, encoding=None, labels=None, sparse=True, gaussian_prior_sigma=0, max_iter = 10)
#    fmec = open('me_classifier.pickle', 'w')
#    pickle.dump(MaxEntClassifier, fmec)
#    fmec.close()
#    testTweet = "Awesome @AlbertoGloder, well done, that's great!"
#    processedTestTweet = processTweet(testTweet)
#    print MaxEntClassifier.classify(extract_features(buildFeatureVector(processedTestTweet)))
#    print MaxEntClassifier.show_most_informative_features(10)
#else:
#    print "Okay."
#TEST TIME
#TEST TIME
#TEST TIME

# Function to test the classifier, eats the classifier, the sets
def tester(classifier, test_set, training_set = ''):
    for i, (features, label) in enumerate(test_set):
        #referenceSets[label].add(i)
        predicted = classifier.classify(features)
        #print predicted
        #testSets[predicted].add(i)
    print "Train on %d instances, test on %d instances" % (len(training_set), len(test_set))
    print "Accuracy:", nltk.classify.util.accuracy(classifier, test_set)
    classifier.show_most_informative_features(10)
    
# ASKING USER IF HE WANTS TO TEST
# ASKING USER IF HE WANTS TO TEST
answer =  raw_input("Do we want to test how well it does (y/n)? ")
if (answer == 'y'):
    while (answer == 'y'):
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
        tester (NBClassifier, test_set, training_set)
        answer = raw_input("\nDo you wish to do more tests (y/n)? ")
else:
    pass

    
print "\n\nFinally done."




