import spacy
import json
import os
from nltk.corpus import stopwords
import pandas as pd
import gensim
import gensim.corpora as corpora
from tqdm import tqdm
import re
import contractions
from nltk.corpus import words

with open("./stopwords.json", "r") as f:
    common = json.load(f)
    common.extend(stopwords.words("english"))
    common = set(common)


eng_words = set(words.words())

def cleaner(text: str):
    
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
for movie_year in tqdm(tuple(os.walk("./MergedData/merged_movie_jsons"))[0][1]):
    subdir = tuple(os.walk(f"./MergedData/merged_movie_jsons/{movie_year}"))
    for file_name in tuple(subdir)[0][-1]:
        # print(f"{subdir[0][0]}/{file_name}")
        with open(f"{subdir[0][0]}/{file_name}", 'r', encoding="utf-8") as f:
            file = json.load(f)
        corpus = []
        my_pos = set(["ADJ"])
        content = [review["content"] for review in file["reviews"]]
        nlp = spacy.load("en_core_web_sm") #python -m spacy download en_core_web_lg
        for review in content:
            string = nlp(review)
            clean = []
            for word in string:
                if word.pos_ in my_pos:
                    clean.append(str(word.lemma_))
            corpus.append(" ".join(clean))
            
        proc_data = [cleaner(string.split()) for string in corpus]
        input_dict = corpora.Dictionary(proc_data)
        input_corpus = [input_dict.doc2bow(token, allow_update=True) for token in proc_data]

        model = gensim.models.TfidfModel(input_corpus, id2word=input_dict)
        vector = model[input_corpus]

        d = {}
        for v in vector:
            for id, f in v:
                d[input_dict[id]] = f
        
        file['vibes'] = [k for k,v in d.items() if v == 1]

        print(f"{file_name=}, {file['vibes']=}")
        
        with open(f"{subdir[0][0]}/{file_name}", 'w') as wr:
            json.dump(file, wr, indent=4)
