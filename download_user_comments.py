import sys
import re
import codecs 
import grequests
import requests
import nltk 
import logging
from nltk.tokenize.punkt import PunktWordTokenizer

from api_path import api 
api_users = api + '/users?page={0}'
api_user_comments = api + '/users/{0}/comments?page={1}'

out_file_tmpl = 'data/users/user_{0}'

# woops I discovered that not setting this can hammer
# the server hard enough to break it .. I think?
MAX_PARALLEL_REQUESTS = 15

#all the cleverness of nltk.word_tokenizer gets me nowhere so just use a regexp!!
# # not sure the right way to signify this dependency  
# # but for the tokenizer to work right you want to follow instructions 
# # on getting nltk data sets here:
# # http://nltk.org/data.html
# # (basically run nltk.download() in a python shell and pops up a magic gui thing)
# # then download nltk_data/tokenizers/punkt under models, punkt
# sentence_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
# # word tokenizer, only works on sentences, apparently

regexp_tokenizer = nltk.tokenize.RegexpTokenizer(r'(?:[A-Z][.])+|\d[\d,.:\-/\d]*\d|\w+[\w\-\'.&|@:/]*\w+')

def clean_by_tokenize(text):
	one_line = re.sub("\n", " ", text)
	# words = [word 
	# 		for sent in sentence_tokenizer.tokenize(one_line) 
	# 		for word in nltk.word_tokenize(sent)]
	words = [word.lower() for word in regexp_tokenizer.tokenize(one_line)]
	clean_line = " ".join(words)
	return clean_line + '\n'
	
def parse_user_comments(resp):
	print "Status: [%s] URL: %s" % (resp.status_code, resp.url)
	data = resp.json()
	page_num = data['page']
	username = users_to_fetch[resp.url].lower()
	file_name = out_file_tmpl.format(username)
	print "About to tokenize to " + file_name
	with codecs.open(file_name, 'w', 'utf-8') as outfile:
		for line in data['comments']:
			outfile.write(clean_by_tokenize(line['body']))
	
def parse_user_index(resp):
	print "Status: [%s] URL: %s" % (resp.status_code, resp.url)
	data = resp.json()
	page_num = data['page']
	for line in data['users']:
		comment_count = line['comment_count']
		if (comment_count>0):
			username = line['username']
			comments_url = line['comments']
			users_to_fetch[comments_url] = username
	
def parallel_fetch(urls, call_back):
    rs = (grequests.get(u) for u in urls)
    for resp in grequests.map(rs, size=MAX_PARALLEL_REQUESTS):
        call_back(resp) 

logging.basicConfig(format='%(asctime)s : %(threadName)s : %(levelname)s : %(message)s', level=logging.INFO)
 
#do a request to work out how many pages first..
response = requests.get(api + '/users')
data = response.json()
total_pages = data['total_pages']


#for debug 
#total_pages=3
urls = [api_users.format(page) for page in xrange(1, total_pages+1)]
users_to_fetch = {}
parallel_fetch(urls, parse_user_index)
parallel_fetch(users_to_fetch.keys(), parse_user_comments)
