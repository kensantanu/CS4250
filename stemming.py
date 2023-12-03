# -------------------------------------------------------------------------
# FILENAME: stemming.py
# SPECIFICATION: Apply stemming to a list of tokens, returning the stemmed terms
# FOR: CS 4250- Group Project
# -----------------------------------------------------------*/

import nltk
from nltk.stem.snowball import SnowballStemmer

def stem(tokens):
    # Using lemmatizer
    lemma = nltk.wordnet.WordNetLemmatizer()
    terms = [lemma.lemmatize(token) for token in tokens]

    # Using stemmer
    # snowball = SnowballStemmer(language="english")
    # terms = [snowball.stem(token) for token in tokens]
    return terms
