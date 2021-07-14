import nltk
# Uncomment to Download NLTK Packages
# nltk.download()
from nltk.stem import WordNetLemmatizer
import csv
import spacy
import requests
import json
import pyTigerGraph as tg

## TG STUFF INCOMING

conn = tg.TigerGraphConnection(host="https://a9cf2383f44d4944b4969837ae17f425.i.tgcloud.io/", username="tigergraph", password="Ap20062016", gsqlVersion="3.1.1", useCert=True)

# Reads Page 1 and stores its contents in a variable 
f = open('sample text.txt', 'r', encoding='utf-8')
content = f.read()
f.close()
content = content.replace("\n", " ")

## NLTK STUFF BELOW
# Initialize Lemmatizer (to combine similar words)
lemmatizer = WordNetLemmatizer()
# Set StopWords List
words = nltk.word_tokenize(content)
stopwords = nltk.corpus.stopwords.words('english')
## ^ Default NLTK Stopwords List
#file = open(INSERT_CUSTOM_STOPWORDS_FILENAME, "r", encoding="utf-8")

#text = file.read()
## ^ For Custom Stopword Lists
#words = [word for word in words if word.lower() not in stopwords]
# content = ' '.join(word for word in words)
# Initialize Spacy Engine
nlp = spacy.load("en_core_web_sm")
attributes = []
i = 0
num = 1
doc = nlp(content)

for ent in doc.ents:
    print(ent.text, ent.label_)
for chunk in doc.noun_chunks:
    if str(chunk.root.dep_)=="nsubj" and i==0:
        print(chunk.text + " is the main subject.")
        main_subject = chunk.root.text
        main_subject_query='''CREATE VERTEX ''' + chunk.root.text + '''(PRIMARY_ID ''' + chunk.root.dep_ + ''' STRING)'''
        print(conn.gsql(main_subject_query))
        i+=1
    if str(chunk.root.dep_) != "nsubj":
        attribute_query='''CREATE VERTEX ''' + chunk.root.text + '''(PRIMARY_ID ''' + chunk.root.dep_ + ''' STRING)'''
        edge_query='''CREATE UNDIRECTED EDGE association''' + str(num) + '''(FROM ''' + chunk.root.text + ''', TO ''' + main_subject +''')'''
        print(conn.gsql(attribute_query))
        print(conn.gsql(edge_query))
        attributes.append(chunk.root.text)
        num+=1
    print(chunk.text, "--", chunk.root.text, "is a", chunk.root.dep_, spacy.explain(chunk.root.dep_))
#sentences = nltk.sent_tokenize(content)
#for sentence in sentences:
#    words = nltk.word_tokenize(sentence)
#    #stemmed_words = [stemmer.stem(word) for word in words]
#    lemmatized_words = [lemmatizer.lemmatize(word) for word in words]
#    important_words = [lemmatized_word for lemmatized_word in lemmatized_words if lemmatized_word.lower() not in stopwords]
#    tagged = nltk.pos_tag(important_words)
#   
#   namedEnt = nltk.ne_chunk(tagged)
#   
#    namedEnt.draw()

graph_query = '''CREATE GRAPH ''' + main_subject + '''Graph(*)'''
print(conn.gsql(graph_query))
conn.apiToken = conn.getToken(conn.createSecret())