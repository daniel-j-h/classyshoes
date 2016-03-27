#!/usr/bin/env python3

from os.path import isfile
from sys import exit
from logging import basicConfig

from classyshoes.db import mkEngine, mkStorage, mkScopedSession, Review
from classyshoes.api import mkKeepAliveSession, mkEndpoint, mkIterable
from classyshoes.args import mkArguments
from classyshoes.httpd import mkHttpd
from classyshoes.headers import mkBaseHeaders
from classyshoes.language import mkLanguage
from classyshoes.progress import mkProgress, mkNullProgress
from classyshoes.semantics import mkTrainedModel, mkExistingTrainedModel, mkLabeledReviews


def main():
    args = mkArguments('Learns review semantics based on article reviews')
    language = mkLanguage(args.locale)

    if args.verbose:
        basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

    engine = mkEngine(args.storage)

    if not isfile(args.storage):
        mkStorage(engine)
        mkDatabase(engine, args)

    if not isfile(args.model):
        model = mkSemanticModel(engine, args.model, language)
    else:
        model = mkExistingTrainedModel(args.model)

    httpd = mkHttpd(model, language)
    httpd.run(debug=True)


def mkDatabase(engine, args):
    headers = mkBaseHeaders(args.locale, 'gzip', args.whoami)
    progress = mkProgress('Page')

    with mkKeepAliveSession() as httpSession, mkScopedSession(engine) as sqlSession:
        endpoint = mkEndpoint(args.shopURL, 'article-reviews')
        fields = ('reviewId', 'articleId', 'title', 'description', 'rating', 'recommend', 'helpfulCount', 'unhelpfulCount')
        reviews = mkIterable(httpSession, endpoint, headers, fields, progress, args.timeout)

        for review in reviews:
            sqlReview = Review(reviewId=review['reviewId'], articleId=review['articleId'], title=review['title'],
                               description=review['description'], rating=review['rating'], recommend=review['recommend'],
                               helpfulCount=review['helpfulCount'], unhelpfulCount=review['unhelpfulCount'])
            sqlSession.add(sqlReview)


def mkSemanticModel(engine, path, language):
    progress = mkProgress('Epoch')

    with mkScopedSession(engine) as sqlSession:
        # Force generator; keep in memory as we have to walk over corpus multiple times
        reviews = list(mkLabeledReviews(sqlSession, language))
        model = mkTrainedModel(reviews, path, progress)

    return model


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit('\nBye')
