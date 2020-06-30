#!/usr/bin/env python
# coding: utf-8

# In[18]:


# set up libraries
import requests
import json
from datetime import datetime
from collections import Counter
import os
from pathlib import Path
import argparse
# external libraries
# check if additional installation needed
import plotly.graph_objects as go
import ipywidgets as widgets
from ipywidgets import interact, interact_manual


# In[2]:


# setup global
url = "http://nlp.ailab.lv/api/nlp"
headers = {'content-type': 'application/json'}

def tstamp():
    return datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")


def time_decor(fun):
    def wrap(*args, **kwargs):
        print(f"Before: {fun.__name__} - {tstamp()}")
        res = fun(*args, **kwargs)
        print(f"After: {fun.__name__} - {tstamp()}")
        return res
    return wrap

@time_decor
def getNLP(url = "http://nlp.ailab.lv/api/nlp", data =            { "data" : { "text":"change me"},            "steps":  ["tokenizer", "morpho", "parser", "ner"],            "model": "default",            "config": None},           headers = {'content-type': 'application/json'}):
    """Give a Python object and returns a Python object decoded from JSON"""
#     print(json.dumps(data))
    response = requests.post(url, json.dumps(data), headers=headers)
    if (response.status_code != 200):        
        print(f"Bad response code: {response.status_code}")
        return None
    return response.json()

def getData(text, offset=0,limit=None, steps=["tokenizer", "morpho", "parser", "ner"]):
    if limit:
        txt = text[offset:offset+limit]
    else:
        txt = text[offset:]
    return { "data" : { "text":txt},            "steps":  steps,            "model": "default",            "config": None}

def processChunks(chunks):
    return [getNLP(data=getData(chunk)) for chunk in chunks]

def splitText(text, maxLen=10_000, delim="."):
    chunks = []
    beg = 0
    while beg < len(text):
        end = text[beg:beg+maxLen].rfind(delim) 
        if end <= 0: # -1 if nothing found
            end = maxLen
        chunk = text[beg:beg+end+1]
        beg += end + 1
        chunks.append(chunk)
        print("Beg:", beg, len(text))
    return chunks
        
        

def getPunList(nlobj):
    upos_list = []
    for sentence in nlobj['data']['sentences']:
        for token in sentence['tokens']:
#             print(token['form'], token['lemma'], token['upos'])
            upos_list.append(token.get('upos'))
    return upos_list


# In[8]:


def getChunks(fpath):
    with open(fpath, encoding="utf-8") as f:
        txt = f.read()
    return splitText(txt)


# In[11]:


def processFolder(folder):
    files = os.listdir(folder)
    print(files)


# In[35]:


def processFile(file, inpath, outpath="json"):
    chunks = getChunks(os.path.join(inpath,file))
    jlist = processChunks(chunks)
    outfile = os.path.join(outpath, Path(file).with_suffix(".json"))
    with open(outfile, encoding="utf-8", mode="w") as f:
        json.dump(jlist,f, indent=2, ensure_ascii=False)


# In[ ]:

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Read DOM Files From URL')
    parser.add_argument('-d', '--dir', default='todo',
                        type=str, help="Folder to process all txt files throuh ailab into json")
    args = parser.parse_args()
    if args.d:
        processFolder(args.d)




