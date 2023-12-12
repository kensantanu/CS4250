import tokenizer
import stopping
import stemming
import db_connection
from bson.json_util import dumps, loads 

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

    # grab index from db
    index = db.index.find({'_id': { '$in': stemmed_tokens}})
    index = list(index)
    
    # calculate document scores by geting tf-idf for each doc and adding them up
    rank = {}
    for i in index:
        for doc in i["documents"]:
            if doc["document"] in rank:
                rank[doc["document"]] = rank[doc["document"]] + doc["tf-idf"]
            else:
                rank[doc["document"]] = doc["tf-idf"]

    # return a list of faculty sorted by descending document scores
    rankList = sorted(rank.items(), key=lambda x:x[1], reverse=True)
    webList = []
    for id, tfidf in rankList:
        faculty = db.faculty.find({'_id': id})
        faculty = list(faculty)
        webList.append(faculty[0]["web"])
    return webList