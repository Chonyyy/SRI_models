from code.parser import CranParser
# from code.document import Document
from code.model import Vector_Model

import re
from nltk import word_tokenize as tokenize
from nltk.corpus import stopwords
import string
# stemming
from nltk.stem import PorterStemmer
import os


def processing_text(raw_text: str, language: str) -> list[str]:
    """This method has the propose of processing the text
    Returns: a List of stemmed and normalized tokens
    """
    # raw_text = re.sub(r'[^\w\s]', '', raw_text)
    res = tokenize(raw_text, language)
    stop_list = stopwords.words(language) + [*string.punctuation]
    stemmer = PorterStemmer()
    return [stemmer.stem(token) for token in res if (token not in stop_list) and len(token) >= 3]

def testing_parser():
    parser = CranParser(processing_text) 
    print("hola")
    with open("data/cran/cran.all.1400","r") as doc:
        print(parser.parse(doc))
        
        
def testing_model():
    parser = CranParser(processing_text)
    model = Vector_Model(processing_text)
    documents = []
    query =  "what similarity laws must be obeyed when constructing aeroelastic models of heated high speed aircraft ."
    
    with open("data/cran/cran.all.1400","r") as doc:
        documents = parser.parse(doc)
        
    for doc in documents:
        model.add_document(doc)
                
    ranking = model.get_ranking(query,10,0)
    print(([( doc.doc_name, rank) for doc, rank in ranking ], len(ranking)))
        
if __name__ == "__main__":
    testing_model()
    
