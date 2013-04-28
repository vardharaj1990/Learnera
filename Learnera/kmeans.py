# Author: Peter Prettenhofer <peter.prettenhofer@gmail.com>
#         Lars Buitinck <L.J.Buitinck@uva.nl>
# License: Simplified BSD

from __future__ import print_function

from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn import metrics
import Read_Data
from collections import defaultdict

from sklearn.cluster import KMeans, MiniBatchKMeans

import logging
from optparse import OptionParser
import sys
from time import time

import numpy as np


# Display progress logs on stdout
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')

# parse commandline arguments
op = OptionParser()
op.add_option("--no-minibatch",
              action="store_false", dest="minibatch", default=False,
              help="Use ordinary k-means algorithm (in batch mode).")
op.add_option("--no-idf",
              action="store_false", dest="use_idf", default=True,
              help="Disable Inverse Document Frequency feature weighting.")
op.add_option("--use-hashing",
              action="store_true", default=False,
              help="Use a hashing feature vectorizer")
op.add_option("--n-features", type=int, default=10000,
              help="Maximum number of features (dimensions)"
                   "to extract from text.")

print(__doc__)
op.print_help()

(opts, args) = op.parse_args()
if len(args) > 0:
    op.error("this script takes no arguments.")
    sys.exit(1)


###############################################################################
# Load some categories from the training set

def getLabels(coursedict):
    training_documents = list()
    coursekeys = list()
    for key in coursedict:
            training_documents.append(coursedict[key] + '' + key)
            coursekeys.append(key)

    true_k = 300

    #print("Extracting features from the training dataset using a sparse vectorizer")
    t0 = time()
    if opts.use_hashing:
        if opts.use_idf:
            # Perform an IDF normalization on the output of HashingVectorizer
            hasher = HashingVectorizer(n_features=opts.n_features,
                                       stop_words='english', non_negative=True,
                                       norm=None, binary=False)
            vectorizer = Pipeline((
                ('hasher', hasher),
                ('tf_idf', TfidfTransformer())
            ))
        else:
            vectorizer = HashingVectorizer(n_features=opts.n_features,
                                           stop_words='english',
                                           non_negative=False, norm='l2',
                                           binary=False)
    else:
        vectorizer = TfidfVectorizer(max_df=0.2, max_features=opts.n_features,
                                     stop_words='english', use_idf=opts.use_idf)
    X = vectorizer.fit_transform(training_documents)

   # print("done in %fs" % (time() - t0))
   # print("n_samples: %d, n_features: %d" % X.shape)
    #print()


    ###############################################################################
    # Do the actual clustering

    if opts.minibatch:
        km = MiniBatchKMeans(n_clusters=true_k, init='k-means++', n_init=1,
                             init_size=1000,
                             batch_size=1000, verbose=0)
    else:
        km = KMeans(n_clusters=true_k, init='k-means++', max_iter=500, n_init=1,
                    verbose=0)

    #print("Clustering sparse data with %s" % km)
    t0 = time()
    km.fit(X)

    print(km.labels_)


    clusterdict = defaultdict(int)
    for i in range(0,len(km.labels_)):
        clusterdict[coursekeys[i]] = km.labels_[i]

    return clusterdict
