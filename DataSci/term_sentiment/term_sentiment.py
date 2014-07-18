import sys
import json
from collections import defaultdict
import re

def main():
  sentiment_scores = sentiment_input('AFINN-111.txt')
  tweets_parsed = data_parse('output.txt')
  derive_sentiment(tweets_parsed, sentiment_scores)

#convert sentiment file data into dictionary structure stored in memory
def sentiment_input(sentiment_dict_file):
  afinnfile = open(sentiment_dict_file)
  scores = {} 
  for line in afinnfile:
    term, score  = line.split("\t")  #the file is tab-delimited. 
    scores[term] = int(score)  
  return scores

#parse the Twitter data in the appropriate format
def data_parse(tweet_data_file):
  tweets = {}
  tweet_count = 1
  data = open(tweet_data_file) #Twitter JSON data
  for jsonstring in data:
      entry = json.loads(jsonstring)
      try:
          tweets[tweet_count] = unicode.split(entry['text'])
          tweet_count += 1
      except KeyError:
          pass
  return tweets

#derive sentiment of new terms that do not appear in the sentiment dictionary
def derive_sentiment(tweets, scores):
  new_terms = defaultdict(list)
  for tweet in tweets: 
    tweet_tally = []
    term_list = []
    for word in tweets[tweet]:
        word = standardize(word)
        if word not in scores.keys():  
            term_list.append(word)
        else:
            tweet_tally.append(scores[word])
    for i in term_list:
      new_terms[i].extend(tweet_tally) 
  for key, value in new_terms.iteritems():
    if len(value) == 0:
      print unicode(key) + " N/A"
    else:
      print unicode(key) + " " + str(float(sum(value))/len(value)) #printing to autograder in accepted format

#remove special characters from start/end of string and convert to lowercase
def standardize(string):
    string = re.sub('^[#@,;:!"_\-\.\?\'\(\)\[\]\^\*]+', '', string)
    word = re.sub('[#@,;:!"_\-\.\?\'\(\)\[\]\^\*]+$', '', string)
    word = word.lower()
    return word

if __name__ == "__main__":
    main()
