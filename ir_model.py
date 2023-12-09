import tokenizer
import stopping
import stemming
import db_connection

def search(userQuery):
    db = db_connection.connectDataBase()
    pass
    # tokenize userQuery
    # remove common words
    # stem tokens
    tokens = tokenizer.tokenize(userQuery)

        # Apply stopping
    stopped_tokens = stopping.remove_common_words(tokens)

        # Apply stemming
    stemmed_tokens = stemming.stem(stopped_tokens)

    # calculate query weights?

    # calculate document scores by multiplying query weights and tf-idf and adding them up?

    # return a list of faculty sorted by descending document scores