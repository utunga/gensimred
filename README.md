gensimred
=========

Playing with word2vec and reddit data

dependencies
------------

At the moment there is a heavy dependency on gensim (in fact on the development
branch - so as to have the word2vec model included). 

Unfortunately getting that to work nicely means getting
- scipy (hency gfortran and a BLAS library)
- numpy
- cython 
working.. and then installing gensim from the development branch. 

You also want to make sure you have good BLAS support in the setup so things run fast. 

This code also depends on a few other python libraries
gresource, nltk and resource. I have listed dependencies
in setup.py but, hmm yeah I havent tested setup.py 
yet so 'python setup.py install' may not work

usage
-----

Very much a work in progress but currently to use you would 
1. Install dependencies
1. Run python then 'import nltk\n nltk.download()' and use the gui to download wordnet corpus 
1. download_comments.py
1. download_user_comments.py
1. create_user_comment_dictionary.py
1. train_model.py
1. vectorize_users.py
