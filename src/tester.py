from code.text_processor import TextProcessor
from nltk import word_tokenize as tokenize
from nltk.corpus import stopwords
from code.bolean_model import BooleanModel, query_to_dnf
# stemming
from nltk.stem import PorterStemmer

def parse_cran_qrels():
    """
    Parsea el archivo de relevancia de consultas CRAN y devuelve un diccionario con las consultas como claves y
    una lista de documentos relevantes como valores.

    Returns:
        dict: Diccionario con las consultas como claves y una lista de documentos relevantes como valores.
    """
    qrels = {}
    with open("./data/cran/cranqrel", "r") as f:
        for line in f:
            line = line.split(" ")
            if line[0] not in qrels:
                qrels[line[0]] = []
            qrels[line[0]].append(int(line[1]))
    return qrels

def parse_cran_queries():
    """
    Parsea el archivo de consultas CRAN y devuelve una lista de diccionarios, donde cada diccionario representa una consulta
    con su ID y texto.

    Returns:
        list: Lista de diccionarios con las consultas.
    """
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

def metrics(model, rels, query):
    """
    Calcula las métricas de evaluación para una consulta dada utilizando un modelo de recuperación de información.

    Args:
        model (TextProcessor): Instancia del modelo de recuperación de información.
        rels (dict): Diccionario con las consultas como claves y una lista de documentos relevantes como valores.
        query (dict): Diccionario con el ID y el texto de la consulta.

    Returns:
        list: Lista con las métricas de evaluación: precisión, recall, F1 y fallout.
    """
    model.query_processor(query["text"])
    ranking = list(model.similarity())  
    metric = [] 

    # calculate the evaluation metrics
    RR = 0
    RI = 0

    for i in range(len(ranking)):    
        a = ranking[i]
        if model.docID[a] in rels[str(int(query["id"]))]:
            RR += 1
        else:
            RI += 1

    NR = len(rels[str(int(query["id"]))]) - RR
    NI = (len(model.docs) - len(rels[str(int(query["id"]))])) - RI  


    precision = RR / (RR + RI)
    recall = RR / (RR + NR)
    f1 = 2 * (precision * recall) / ((precision + recall) + 1e-8)
    fallout = RI / (RI + NI)

    metric.append(precision)
    metric.append(recall)
    metric.append(f1)
    metric.append(fallout)

    return metric

def testing_model():
    """
    Realiza pruebas en un modelo de recuperación de información utilizando un conjunto de consultas y sus correspondientes
    documentos relevantes. Calcula las métricas de evaluación para cada consulta y devuelve las métricas promedio.


    Returns:
        None
    """
    rels = parse_cran_qrels()
    queries = parse_cran_queries()
    model = TextProcessor()

    list = [0]*4

    print("Introduzca numero de query")
    queryNumber=int(input())
    metrics_query = metrics(model, rels, queries[queryNumber])

    print("Our model")
    print("Precision:" + str(metrics_query[0]))
    print("Recall : " + str(metrics_query[1]))
    print("F1 : " + str(metrics_query[2]))
    print("Fallout : " + str(metrics_query[3]))
    
    query=queries[queryNumber]
    booleanResults=BooleanModel(query_to_dnf(query['text']))
    ranking=[model.docID[x] for x in booleanResults]
        # calculate the evaluation metrics
    RR = 0
    RI = 0

    for i in range(len(ranking)):    
        a = ranking[i]
        if model.docID[a] in rels[str(int(query["id"]))]:
            RR += 1
        else:
            RI += 1

    NR = len(rels[str(int(query["id"]))]) - RR
    NI = (len(model.docs) - len(rels[str(int(query["id"]))])) - RI  


    precision = RR / (RR + RI + 1e-8)
    recall = RR / (RR + NR)
    f1 = 2 * (precision * recall) / ((precision + recall) + 1e-8)
    fallout = RI / (RI + NI)

    print("Boolean model")
    print("Precision:" + str(precision))
    print("Recall : " + str(recall))
    print("F1 : " + str(f1))
    print("Fallout : " + str(fallout))


if __name__ == "__main__":
    testing_model()