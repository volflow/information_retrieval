from lxml import html,etree
from bs4 import BeautifulSoup
from bs4.element import Comment
import re
import os
import json

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def parse(fn):
    with open(fn) as f:
        soup = BeautifulSoup(f, features="lxml")

    title = soup.findAll("title")
    titles = []
    for i in title:
        titles.append(i.text)

    meta = soup.findAll("meta")
    metas = []
    for i in meta:
        if (i.get("name") in ["description", "keywords"]):
            metas.append(i.get("content"))

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
    id_to_url = import_id_to_url(bookeeping_fp)
    index = Index(id_to_url=id_to_url)

    print('Parsing Documents...')
    for doc_id in id_to_url:
        fp = './WEBPAGES_RAW/' + doc_id

        # map
        title,metadata,body = parse(fp)

        token_dict = {}
        for str_ in title:
            tokens = tokenize(str_,3)
            token_dict = insert_token_dict(tokens,type=0,dict_=token_dict)
        for str_ in metadata:
            tokens = tokenize(str_,3)
            token_dict = insert_token_dict(tokens,type=1,dict_=token_dict)
        for str_ in body:
            tokens = tokenize(str_,3)
            token_dict = insert_token_dict(tokens,type=2,dict_=token_dict)

        # reduce
        for token,token_freq in token_dict.iteritems():
            index.add(doc_id,token,token_freq)

        #print(doc_id,fp)

    print('Calculating Scores...')
    index.update_scores()

    print('done')
    return index


def tokenize(s, min_len):
    # find all alpha numerical tokens of len  >= min_len
    s = re.findall('[a-zA-Z0-9]{%d}[a-zA-Z0-9]*' % min_len, s)
    return map(lambda x: x.lower(), s)  # make all tokens lowercase

def insert_token_dict(tokens, dict_ = {}, type, count=True):
    """
    type: 0 title | 1 metadata | 2 body
    """
    for t in tokens:
        t.lower()
        dict_.setdefault(t, (0,0,0))
        if count:
            dict_[t][type] += 1
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

        results = []
        for token in tokens:
            if token in self.token_to_id_score:
                found = self.token_to_id_score[token]
                #scored = self.score(token,found)
            results += found
            break

        def add_urls(id_tuple):
            url = self.id_to_url[id_tuple[0]]
            return url, id_tuple

        results = map(add_urls,results)
        return results

    def score(self,token):
        postings_list = self.token_to_id_metadata[token]
        idf = len(self.token_to_id_metadata[token])/len(self.id_to_url) # df/total_documents

        def tf_idf(x):
            score = x[1] * idf
            return x[0], score#, x[1], idf#token,score

        scored_postings = list(map(tf_idf,postings_list))
        # sort scored_postings
        scored_postings.sort(key=lambda x: x[1], reverse=True)

        return scored_postings

    # def rank(self,id_tuple_lsit):
    #     'in-place ranking'
    #     id_tuple.sort(key=lambda x: x[1], reverse=True)
