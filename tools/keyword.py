# Extracts keywords from the prompt that is then passed to the information sources to use as information. 

import spacy
import json

nlp = spacy.load("en_core_web_sm")

def extract_keywords(market: json = "selected_market.json"): 

    with open(market, "r", encoding = "utf-8") as f:
        selected_market = json.load(f)

    question = nlp(selected_market["question"])

    keywords = [token.lemma_ for token in question if token.pos_ in ['PROPN', 'NOUN', 'ADJ']]

    final = ""

    for key in keywords: 
        final += key + " " 

    print(final)



