import spacy
import json
import os
from nltk.corpus import stopwords
import pandas as pd
import gensim
import gensim.corpora as corpora

files = []
# print( tuple(os.walk("./MergedData/merged_movie_jsons"))[2])
for movie_year in tuple(os.walk("./MergedData/merged_movie_jsons"))[0][1]:
    subdir = tuple(os.walk(f"./MergedData/merged_movie_jsons/{movie_year}"))
    for file_name in tuple(subdir)[0][-1]:
        # print(f"{subdir[0][0]}/{file_name}")
        with open(f"{subdir[0][0]}/{file_name}", 'r', encoding="utf-8") as f:
            files.append(json.load(f))



# nlp.max_length = 50_000_000
for i, file in enumerate(files):
    corpus = []
    my_pos = set(["ADJ"])
    content = [review["content"] for review in file["reviews"]]
    nlp = spacy.load("en_core_web_lg")
    for review in content:
        string = nlp(review)
        clean = []
        for word in string:
            if word.pos_ in my_pos:
                clean.append(str(word.lemma_))
        corpus.append(" ".join(clean))
        
    proc_data = [string.split() for string in corpus]
    input_dict = corpora.Dictionary(proc_data)
    input_corpus = [input_dict.doc2bow(token, allow_update=True) for token in proc_data]

    model = gensim.models.TfidfModel(input_corpus, id2word=input_dict)
    vector = model[input_corpus]

    d = {}
    for v in vector:
        for id, f in v:
            d[input_dict[id]] = f

    with open("stopwords_list.txt", 'a') as f:
        f.write(" ".join(d.keys()) + "\n")
    print(i)