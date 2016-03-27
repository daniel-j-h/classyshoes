### Classy Shoes!

Learning semantical representations using a Distributed Memory Model of Paragraph Vectors (PV-DM)


## Usage

    # Virtualenv with Python3
    pyvenv --system-site-packages .env
    . .env/bin/activate

    # Install dependencies into env
    pip install -r requirements.txt

    # Download NLTK data needed for language pre-processing
    python -m nltk.downloader snowball_data stopwords punkt

    # Fetch reviews, train model, start Httpd
    ./mkReviews.py

No command line arguments imply querying the german Zalando API; see `./mkReviews.py --help`.

Do not take the results too seriously at this time. There is the need for experimentation and fine-tuning.


## What it does

We first fetch all article reviews from the Zalando API.
We then transparently cache reviews and their attributes locally in a SQLite3 database.
As soon as we saved the reviews locally, we train a Distributed Memory Model of Paragraph Vectors (PV-DM) on reviews and their attributes, learning semantic meaning from their relationships.
Transparently caching the trained model allows us to skip this step in subsequent runs.


## References

- https://github.com/zalando/shop-api-documentation/wiki/Api-introduction
- https://github.com/zalando/shop-api-documentation/wiki/Article-reviews
- http://radimrehurek.com/gensim/models/doc2vec.html
- http://cs.stanford.edu/~quocle/paragraph_vector.pdf


## License

Copyright © 2016 Daniel J. Hofmann

Distributed under the MIT License (MIT).
