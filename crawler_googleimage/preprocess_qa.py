import nltk
import csv
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag
lm = WordNetLemmatizer()

data_dir = 'C:/Users/dilab/PycharmProjects/CQA/data/Rand/'
file_name = 'cqa_train.csv'

train_fi = []
with open(data_dir+file_name, 'r',encoding='CP949') as f:
    r = csv.reader(f)
    for line in r:
        train_fi.append(line)
del train_fi[0]


stop_words = set(stopwords.words('english'))
sent = []
for obj in train_fi:
    word_tokens = word_tokenize(obj[2].lower())
    result = []
    for w in word_tokens:
        if w not in stop_words:
            w=lm.lemmatize(w, pos="v")
            result.append(w)

    result = (' ').join(result)
    tagged_list = pos_tag(word_tokenize(result))
    for_search_words = [t[0] for t in tagged_list if t[1] == "NN" or t[1] == "VB" or t[1] == "VBP" or t[1] == "JJ" or t[1] == "NNS"]
    for_search_words = (' ').join(for_search_words)
    sent.append(for_search_words)
