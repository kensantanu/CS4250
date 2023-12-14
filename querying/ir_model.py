from indexing.transforming import stopping, stemming, tokenizer
import db_connection
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

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
    
    # creates vector space by getting tf-idf for each doc
    rank = []
    for i in index:
        row = {}
        for doc in i["documents"]:
            row[doc["document"]] = doc["tf-idf"]
        rank.append(row)
    df = pd.DataFrame(rank)
    df = df.transpose()
    df = df.fillna(0)
    print("Vector Space:")
    print(df)

    dfIndex = pd.DataFrame([1] * len(index))

    # Calculate cosine similarity for each row with the target vector
    cosine_similarities = [cosine_similarity(df.loc[row].values.reshape(1, -1), dfIndex.values.reshape(1, -1))[0, 0] for row in df.index]

    # Create a DataFrame with cosine similarities
    result_df = pd.DataFrame({'Cosine_Similarity': cosine_similarities}, index=df.index)
    print(result_df)
    
    # rank = {}
    # for i in index:
    #     for doc in i["documents"]:
    #         if doc["document"] in rank:
    #             rank[doc["document"]] = rank[doc["document"]] + doc["tf-idf"]
    #         else:
    #             rank[doc["document"]] = doc["tf-idf"]

    # return a list of faculty sorted by descending document scores
    rankList= [{index: row.values[0]} for index, row in result_df.iterrows()]

    rankList = [[key, value] for d in sorted(rankList, key=lambda d: list(d.values())[0], reverse=True) for key, value in d.items()]
    # rankList = sorted(rankList, key=lambda x: list(x.values())[0], reverse=True)
    # rankList = [[key, value] for item in rankList for key, value in item.items()]
    webList = []
    for id, score in rankList:
        faculty = db.faculty.find({'_id': id})
        faculty = list(faculty)
        webList.append([faculty[0]["web"], score])
    return webList