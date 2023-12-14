# -------------------------------------------------------------------------
# FILENAME: transforming.py
# SPECIFICATION: Transform text data by tokenizing, stopping, and stemming,
# then storing the processed tokens under the field 'tokens' for each professor.
# FOR: CS 4250- Group Project
# -----------------------------------------------------------*/

from indexing.transforming import tokenizer
from indexing.transforming import stopping
from indexing.transforming import stemming
from database import db_connection

def transform():
    db = db_connection.connectDataBase()
    faculty = db.faculty
    professors = faculty.find()
    for professor in professors:
        text = professor.get('text', '')
        # Tokenize the text
        tokens = tokenizer.tokenize(text)

        # Apply stopping
        stopped_tokens = stopping.remove_common_words(tokens)

        # Apply stemming
        stemmed_tokens = stemming.stem(stopped_tokens)

        # Save the processed tokens back to the database with the name 'tokens'
        faculty.update_one(
            {'_id': professor['_id']},
            {'$set': {'tokens': stemmed_tokens}})