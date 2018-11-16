from lxml import html,etree
import re
import os

def parse(fn):
    tree = html.parse(fn)

    text = []
    for x in tree.getiterator():
    #print(x.tag,x.text)
        if x.tag not in ['script','style','img'] and type(x.tag) == str and type(x.text) == str:
            #print('in:',x.tag,x.text)
            text.append(x.text)
        else:
            pass
            #print('ignored:',x.tag,x.text)

    return ' '.join(text) # TODO: make it wokt without join

def import_bookeeping(fn):
    

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
