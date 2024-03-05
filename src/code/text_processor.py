import ir_datasets
import nltk
import gensim
from code.query import Query
import numpy as np
import math
import json

class TextProcessor:
    def __init__(self):
        self.dictionary = {}
        self.corpus = []
        dataset = ir_datasets.load("cranfield")
        self.docs = [doc.text for doc in dataset.docs_iter()]
        del self.docs[470]
        del self.docs[993]
        self.tokenized_docs = self.filter_tokens_by_occurrence(self.morphological_reduction_nltk(self.remove_stopwords(self.remove_noise_nltk(self.tokenization_nltk()))))
        self.vocabulary = list(self.dictionary.token2id.keys())
        self.vector_repr = self.vector_representation(self.tokenized_docs, self.dictionary)
        self.vector_repr = self.generalize(self.vector_repr)

    def tokenization_nltk(self):
        #Tokenize the query using NLTK
        a=dict()
        try:
            with open('data/feedback.json', 'x') as json_file:
                json.dump({}, json_file)
            return [nltk.tokenize.word_tokenize(doc) for doc in self.docs]
        except FileExistsError:
            with open("data/feedback.json",'r') as data:
                a=json.load(data)
        docs=[d+a[d] if d in a.keys() else d for d in self.docs]
        tokenized = [nltk.tokenize.word_tokenize(doc) for doc in docs]
        return tokenized
    
    def remove_noise_nltk(self, tokenized_docs):
        return  [[word.lower() for word in doc if word.isalpha()] for doc in tokenized_docs]
    
    def remove_stopwords(self, tokenized_docs):
        stop_words = set(nltk.corpus.stopwords.words('english'))
        return [
            [word for word in doc if word not in stop_words] for doc in tokenized_docs
        ]
    
    def morphological_reduction_nltk(self, tokenized_docs, use_lemmatization=True):
        if use_lemmatization:
            lemmatizer = nltk.stem.WordNetLemmatizer()
            tokenized_docs = [
                [lemmatizer.lemmatize(word) for word in doc]
                for doc in tokenized_docs
            ]
        else:
            stemmer = nltk.stem.PorterStemmer()
            tokenized_docs = [
                [stemmer.stem(word) for word in doc] for doc in tokenized_docs
            ]

        return tokenized_docs

    def filter_tokens_by_occurrence(self, tokenized_docs, no_below=5, no_above=0.5):
        if not self.dictionary:
            self.dictionary = gensim.corpora.Dictionary(tokenized_docs)
            self.dictionary.filter_extremes(no_below=no_below, no_above=no_above)
        filtered_words = [word for _, word in self.dictionary.iteritems()]
        return [
            [word for word in doc if word in filtered_words]
            for doc in tokenized_docs
        ]
    
    def vector_representation(self, tokenized_docs, dictionary, use_bow=True):
        if not self.corpus:
            self.corpus = [dictionary.doc2bow(doc) for doc in tokenized_docs]

        if use_bow:
            vector_repr = self.corpus
        else:
            tfidf = gensim.models.TfidfModel(self.corpus)
            vector_repr = [tfidf[doc] for doc in self.corpus]

        return vector_repr
    
    def generate_independets_vectors(self):
        # Genera un vector inicial con 1 en la primera posición y 0 en el resto
        vector_inicial = [1] + [0] * (len(self.vector_repr) - 1)
        
        # Genera la lista de vectores rotando el 1 a través de ellos
        lista_de_vectores = [vector_inicial[-i:] + vector_inicial[:-i] for i in range(len(self.vector_repr))]
        
        return np.array(lista_de_vectores)
    
    def generalize(self, vectors_weight, query=False):
        c = [[0] * len(self.vector_repr) for _ in range(len(self.vocabulary))]

        vectors = self.generate_independets_vectors()

        for i, k in zip(self.vector_repr, range(len(self.vector_repr))):
            for j in i:
                c[j[0]][k] += j[1]

        k_i = []
        k = 0
        for i in c:
            c_big = 0
            for j,v in zip(i,vectors):
                k = k + j * v
                c_big += j ** 2
            k_i.append((k/math.sqrt(c_big)).tolist())
            k = 0
            c_big = 0

        new_vectors = []
        
        if query:
            for vector in (vectors_weight):
                new_weight = 0
                for token in k_i[vector[0]]:  
                    new_weight += vector[1] * token          
                new_vectors.append((vector[0], new_weight))
            
        else:    
            for doc in range(len(vectors_weight)):
                new_tuple = []
                for vector in vectors_weight[doc]:
                    new_tuple.append((vector[0], k_i[vector[0]][doc] * vector[1]))
                new_vectors.append(new_tuple)
        
        return new_vectors


    def query_processor(self, query, use_bow=True):
        self.current_query=query
        self.save(query)
        self.query_processed = Query(query)
        self.query_processed.process_query()

        filterd_words = [word for _, word in self.dictionary.iteritems()]
        self.query_processed.tokenized_query = [word for word in self.query_processed.tokenized_query if word in filterd_words]

        self.query_processed.query_bow = self.dictionary.doc2bow(self.query_processed.tokenized_query)

        if use_bow:
            self.query_processed.vector_repr = self.query_processed.query_bow
        else:
            tfidf = gensim.models.TfidfModel(self.corpus)
            self.query_processed.vector_repr = tfidf[self.query_processed.query_bow]

        self.query_processed.vector_repr = self.generalize(self.query_processed.vector_repr, query=True)

    def similarity(self):
        #Find matched documents based on the query
        index = gensim.similarities.MatrixSimilarity(self.vector_repr)
                
        similarities = index[self.query_processed.vector_repr]
        top_matches = sorted(enumerate(similarities), key=lambda x: -(x[1]))
        best_match_indices = [match[0] for match in top_matches if match[1]<1e-8]
        return map(lambda x: self.docs[x],best_match_indices)
    
    def feedback(self,document):
        a=dict()
        try:
            with open('data/feedback.json', 'x') as json_file:
                json.dump({document:self.current_query}, json_file)
            return
        except FileExistsError:
            with open("data/feedback.json",'r') as data:
                a=json.load(data)
        if document in a:
            a[document]+='\n'+self.current_query
        else:
            a[document]=self.current_query
        with open('data/feedback.json','w') as data:
            json.dump(a,data)
    
    def save(self,query):
        a=''
        try:
            with open('data/recomendation.json', 'x') as json_file:
                json.dump(query, json_file)
            return
        except FileExistsError:
            with open("data/recomendation.json",'r') as data:
                a=json.load(data)
        a+=' '+query
        with open('data/recomendation.json','w') as data:
            json.dump(a,data)
    
    def recomend(self):
        a=''
        try:
            with open('data/recomendation.json', 'x') as json_file:
                json.dump("", json_file)
            return self.docs
        except:
            a=''
        with open("data/recomendation.json",'r') as data:
            a=json.load(data)
        tp=TextProcessor()
        tp.query_processor(a)
        return tp.similarity()
    
