from lxml import html,etree
from bs4 import BeautifulSoup
from bs4.element import Comment
import re
import os

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

def tokenize(s, min_len):
    # find all alpha numerical tokens of len  >= min_len
    s = re.findall('[a-zA-Z0-9]{%d}[a-zA-Z0-9]*' % min_len, s)
    return map(lambda x: x.lower(), s)  # make all tokens lowercase

def insert_token_dict(tokens, dict_ = {}, count=True):
    for t in tokens:
        t.lower()
        dict_.setdefault(t, 0)
        if count:
            dict_[t] += 1
    return dict_


class Index(object):
    def __init__(self, dict_={}):
        self.dict_ = dict_

    def add(self,doc_id,token,token_freq):

        self.dict_.setdefault(token, [])

        self.dict_[token].append((doc_id,token_freq))

    def search(self,query):
        tokens = tokenize(query,min_len=3)

        results = []
        for token in tokens:
            if token in self.dict_:
                found = self.dict_[token]
                found.sort(key=lambda x: x[1], reverse=True)
            results += found

        return results
