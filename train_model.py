import sys
import os 
import logging
from gensim import corpora, models, similarities
from gensim.models.word2vec import Word2Vec  
from numpy import seterr

class CommentCorpus(object):
    """Iterate over sentences from the Brown corpus (part of NLTK data)."""
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for fname in os.listdir(self.dirname):
            fname = os.path.join(self.dirname, fname)
            if not os.path.isfile(fname):
                continue
            for line in open(fname):
                words = [word for word in line.split(' ')]
                if not words:  # don't bother sending out empty sentences
                    continue
                yield words

def train(corpus_dir, model_file):
  seterr(all='raise')  # don't ignore numpy errors
  #train word2vec model on comment corpus
  model = Word2Vec(CommentCorpus(comments_dir), size=200, min_count=5, workers=4)
  
  model.save(model_file + '.model')
  # model.save_word2vec_format(model_file + '.model.bin', binary=True)
  # model.save_word2vec_format(model_file + '.model.txt', binary=False)

  logging.info("finished running %s" % program)

  # double check
  # word1='raised'
  # word2='other'
  # similarity = model.similarity(word1,word2)
  # logging.info("similarity of \'%s\' and \'%s\' is %f" % (word1,word2,similarity))


# Example: ./genred.py ~/genred/clean_comments ~/genred/word2vec
if __name__ == "__main__":
  logging.basicConfig(format='%(asctime)s : %(threadName)s : %(levelname)s : %(message)s', level=logging.INFO)
  logging.info("running %s" % " ".join(sys.argv))
    
  # check and process cmdline input
  program = os.path.basename(sys.argv[0])
  comments_dir = './comments'
  model_file = 'word2vec'
  if len(sys.argv) == 2:
    comments_dir = sys.argv[1]
    model_file = sys.argv[2]

  train(comments_dir, model_file)
  