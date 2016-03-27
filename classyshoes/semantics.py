from os.path import isfile
from random import shuffle
from string import punctuation
from multiprocessing import cpu_count

from gensim.models.doc2vec import TaggedDocument, Doc2Vec
from gensim.utils import simple_preprocess

from classyshoes.db import Review
from classyshoes.language import mkStemmer, mkTokenizer, mkStopper


# Pre-process text for training and querying
def mkCanonical(text, stemmer, tokenizer, stopper):
    tokens = [stemmer(token).lower() for token in tokenizer(text) if token not in punctuation]
    return [word for word in tokens if not stopper(word)]


# Pre-processes a review and attaches labels to it
def mkTaggedDocument(review, stemmer, tokenizer, stopper):
    articleId = review.articleId

    title = mkCanonical(review.title, stemmer, tokenizer, stopper)
    description = mkCanonical(review.description, stemmer, tokenizer, stopper)

    words = title + description
    tags = [articleId]

    return TaggedDocument(words, tags)


# Streaming access to review pre-processed for usage as documents
def mkLabeledReviews(session, language):
    stemmer = mkStemmer(language)
    tokenizer = mkTokenizer(language)
    stopper = mkStopper(language)

    for review in session.query(Review).all():
        yield mkTaggedDocument(review, stemmer, tokenizer, stopper)


# Trains a distributed representation of documents model showing the progress
def mkTrainedModel(documents, progress, epochs=10):
    model = Doc2Vec(size=300, window=10, min_count=1, sample=1e-5, workers=cpu_count(), alpha=0.025, min_alpha=0.025)

    model.build_vocab(documents)

    rate = 0.002

    for epoch in progress(range(epochs)):
        shuffle(documents)

        model.train(documents)

        model.alpha -= rate
        model.min_alpha = model.alpha

    return model


# Semantics based on labeled text corpus; transparently caches trained model
def mkModel(documents, path, progress):
    if isfile(path):
        model = Doc2Vec.load(path)
    else:
        model = mkTrainedModel(documents, progress)
        model.save(path, pickle_protocol=3)

    return model
