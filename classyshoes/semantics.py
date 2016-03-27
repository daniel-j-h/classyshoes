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
def mkTrainedModel(documents, path, progress, epochs=10):
    alpha = 0.025
    alpha_min = 0.001
    alpha_delta = (alpha - alpha_min) / epochs

    model = Doc2Vec(size=300, window=5, min_count=1, sample=1e-5, workers=cpu_count())

    model.build_vocab(documents)

    for epoch in progress(range(epochs)):
        shuffle(documents)

        model.alpha = alpha
        model.min_alpha = alpha

        model.train(documents)

        alpha -= alpha_delta

    model.save(path, pickle_protocol=3)

    return model


# Loads an existing model from disk
def mkExistingTrainedModel(path):
    return Doc2Vec.load(path)
