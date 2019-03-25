import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from bs4 import BeautifulSoup
import gensim




def clean_text(data):
    if data != "NULL":
        data = data.lower()
        result = re.sub(r"[\.\,\(\)\:]","",data)
        result = nltk.word_tokenize(result)
        word = WordNetLemmatizer()
        result = [word.lemmatize(e) for e in result]
        filter_word = [word for word in result if word not in stopwords.words('english')]
        return filter_word
    return
all_useful_sentences = []
df = pd.read_csv("all_information.csv",index_col=0)
df["handbook_description"] = df["handbook_description"].fillna("NULL")
df["learning_outcome"] = df["learning_outcome"].fillna("NULL")

for e in df["handbook_description"]:
    if e == "NULL":
        continue
    else:
        text = BeautifulSoup(e, "html.parser").get_text()
        all_useful_sentences.append(clean_text(text))

for e in df["learning_outcome"]:
    if e == "NULL":
        continue
    else:
        all_useful_sentences.append(clean_text(e))

model = gensim.models.Word2Vec(all_useful_sentences, min_count=1)
model.save("mymodel")
print(model.most_similar("medicine"))