### Classy Shoes!

Learning semantical representations using a distributed representation of documents.


## Usage

    # Virtualenv with Python3
    pyvenv --system-site-packages .env
    . .env/bin/activate

    # Install dependencies into env
    pip install -r requirements.txt

    # Download NLTK data needed for language pre-processing
    python -m nltk.downloader snowball_data stopwords punkt

    # Fetch reviews and train model
    ./mkReviews.py

Note: no command line arguments imply querying the german Zalando API; see `./mkReviews.py --help`.

When done, we currently drop you into a interactive console with the trained model at hand.
The function `Q` canonicalizes your query by tokenizing, stemming and removing punctuation.

    >>> model.doesnt_match(Q('sneaker stiefel hemd'))
    hemd

    >>> model.most_similar(Q('stiefel kalt'), Q('warm'), topn=3)
    [('schuh', 0.4282079041004181), ('blazer', 0.4223514497280121), ('sneaker', 0.4199856221675873)]

    >>> model.similarity(Q('kleid'), Q('hemd'))
    0.8267573236460305

The same works on document vectors.

    >>> model.docvecs.similarity('M0822D06Q-K11', 'SE652K000-M11')
    0.33098285641485276


Note: do not take the results too seriously at this time. There is the need for experimentation and fine-tuning.


## What it does

We first fetch all article reviews from the Zalando API.
We then transparently cache reviews and their attributes locally in a SQLite3 database.
As soon as we saved the reviews locally, we train a distributed representation of documents model on reviews and their attributes, learning semantic meaning from their relationships.
Transparently caching the trained model allows us to skip this step in subsequent runs.


## References

- https://github.com/zalando/shop-api-documentation/wiki/Api-introduction
- https://github.com/zalando/shop-api-documentation/wiki/Article-reviews
- http://radimrehurek.com/gensim/models/doc2vec.html
- http://cs.stanford.edu/~quocle/paragraph_vector.pdf


## License

Copyright © 2016 Daniel J. Hofmann

Distributed under the MIT License (MIT).
