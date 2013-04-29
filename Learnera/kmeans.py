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
	
    vectorizer = TfidfVectorizer(max_df=0.2, max_features=10000,
                                     stop_words='english', use_idf=True)
    X = vectorizer.fit_transform(training_documents)

    km = KMeans(n_clusters=true_k, init='k-means++', max_iter=500, n_init=1,
                    verbose=0)

    print("Clustering sparse data with %s" % km)
    t0 = time()
    km.fit(X)

    print(km.labels_)


    clusterdict = defaultdict(int)
    for i in range(0,len(km.labels_)):
        clusterdict[coursekeys[i]] = km.labels_[i]

    return clusterdict
