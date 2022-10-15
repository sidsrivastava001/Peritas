from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

def similarity(doc1, corpus):
    vect = TfidfVectorizer(min_df=1, stop_words="english")                                                                                                                                                                                                   
    tfidf = vect.fit_transform(corpus)                                                                                                                                                                                                                 
    pairwise_similarity = tfidf * tfidf.T
    
    arr = pairwise_similarity.toarray()
    np.fill_diagonal(arr, np.nan)                                                                                                                                                                                                 
    input_idx = corpus.index(doc1)                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
    result_idx = np.nanargmax(arr[input_idx])
    return result_idx     

corpus= ["I'd like an apple", 
        "An apple a day keeps the doctor away", 
        "Never compare an apple to an orange", 
        "I prefer scikit-learn to Orange", 
        "The scikit-learn docs are Orange and Blue"]

print(similarity("The scikit-learn docs are Orange and Blue", corpus))