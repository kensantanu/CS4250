# -------------------------------------------------------------------------
# FILENAME: tokenizer.py
# SPECIFICATION: Removes special characters, splits the document into terms and
# converts them to lowercase.
# FOR: CS 4250- Group Project
# -----------------------------------------------------------*/

from sklearn.feature_extraction.text import CountVectorizer

def tokenize(document):
    vectorizer = CountVectorizer(
        lowercase=True,
        token_pattern=r'\b\w+\b',  # Use a regex pattern to extract words & remove punctuation
        strip_accents='unicode',
    )

    # Fit and transform the document
    vector = vectorizer.fit_transform([document])

    # Get the feature names (terms)
    terms = vectorizer.get_feature_names_out()

    return terms