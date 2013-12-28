import sys
import os 
import logging
from gensim import corpora, models, similarities
from gensim.models.word2vec import Word2Vec  
from numpy import seterr


def query_word_similarity(model_file, word1, word2):
  seterr(all='raise')  # don't ignore numpy errors

  #load model from given file
  model = Word2Vec.load(model_file + '.model')
  similarity = model.similarity(word1,word2)
  logging.info("similarity of \'%s\' and \'%s\' is %f" % (word1,word2,similarity))

# Example: ./query_model.py word1 word2
if __name__ == "__main__":
  logging.basicConfig(format='%(asctime)s : %(threadName)s : %(levelname)s : %(message)s', level=logging.INFO)
  logging.info("running %s" % " ".join(sys.argv))
   
  # check and process cmdline input
  program = os.path.basename(sys.argv[0])
  model_file = 'word2vec'
  word1 = 'brother'
  word2 = 'sister'
  if len(sys.argv) == 4:
    model_file = sys.argv[1]
    word1 = sys.argv[2]
    word2 = sys.argv[3]

  if len(sys.argv) == 3:
    word1 = sys.argv[1]
    word2 = sys.argv[2]

  query_word_similarity(model_file, word1, word2)
  