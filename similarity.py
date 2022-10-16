from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

def similarity(doc1, corpus):
    c = corpus.values()
    print(c)
    vect = TfidfVectorizer(min_df=1, stop_words="english")                                                                                                                                                                                                   
    tfidf = vect.fit_transform(c)                                                                                                                                                                                                                 
    pairwise_similarity = tfidf * tfidf.T
    
    arr = pairwise_similarity.toarray()
    np.fill_diagonal(arr, 0)                                                                                                                                                                                                 
    input_idx = list(c).index(doc1)

    return arr[input_idx]


