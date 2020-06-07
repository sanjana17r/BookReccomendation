import numpy as np # linear algebra
import pandas as pd
import os
import operator

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

books = pd.read_csv(r'C:\sanju\nptel\booksRec\templates\all.csv', encoding = "utf-8-sig")


titles = books

indices = pd.Series(books.index, index=books['name.1'])

totgenre = (books['genre1'].dropna()).append(books['genre2'].dropna()).reset_index(drop=True)
#indicegenre = pd.Series(books.index, index=totgenre))
#print(indicegenre)


#this efature involves words..,using 1 and 2 n_grams,...min threshold value of the vector will be 0: ignore terms that appear in less than 0% documents, stop words: unnceccary words to be removed
tf = TfidfVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0, stop_words='english')
tfidf_matrix = tf.fit_transform(books['author'])
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
#print(cosine_sim)



def authors_recommendations(title):
    idx = indices[title]#index of that title
    sim_scores = list(enumerate(cosine_sim[idx]))#cosine_sim has each index mapped to all other index. so what weve
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:21]
    book_indices = [i[0] for i in sim_scores]
    book_indices = [i[0] for i in sim_scores]
    titles = books
    titles=titles.iloc[book_indices]
    titles.sort_values(['no of ratings','rating'], ascending=[False,False],inplace=True)
    titlesn=titles['name.1']
    imgn=titles['image-src']
    bookn=titles['booklink-href']
    auth=titles['author']
    return (titlesn[:20],imgn[:20],bookn[:20],auth[:20])
    

books['corpus'] = (pd.Series(books[['genre1','genre2','genre3','genre4','genre5','genre6']]
                .fillna('')
                .values.tolist()
                ).str.join(' '))

tf_corpus = TfidfVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0, stop_words='english')
tfidf_matrix_corpus = tf_corpus.fit_transform(books['corpus'])
cosine_sim_corpus = linear_kernel(tfidf_matrix_corpus, tfidf_matrix_corpus)

##########################################################

def corpus_recommendations(title):
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim_corpus[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores=sim_scores[1:21]
    book_indices = [i[0] for i in sim_scores]
    titles = books
    titles=titles.iloc[book_indices]
    titles.sort_values(['no of ratings','rating'], ascending=[False,False],inplace=True)
    titlesn=titles['name.1']
    imgn=titles['image-src']
    bookn=titles['booklink-href']
    auth=titles['author']
    return (titlesn[:20],imgn[:20],bookn[:20],auth[:20])

def genre_based(g):
    k=books.loc[books['genre1']==g, 'name.1']
    l=books.loc[books['genre1']==g, 'image-src']
    m=books.loc[books['genre1']==g, 'booklink-href']
    n=books.loc[books['genre1']==g,'author']
    return (k,m,l,n)

totgenre = (books['genre1'].dropna()).reset_index(drop=True)
totgenre=list(set(totgenre))
