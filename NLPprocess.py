import json
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import gensim



def clean_text(data):
    if data != "NULL":
        data = data.lower()
        result = re.sub(r"[\.\,\(\)\:]"," ",data)
        result = nltk.word_tokenize(result)
        word = PorterStemmer()
        result = [word.stem(e) for e in result]
        filter_word = [word for word in result if word not in stopwords.words('english')]
        return filter_word
    return

def create_vector_file(filename):
    with open("cour_all.json","r") as f:
        all_info = json.loads(f.read())
    for e in range(len(all_info)):
        all_info[e] = clean_text(all_info[e])
    model = gensim.models.Word2Vec(sentences=all_info,size=200,min_count=1)
    model.save(filename)

def load_vector_file(filename):
    model = gensim.models.Word2Vec.load(filename)
    return model