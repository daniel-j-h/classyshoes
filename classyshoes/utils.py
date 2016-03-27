from classyshoes.language import mkStemmer, mkTokenizer, mkStopper
from classyshoes.semantics import mkCanonical


# Pre-process text to make it queryable; convinience helper
def mkQueryable(language):
    stemmer = mkStemmer(language)
    tokenizer = mkTokenizer(language)
    stopper = mkStopper(language)

    return lambda text: mkCanonical(text, stemmer, tokenizer, stopper)
