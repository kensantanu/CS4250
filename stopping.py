# -------------------------------------------------------------------------
# FILENAME: stopping.py
# SPECIFICATION: Remove stop words from tokens using predefined stopwords dataset from ntlk
# FOR: CS 4250- Group Project
# -----------------------------------------------------------*/

from nltk.corpus import stopwords
import nltk

# Download NLTK stopwords dataset
nltk.download('stopwords')
def remove_common_words(tokens):
    stop_words = set(stopwords.words('english'))
    terms = [term for term in tokens if term not in stop_words]
    return terms