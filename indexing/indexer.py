# -------------------------------------------------------------------------
# FILENAME: indexer.py
# SPECIFICATION: Connect to the MongoDB called biology_department and use the tokens from the faculty collection
#                to create an inverted index collection where each token references which faculty documents it appears
#                on. For each document that the term appears on we also calculate the TF-IDF term weight and store it.
# FOR: CS 4250- Group Project
# -----------------------------------------------------------*/

# importing some Python libraries
from collections import defaultdict
from math import log
from database import db_connection


def calculate_tf_idf(term_frequency, total_terms_in_document, document_frequency, total_documents):
    # Calculate TF-IDF term weight

    tf = term_frequency/total_terms_in_document
    df = document_frequency
    N = total_documents

    idf = log(N / df, 10) if df > 0 else 0
    tf_idf = tf * idf

    return tf_idf


def create_index():
    # Creates a tf-idf inverted index

    db = db_connection.connectDataBase()
    faculty = db.faculty
    index = db.index

    # Total number of documents in the faculty collection
    total_documents = faculty.count_documents({})

    # Clear existing index collection to override with new one
    index.delete_many({})

    # Dictionary to store the document frequency for each unique term
    document_frequency_dict = defaultdict(int)

    # Gets the occurrence of token in the collection
    for professor in faculty.find():
        temp_tokens = professor.get('tokens', [])
        unique_terms_in_document = set(temp_tokens)  # Calculate the unique terms in each document for entire collection
        # Update document frequency for each unique term
        for term in unique_terms_in_document:
            document_frequency_dict[term] += 1

    # Iterate over each professor in the faculty collection
    for professor in faculty.find():
        document_id = professor['_id']
        tokens = professor.get('tokens', [])
        total_terms_in_document = len(tokens)  # Calculate the total number of terms in the document

        # Iterate over each token in the professor's tokens
        for token in tokens:
            if token:  # Skip empty tokens
                term_frequency = tokens.count(token)  # Keeps count of number of times term appears in document

                existing_entry = index.find_one({'_id': token})  # Check if the term already exists in the index collection

                if existing_entry:
                    # Check if the document entry already exists for the current document. If it does move on to next token
                    document_entry = next((doc for doc in existing_entry['documents'] if doc['document'] == document_id), None)

                    # Append a new document entry
                    if not document_entry:
                        existing_entry['documents'].append({'document': document_id, 'tf-idf': calculate_tf_idf(term_frequency, total_terms_in_document, document_frequency_dict[token], total_documents)})
                        index.update_one({'_id': token}, {'$set': {'documents': existing_entry['documents']}})  # Update existing entry with the new document and tf-idf value

                else:
                    # Create a new entry in the index collection with tf-idf value
                    tf_idf = calculate_tf_idf(term_frequency, total_terms_in_document, document_frequency_dict[token], total_documents)
                    new_entry = {'_id': token, 'documents': [{'document': document_id, 'tf-idf': tf_idf}]}
                    index.insert_one(new_entry)
