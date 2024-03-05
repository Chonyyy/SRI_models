from code.text_processor import TextProcessor
from nltk import word_tokenize as tokenize
from nltk.corpus import stopwords
import string
# stemming
from nltk.stem import PorterStemmer

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
    model = TextProcessor()
    rels = parse_cran_qrels()
    queries = parse_cran_queries()
    query = queries[0]
    # query =  "what similarity laws must be obeyed when constructing aeroelastic models of heated high speed aircraft ."
    
    model.query_processor(query["text"])
    ranking=list(model.similarity())           

    #calculate the evaluation metrics
    RR = 0
    RI = 0
    
    for i in range(len(ranking)):    
        a = ranking[i]
        if model.docID[a] in rels[str(int(query["id"]))]:
            RR += 1
        else:
            RI += 1
        
    NR =  len(rels[str(int(query["id"]))]) - RR
    NI = (len(model.docs)-len(rels[str(int(query["id"]))])) - RI  

    precision = RR/ (RR + RI)
    recall = RR / (RR + NR)
    f1 = 2 * (precision * recall) / (precision + recall)
    fallout = RI / (RI + NI)
    
    print("\nPrecision Vector: " + str(precision) )
    print("Recall Vector: " + str(recall) )
    print("F1 Vector: " + str(f1) )
    print(f"Fallout Vector: {fallout}")
     
    
if __name__ == "__main__":
    testing_model()