import sys
import os 
import logging
import codecs
from gensim import corpora, models, similarities
from gensim.models.word2vec import Word2Vec  
from numpy import seterr
import numpy 
import nltk


class UserCommentLines(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for fname in os.listdir(self.dirname):
            if not (fname.find('user_')==0):
                continue
            fname = os.path.join(self.dirname, fname)
            if not os.path.isfile(fname):
                continue
            for line in open(fname):
                yield line.lower().split()

class UserCommentCorpus(object):
    
    def __init__(self, dirname, dictionary):
        self.dirname = dirname
        self.dictionary = dictionary

    def __iter__(self):
        self.user2doc = {}
        for fname in os.listdir(self.dirname):
            if not (fname.find('user_')==0):
                continue
            username = fname.split('_')[-1]
            fname = os.path.join(self.dirname, fname)
            if not os.path.isfile(fname):
                continue
            with codecs.open(fname) as f:
              lines = f.readlines()
            one_line_per_user = " ".join(lines)
            yield self.dictionary.doc2bow(one_line_per_user.lower().split())
   

def create_dictionary(user_comments_dir, dictionary_file):
  seterr(all='raise')  # don't ignore numpy errors
  stopset = set(nltk.corpus.stopwords.words('english'))
  dictionary = corpora.Dictionary(UserCommentLines(user_comments_dir))

  stop_ids = [dictionary.token2id[stopword] for stopword in stopset
              if stopword in dictionary.token2id]
  once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.iteritems() if docfreq == 1]
  dictionary.filter_tokens(stop_ids + once_ids) # remove stop words and words that appear only once
  dictionary.compactify() # remove gaps in id sequence after words that were removed
  logging.info("saving dictionary to %s" % dictionary_file)
  dictionary.save(dictionary_file)

def create_corpus(user_comments_dir, dictionary, corpus_file):
  dictionary = corpora.Dictionary().load(dictionary_file)
  corpus = UserCommentCorpus(user_comments_dir, dictionary)
  logging.info("saving corpus to %s" % corpus_file)
  corpora.MmCorpus.serialize(corpus_file, corpus)

# Example: ./genred.py ~/genred/clean_comments ~/genred/word2vec
if __name__ == "__main__":
  logging.basicConfig(format='%(asctime)s : %(threadName)s : %(levelname)s : %(message)s', level=logging.INFO)
  logging.info("running %s" % " ".join(sys.argv))
    
  # check and process cmdline input
  program = os.path.basename(sys.argv[0])
  user_comments_dir = './data/users'
  dictionary_file = user_comments_dir + '/dict_user_comments.dict'
  corpus_file =  user_comments_dir + '/corpus_user_comments.mm'
  
  if len(sys.argv) == 4:
    user_comments_dir = sys.argv[1]
    dictionary_file = sys.argv[2]
    corpus_file = sys.argv[3]

  create_dictionary(user_comments_dir,dictionary_file)
  create_corpus(user_comments_dir, dictionary_file,corpus_file)
