# -------------------------------------------------------------------------
# FILENAME: stemming.py
# SPECIFICATION: Uses lemmatizer to apply stemming to a list of tokens, returning the stemmed terms
# FOR: CS 4250- Group Project
# -----------------------------------------------------------*/

import nltk

def stem(tokens):
    lemma = nltk.wordnet.WordNetLemmatizer()
    terms = [lemma.lemmatize(token) for token in tokens]
    return terms