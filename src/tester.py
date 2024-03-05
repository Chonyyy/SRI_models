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

def metrics(model,rels,query):
    model.query_processor(query["text"])
    ranking=list(model.similarity())  
    metric = [] 
             
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
    f1 = 2 * (precision * recall) / ((precision + recall)+ 1e-8)
    fallout = RI / (RI + NI)
    
    metric.append(precision)
    metric.append(recall)
    metric.append(f1)
    metric.append(fallout)
    
    print("\nPrecision : " + str(precision) )
    print("Recall : " + str(recall) )
    print("F1 : " + str(f1) )
    print(f"Fallout : {fallout}")

    return metric

        
def testing_model():
    rels = parse_cran_qrels()
    queries = parse_cran_queries()
    model = TextProcessor()

    list = [0]*4
    
    # for i in range(len(queries)):
    for i in range(10):
        metrics_query = metrics(model,rels,queries[i])
        list[0]+=metrics_query[0]
        list[1]+=metrics_query[1]
        list[2]+=metrics_query[2]
        list[3]+=metrics_query[3]
    
    list[0] = list[0]/10
    list[1] = list[1]/10
    list[2] = list[2]/10
    list[3] = list[3]/10

    print("MEAN")
    print("Precision:" + str(list[0]))
    print("Recall : " + str(list[1] ))
    print("F1 : " + str(list[2] ))
    print("Fallout : " + str(list[3]))
     
    
if __name__ == "__main__":
    testing_model()