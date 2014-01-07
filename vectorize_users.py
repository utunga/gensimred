import sys
import os 
import logging
import codecs
from gensim import corpora, models, similarities
from gensim.models.word2vec import Word2Vec  
from numpy import seterr
import numpy 


from numpy import exp, dot, outer, random, dtype, get_include, float32 as REAL,\
    uint32, seterr, array, uint8, vstack, argsort, fromstring, sqrt, newaxis

from gensim import utils, matutils  # utility fnc for pickling, common scipy operations etc

logger = logging.getLogger("vectorize_users")

def vectorize(model_file, dictionary_file, corpus_file):
  seterr(all='raise')  # don't ignore numpy errors

  #load model from given file
  model = Word2Vec.load(model_file)
  dictionary = corpora.Dictionary().load(dictionary_file)
  corpus = corpora.MmCorpus(corpus_file)
  tfidf = models.TfidfModel(corpus)
  d = corpora.Dictionary()
  d = d.load(dictionary_file)
  corpus = corpora.MmCorpus(corpus_file)
  tf = models.TfidfModel(corpus)
  vectorize = []
  for doc_no, tdoc in enumerate(tf[corpus]):
    tdoc.sort(key=lambda kv: kv[1], reverse=True)
    if doc_no % 100 == 0:
          logger.info("PROGRESS: vectorizing user #%i of %i" %
              (doc_no, len(corpus)))
    words_per_user = 8
    word_vecs = []
    for wordid, measure in tdoc:
      word = d[wordid]
      if word in model:
        word_vecs.append(model[word])
        print word
      if len(word_vecs)>=words_per_user:
        break

    if len(word_vecs)==words_per_user:
      avg = matutils.unitvec(array(word_vecs).mean(axis=0)).astype(REAL)
      vectorize.append(avg)
      #print [word for word, measure in model.most_similar_from_array(avg, topn=5)]
  
  return vectorize
  
# Example: ./genred.py ~/genred/clean_comments ~/genred/word2vec
if __name__ == "__main__":
  logging.basicConfig(format='%(asctime)s : %(threadName)s : %(levelname)s : %(message)s', level=logging.INFO)
  logging.info("running %s" % " ".join(sys.argv))
    
  # check and process cmdline input
  program = os.path.basename(sys.argv[0])
  user_comments_dir = './data/users'
  dictionary_file = user_comments_dir + '/dict_user_comments.dict'
  corpus_file =  user_comments_dir + '/corpus_user_comments.mm'
  model_file = 'word2vec.model'
  vectorized_csv_file = 'vectorized.csv'

  if len(sys.argv) == 4:
    model_file = sys.argv[1]
    dictionary_file = sys.argv[2]
    corpus_file = sys.argv[3]

  vectorized = vectorize(model_file, dictionary_file, corpus_file)
  numpy.savetxt(vectorized_csv_file, vectorized, delimiter=",")
