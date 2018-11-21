from flask import Flask, render_template, request
from lxml import html,etree
from bs4 import BeautifulSoup
from bs4.element import Comment
import re
import os
import json
import math
import pickle

bookeeping_fp = './WEBPAGES_RAW/bookkeeping.json'
corpus_fp = './WEBPAGES_RAW/'
index_fp = './index_dump'

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def parse(fn):
    with open(fn, encoding='utf-8', errors='ignore') as f:
        soup = BeautifulSoup(f, features="lxml")

    title = soup.findAll("title")
    titles = []
    for i in title:
        titles.append(i.text)

    meta = soup.findAll("meta")
    metas = []
    for i in meta:
        if (i.get("name") in ["description", "keywords"]):
            content = i.get("content")
            value = i.get("value")
            if content is not None:
                metas.append(content)
            if value is not None:
                metas.append(value)

    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    body_text = []
    for i in visible_texts:
        body_text.append(i)

    return (titles, metas, body_text) # TODO: make it wokt without join

def import_id_to_url(json_fp=bookeeping_fp):
    with open(json_fp) as f:
        id_to_url = json.load(f)

    return id_to_url

def build_index():
    min_token_len = 3
    id_to_url = import_id_to_url(bookeeping_fp)
    index = Index(id_to_url=id_to_url)

    print('Parsing Documents...')
    for doc_id in id_to_url:
        fp = corpus_fp + doc_id

        # map
        title,metadata,body = parse(fp)
        token_dict = {}
        for str_ in title:
            tokens = tokenize(str_,min_token_len)
            token_dict = insert_token_dict(tokens,type=0,dict_=token_dict)
        for str_ in metadata:
            tokens = tokenize(str_,min_token_len)
            token_dict = insert_token_dict(tokens,type=1,dict_=token_dict)
        for str_ in body:
            tokens = tokenize(str_,min_token_len)
            token_dict = insert_token_dict(tokens,type=2,dict_=token_dict)

        # reduce
        for token,token_freq in token_dict.items():
            index.add(doc_id,token,token_freq)

        print(doc_id,fp)

    print('Calculating Scores...')
    index.update_scores()

    print('done')
    return index


def tokenize(s, min_len):
    # find all alpha numerical tokens of len  >= min_len
    s = re.findall('[a-zA-Z0-9]{%d}[a-zA-Z0-9]*' % min_len, s)
    return map(lambda x: x.lower(), s)  # make all tokens lowercase

def insert_token_dict(tokens, type, dict_ = {}, count=True):
    if type is not None:
        """
        type: 0 title | 1 metadata | 2 body
        """
        for t in tokens:
            t.lower()
            dict_.setdefault(t, [0,0,0])
            if count:
                dict_[t][type] += 1
    else:
        for t in tokens:
            t.lower()
            dict_.setdefault(t, 0)
            if count:
                dict_[t] += 1
    return dict_


class Index(object):
    def __init__(self, token_to_id_metadata={}, id_to_url={}):
        self.id_to_url = id_to_url
        self.token_to_id_metadata = token_to_id_metadata
        self.token_to_id_score = {}

    def add(self,doc_id,token,token_freq):
        self.token_to_id_metadata.setdefault(token, [])
        self.token_to_id_metadata[token].append((doc_id,token_freq))

    def update_scores(self):
        self.token_to_id_score = {}
        for token in self.token_to_id_metadata:
            id_score = self.score(token)
            self.token_to_id_score[token] = id_score

    def search(self,query):
        tokens = tokenize(query,min_len=3)
        q_dict = insert_token_dict(tokens,type=None,count=True)

        results = {}
        for token in q_dict:
            # q_tf = 1+math.log(q_dict[token])
            # q_idf = len(self.token_to_id_score[token])/len(self.id_to_url) # df/total_documents
            # q_w = q_tf * q_idf
            if token in self.token_to_id_score:
                found = self.token_to_id_score[token]
                #scored = self.score(token,found)
                for id,score in found:
                    results.setdefault(id,[0,0])
                    results[id][0] += 1
                    results[id][1] += score

        result = sorted(results.items(), key = lambda x : x[1],reverse=True)

        def add_urls(id_tuple):
            url = self.id_to_url[id_tuple[0]]
            return url, id_tuple

        result = map(add_urls,result)
        return result

    def score(self,token,use_idf=True):
        postings_list = self.token_to_id_metadata[token]
        if use_idf:
            idf = math.log(len(self.id_to_url)/len(self.token_to_id_metadata[token]),10) # total_documents/df

        def tf_idf(x):
            # 2.5*title_freq+1.5*metadata_freq+1*body_freq
            tf = 1 + math.log((5*x[1][0]+3*x[1][1]+2*x[1][2])/2,10)
            if use_idf:
                score = tf * idf
            else:
                score = tf
            return x[0], score#, x[1], idf#token,score

        scored_postings = map(tf_idf,postings_list)
        # sort scored_postings
        scored_postings = sorted(scored_postings,key=lambda x: x[1], reverse=True)

        return scored_postings

    # def rank(self,id_tuple_lsit):
    #     'in-place ranking'
    #     id_tuple.sort(key=lambda x: x[1], reverse=True)
app = Flask(__name__)
index = ""
@app.route('/')
def hello_worldk():
    return render_template("google_but_better.html")

@app.route('/forward')
def forward():
    #get query
    queryName = "Hello"
    with open("history",'rb') as history_file:
        history_list = pickle.load(history_file)
        x = history_list[-1]
    print(x)
    links = (list(index.search(queryName)))
    return render_template("query_page.html", links=links)

@app.route('/query')
def hello_world():
    links = []
    queryName = request.args["queryEntryBox"]
    links = (list(index.search(queryName)))
    with open("history",'rb') as history_file:
        history_list = pickle.load(history_file)
    history_list.append(queryName)
    with open("history",'wb') as history_file:
        pickle.dump(history_list, history_file)
    return render_template("query_page.html", links=links)

if __name__ == '__main__':
    with open("index_dump", "rb") as f:
        index = pickle.load(f)
    with open("history",'wb') as history_file:
        history_list = []
        pickle.dump(history_list, history_file)
    app.debug = True
    app.run(host = '0.0.0.0',port=5000)
    #print('Building index')
    #index = build_index()
    #with open(index_fp,'wb') as handle:
        #pickle.dump(index,handle)
