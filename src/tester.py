from code.model import Vector_Model
from code.parser import CranParser
# from code.document import Document

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
        
def parse_cran_qrels():
    qrels = {}
    with open("./data/cran/cranqrel", "r") as f:
        for line in f:
            line = line.split(" ")
            if line[0] not in qrels:
                qrels[line[0]] = []
            qrels[line[0]].append(int(line[1]))
    return qrels

def parse_cran_queries():
    queries = []
    with open("./data/cran/cran.qry", "r") as f:
        for line in f:
            if line.startswith(".I"):
                query = {}
                query["id"] = line.split(" ")[1].strip("\n")
            elif line.startswith(".W"):
                query["text"] = ""
            else:
                query["text"] += line
            if line.startswith(".I"):
                queries.append(query)
    return queries

        
def testing_model():
    parser = CranParser(processing_text)
    model = Vector_Model(processing_text)
    rels = parse_cran_qrels()
    queries = parse_cran_queries()
    query = queries[0]
    documents = []
    # query =  "what similarity laws must be obeyed when constructing aeroelastic models of heated high speed aircraft ."
    
    with open("data/cran/cran.all.1400","r") as doc:
        documents = parser.parse(doc)
        
    for doc in documents:
        model.add_document(doc)
                
    ranking = model.get_ranking(query["text"],10,0)
    # print(ranking[0][0])
    print(([( doc.doc_name, rank) for doc, rank in ranking ], len(ranking)))
    
    #calculate the evaluation metrics
    #precision
    precision_vector = 0
    RR_vector = 0
    RI_vector = 0
    
    #for i in range(len(query_results_vector)):
    for i in range(10):
        if ranking[i][1] == 0:
            continue
        # print(rels[str(int(query["id"]))])
        a = ranking[i][0]
        if a.get_doc_id() in rels[str(int(query["id"]))]:
            RR_vector += 1
        RI_vector += 1
    
    #recall
    recall_vector = 0
    recall_vector = RR_vector / len(rels[str(int(query["id"]))])

    #F1
    f1_vector = 2 * (precision_vector * recall_vector) / (precision_vector + recall_vector)

      
    print("Precision Vector: " + str(precision_vector) )
    print("\nRecall Vector: " + str(recall_vector) )
    print("\nF1 Vector: " + str(f1_vector) )
     
    
if __name__ == "__main__":
    testing_model()
    

