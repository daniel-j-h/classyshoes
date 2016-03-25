from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer


# Language dependant stemmer, stems on a word basis
def mkStemmer(language):
    stemmer = SnowballStemmer(language)
    return lambda word: stemmer.stem(word)


# Language dependant tokenizer, tokenizes on a text basis
def mkTokenizer(language):
    return lambda text: word_tokenize(text, language=language)


# Language dependant stopper, access to stop words
def mkStopper(language):
    return lambda word: word in set(stopwords.words(language))


# Language name needed for the NLTK datasets based on locale
def mkLanguage(code):
    return {'de-DE': 'german'
          , 'de-AT': 'german'
          , 'de-CH': 'german'
          , 'en-GB': 'english'
          , 'es-ES': 'spanish'
          , 'fi-FI': 'finnish'
          , 'fr-CH': 'french'
          , 'fr-FR': 'french'
          , 'it-IT': 'italian'
          , 'nl-BE': 'dutch'
          , 'nl-NL': 'dutch'
          , 'no-NO': 'norwegian'
          , 'sv-SE': 'swedish'}[code]
