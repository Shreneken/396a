from tqdm import tqdm
import spacy
import json
import os
from nltk.corpus import stopwords, words
import pandas as pd
import gensim
import gensim.corpora as corpora
import re
import contractions
import string

with open("./stopwords.json", "r") as f:
    common = json.load(f)
    common.extend(stopwords.words("english"))
    common = set(common)


eng_words = set(words.words())

def clean(text: str):
    
    # remove numbers
    text = re.sub(r"\d+", "", text)
    # expand contraction
    text = contractions.fix(text)
    # remove links
    text = re.sub(r"(ftp|http[s]?)://\S+", "", text)
    # remove punctuations
    sub_txt = r"[" + re.escape(string.punctuation) + r"]"
    text = re.sub(sub_txt, "", text)

    text = re.sub("[^a-zA-Z0-9 ]+", " ", text)

    # remove emails
    text = re.sub("[\w\.-]+@[\w\.-]+\.\w+", " ", text)
    
    text = " ".join([word for word in text.split() if word not in common and word in eng_words and len(word) > 2])

     # remove multispaces
    text = re.sub('\s+', " ", text)

    # lemmatizer.lemmatize()
    return text.strip()


# print( tuple(os.walk("./MergedData/merged_movie_jsons"))[2])
cnt = 0
for movie_year in tqdm(tuple(os.walk("./MergedData/merged_movie_jsons"))[0][1]):
    subdir = tuple(os.walk(f"./MergedData/merged_movie_jsons/{movie_year}"))
    for file_name in tuple(subdir)[0][-1]:
        # print(f"{subdir[0][0]}/{file_name}")
        with open(f"{subdir[0][0]}/{file_name}", 'r', encoding="utf-8") as f:
            file = json.load(f)
        corpus = []
        my_pos = set(["ADJ"])
        nlp = spacy.load("en_core_web_lg") #python -m spacy download en_core_web_lg
        content = [review["content"] for review in file["reviews"]]
        content.extend([review.get("review_title") for review in file["reviews"] if review.get("review_title") != None])
        if file["summary"] != "N/A" and file["summary"] != None:
            content.append(file["summary"])
        
        if file.get("rt_summary") != "N/A" and file.get("rt_summary") != None:
            content.append(file["rt_summary"])
        
        if file.get("meta_summary") != "N/A" and file.get("meta_summary") != None:
            content.append(file["meta_summary"])
        
        for review in content:
            s = nlp(review)
            tidy = []
            for word in s:
                if word.pos_ in my_pos:
                    tidy.append(str(word.lemma_))
            corpus.append(" ".join(tidy))
            
        proc_data = [clean(movie_revs).split() for movie_revs in corpus]
        input_dict = corpora.Dictionary(proc_data)
        input_corpus = [input_dict.doc2bow(token, allow_update=True) for token in proc_data]

        model = gensim.models.TfidfModel(input_corpus, id2word=input_dict,  normalize=True, dictionary=input_dict, slope=2.5, smartirs="Lfc")
        vector = model[input_corpus]

        d = {}
        for v in vector:
            for id, f in v:
                d[input_dict[id]] = f
        
        df = pd.DataFrame(d.values(), index=d.keys(), columns=["TF-IDF"])
        med = df["TF-IDF"].median()
        mean = df["TF-IDF"].mean()
        print(mean - med)
        d = {k: v for k, v in sorted(d.items(), key=lambda item: item[1], reverse=True)}
        file['vibes'] = [k for k,v in d.items() if abs(med - v) <= 0]
        with open(f"{subdir[0][0]}/{file_name}", 'w', encoding="utf-8") as wr:
            json.dump(file, wr, indent=4)
        cnt += 1; print(f"\r{cnt}/1205 :: {file['vibes']}", end="")