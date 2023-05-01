from tqdm import tqdm
from spacy.lang.en.stop_words import STOP_WORDS
from spacy.lang.en import English
from sklearn.feature_extraction.text import TfidfVectorizer
import os
import json
import pandas as pd


data = []
for file in tqdm(os.listdir('./imdb/imdb_movie_jsons/2014/')):
    with open(f'./imdb/imdb_movie_jsons/2014/{file}', 'r') as data_2014:
        curr = json.load(data_2014)
    for review in curr['reviews']:

        # Load English tokenizer, tagger, parser, NER and word vectors
        nlp = English()

        #  "nlp" Object is used to create documents with linguistic annotations.
        my_doc = nlp(review['content'])

        # Create list of word tokens
        token_list = []
        for token in my_doc:
            token_list.append(token.text)

        # Create list of word tokens after removing stopwords
        filtered_sentence =[] 

        for word in token_list:
            lexeme = nlp.vocab[word]
            if lexeme.is_stop == False:
                filtered_sentence.append(word) 

        # print(filtered_sentence)

        data.append(filtered_sentence)


tfIdfVectorizer=TfidfVectorizer(use_idf=True)
tfIdf = tfIdfVectorizer.fit_transform(data)
df = pd.DataFrame(tfIdf[0].T.todense(), index=tfIdfVectorizer.get_feature_names_out(), columns=["TF-IDF"])
df = df.sort_values('TF-IDF', ascending=False)
print (df.head(25))

print(tfIdf.shape)
