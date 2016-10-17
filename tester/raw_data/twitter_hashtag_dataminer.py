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
# Uni NLTK Project, this one fetches tweets and puts them in a graceful manner on a .txt file

from twython import Twython
import os, errno
# wow such dev
TWITTER_APP_KEY = 'somekey'
TWITTER_APP_KEY_SECRET = 'somekey' 
TWITTER_ACCESS_TOKEN = 'somekey'
TWITTER_ACCESS_TOKEN_SECRET = 'somekey'

t = Twython(app_key=TWITTER_APP_KEY, 
            app_secret=TWITTER_APP_KEY_SECRET, 
            oauth_token=TWITTER_ACCESS_TOKEN, 
            oauth_token_secret=TWITTER_ACCESS_TOKEN_SECRET)

#Asking the user for the hashtag.... can't ask for #xxx coz i can't name the file with # for additional processing            
hashtag = raw_input("Please enter the hashtag you want to check out (xxx without #) ")
#Asking the user.. Popular or Recent
pr = raw_input("Search for popular or recent? (popular/recent) ")
search = t.search(q="#"+hashtag, result_type=pr,  #whatever query
                  count=100)    #goodluck with that


tweets = search['statuses']
#goodstuff is a deprecated string (useless) will keep for no reason
#goodstuff = []

#Our files are going to be saved in dir and named tweets_xxxxxxxxxxxxxxxx.txt   (can't name em with an # in the middle)
filename = 'tweets_'+hashtag+'.txt'
#If the path doesn't exist pls do the file/folder
if not os.path.isfile(filename):
  try:
    print "The file does not exist, making it."
    #os.makedirs(os.path.dirname(filename)) #old for dirs
    open(filename, 'a').close()
  except OSError as exception: # Python >2.5
    if exception.errno == errno.EEXIST and os.path.isdir(filename):
      pass
    else: raise
    
#for all the tweets found...
for tweet in tweets:
  #print tweet['text'].encode('utf-8') + "\n"
  #goodstuff.append(tweet['text'].encode('utf-8') + "\n")
  #goodstuff.append(tweet['id_str'], '\n', tweet['text'], '\n\n\n')
  #I just like to watch.
  print tweet['text'].encode('utf-8')
  #Appending more tweets every cycle, dat \n
  with open (filename, 'a') as text_file:
    text_file.write(tweet['text'].encode('utf-8') + "\n")
    text_file.flush()
    
print  "\n\nDone. Saved items to /" + filename

#with open(filename, 'w') as text_file:
#  text_file.write(goodstuff)
  

