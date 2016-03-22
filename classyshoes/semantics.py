from os.path import isfile
from multiprocessing import cpu_count

from gensim.models.doc2vec import TaggedDocument, Doc2Vec
from gensim.utils import simple_preprocess

from classyshoes.db import Review


# Streaming access to review pre-processed for usage as documents
def mkLabeledReviews(session):
    for review in session.query(Review).all():
        articleId = review.articleId

        title = simple_preprocess(review.title)
        description = simple_preprocess(review.description)

        # Generate tags carrying semantic based on review attributes
        rating = 'RATING_GOOD' if review.rating > 3 else 'RATING_BAD'
        recommend = 'RECOMMEND_GOOD' if review.recommend else 'RECOMMEND_BAD'
        helpful = 'HELPFUL_GOOD' if review.helpfulCount > review.unhelpfulCount else 'HELPFUL_BAD'

        words = title + description
        # TODO(daniel-j-h): experiment with additional tags; first try was not that promising
        tags = [articleId] #, rating, recommend, helpful]

        yield TaggedDocument(words, tags)


# Trains a distributed representation of documents model showing the progress
def mkTrainedModel(documents, progress, epochs=10):
    model = Doc2Vec(size=300, window=15, min_count=1, workers=cpu_count(), alpha=0.025, min_alpha=0.025)
    model.build_vocab(documents)

    rate = 0.002
    decay = 0

    for epoch in progress(range(epochs)):
        model.train(documents)
        model.alpha -= rate
        model.min_alpha -= decay

    return model


# Semantics based on labeled text corpus; transparently caches trained model
def mkModel(documents, path, progress):
    if isfile(path):
        model = Doc2Vec.load(path)
    else:
        model = mkTrainedModel(documents, progress)
        model.save(path, pickle_protocol=3)

    return model
