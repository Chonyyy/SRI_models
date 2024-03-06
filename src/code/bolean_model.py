import sympy
import ir_datasets
import gensim

def query_to_dnf(query):
    '''
    This function is used to convert a boolean query to a disjunctive normal form (DNF)

    Args:
      - query: string, the boolean query

    Returns:
      - string, the boolean query in DNF
    '''
    input()
    operators = ['&', '|', '~','(',')']
    reserved_Words = query.split()
     
    #add spaces between the brackets 
    query = query.replace('(', ' ( ').replace(')', ' ) ') 
     
    processed_query = query.replace(" not ", " ~ ").replace(" and ", " & ").replace(" or ", " | ") 
    tokenized = processed_query.split()
    tokenized = [token for token in tokenized if token not in reserved_Words]
    

    #stay with alphanumeric characters 
    tokenized = [word for word in tokenized if word.isdigit() is False or word in operators] 
     
    for i in range(len(tokenized) -1): 
        if tokenized[i] not in operators and (tokenized[i+1] not in operators or tokenized[i+1] == '~'): 
            tokenized[i] = tokenized[i] + ' &' 
     
    processed_query = ' '.join(tokenized) 
     
    if processed_query == "":
       return "error"
    
    query_expr = sympy.sympify(processed_query, evaluate=False) 
    query_dnf = sympy.to_dnf(processed_query, simplify=True, force = True) 
    
    return query_dnf 


def BooleanModel(query):
    '''
    This function is used to search for documents that satisfy a boolean query

    Args:
      - query: string, the boolean query

    Returns:
      - list of integers, the indices of the documents that satisfy the query
    '''
 
    query_dnf = query_to_dnf(query)
    if query_dnf == "error":
       return []
    forms = query_dnf.args 
    Query = str(query_dnf) 
    terms = Query.split(' | ') 
 
    matching_documents = [] 
    
    documents=ir_datasets.load("cranfield")
    documents=[doc.text for doc in documents.docs_iter()]
    dictionary=gensim.corpora.Dictionary()

    for k, doc in enumerate(documents): 
      for clause in terms: 
        if clause[0] == '(': 
          clause = clause[1:-1] 
        clause_matched = True 
        needed = clause.split(' & ') 
        for i in needed: 
            neg = False 
            i = str(i) 
            if i[0] == '~': 
                neg = True 
                i = i[1:] 
            token_id = dictionary.token2id.get(i, -1) 
 
            if token_id in [j[0] for j in dictionary.doc2bow(doc)] and not neg: 
              pass
            elif token_id not in [j[0] for j in dictionary.doc2bow(doc)] and neg: 
              pass
            else: 
              clause_matched = False 
              break 
        if clause_matched is True: 
          matching_documents.append(k) 
          break
    return matching_documents