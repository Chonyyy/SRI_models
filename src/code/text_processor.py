import ir_datasets
import nltk
import gensim
from code.query import Query
import numpy as np
import math
import json

class TextProcessor:
    """
    A class for processing text documents and queries for information retrieval tasks.

    Attributes:
        dictionary (gensim.corpora.Dictionary): A dictionary mapping words to their integer ids.
        corpus (list): A list of bag-of-words representations of documents.
        docs (list): A list of raw text documents.
        docID (dict): A dictionary mapping document text to its index in `docs`.
        tokenized_docs (list): A list of tokenized documents.
        vocabulary (list): A list of words in the vocabulary.
        vector_repr (list): A list of vector representations of documents.
        current_query (str): The current query being processed.
        query_processed (Query): An instance of Query class representing the processed query.
    """

    def __init__(self):
        """
        Initializes TextProcessor with empty attributes.
        """
        self.dictionary = {}
        self.corpus = []
        dataset = ir_datasets.load("cranfield")
        self.docs = [doc.text for doc in dataset.docs_iter()]
        self.docID = dict()
        for i in range(len(self.docs)):
            self.docID[self.docs[i]] = i
        del self.docs[470]
        del self.docs[993]
        self.tokenized_docs = self.filter_tokens_by_occurrence(self.morphological_reduction_nltk(self.remove_stopwords(self.remove_noise_nltk(self.tokenization_nltk()))))
        self.vocabulary = list(self.dictionary.token2id.keys())
        self.vector_repr = self.vector_representation(self.tokenized_docs, self.dictionary)
        self.vector_repr = self.generalize(self.vector_repr)

    def tokenization_nltk(self):
        """
        Tokenizes documents using NLTK.

        Returns:
            list: A list of tokenized documents.
        """
        added_tokens = dict()
        try:
            with open('data/feedback.json', 'x') as json_file:
                json.dump({}, json_file)
            return [nltk.tokenize.word_tokenize(doc) for doc in self.docs]
        except FileExistsError:
            with open("data/feedback.json", 'r') as data:
                added_tokens = json.load(data)
        docs = [d + added_tokens[d] if d in added_tokens.keys() else d for d in self.docs]
        tokenized = [nltk.tokenize.word_tokenize(doc) for doc in docs]
        return tokenized

    def remove_noise_nltk(self, tokenized_docs):
        """
        Removes noise from tokenized documents.

        Args:
            tokenized_docs (list): A list of tokenized documents.

        Returns:
            list: A list of cleaned tokenized documents.
        """
        return [[word.lower() for word in doc if word.isalpha()] for doc in tokenized_docs]

    def remove_stopwords(self, tokenized_docs):
        """
        Removes stopwords from tokenized documents.

        Args:
            tokenized_docs (list): A list of tokenized documents.

        Returns:
            list: A list of tokenized documents with stopwords removed.
        """
        stop_words = set(nltk.corpus.stopwords.words('english'))
        return [[word for word in doc if word not in stop_words] for doc in tokenized_docs]

    def morphological_reduction_nltk(self, tokenized_docs, use_lemmatization=True):
        """
        Reduces words to their base form using NLTK's lemmatizer or stemmer.

        Args:
            tokenized_docs (list): A list of tokenized documents.
            use_lemmatization (bool): Whether to use lemmatization or stemming.

        Returns:
            list: A list of tokenized documents with morphological reduction applied.
        """
        if use_lemmatization:
            lemmatizer = nltk.stem.WordNetLemmatizer()
            tokenized_docs = [[lemmatizer.lemmatize(word) for word in doc] for doc in tokenized_docs]
        else:
            stemmer = nltk.stem.PorterStemmer()
            tokenized_docs = [[stemmer.stem(word) for word in doc] for doc in tokenized_docs]

        return tokenized_docs

    def filter_tokens_by_occurrence(self, tokenized_docs, no_below=5, no_above=0.5):
        """
        Filters tokens based on their occurrence in documents.

        Args:
            tokenized_docs (list): A list of tokenized documents.
            no_below (int): Keep tokens which occur in at least `no_below` documents.
            no_above (float): Keep tokens which occur in less than `no_above` fraction of documents.

        Returns:
            list: A list of filtered tokenized documents.
        """
        if not self.dictionary:
            self.dictionary = gensim.corpora.Dictionary(tokenized_docs)
            self.dictionary.filter_extremes(no_below=no_below, no_above=no_above)
        filtered_words = [word for _, word in self.dictionary.iteritems()]
        return [[word for word in doc if word in filtered_words] for doc in tokenized_docs]

    def vector_representation(self, tokenized_docs, dictionary, use_bow=True):
        """
        Generates vector representations of documents using bag-of-words or TF-IDF.

        Args:
            tokenized_docs (list): A list of tokenized documents.
            dictionary (gensim.corpora.Dictionary): A dictionary mapping words to their integer ids.
            use_bow (bool): Whether to use bag-of-words representation.

        Returns:
            list: A list of vector representations of documents.
        """
        if not self.corpus:
            self.corpus = [dictionary.doc2bow(doc) for doc in tokenized_docs]

        if use_bow:
            vector_repr = self.corpus
        else:
            tfidf = gensim.models.TfidfModel(self.corpus)
            vector_repr = [tfidf[doc] for doc in self.corpus]

        return vector_repr

    def generate_independets_vectors(self):
        """
        Generates independent vectors for documents.

        Returns:
            np.array: An array of independent vectors.
        """
        vector_inicial = [1] + [0] * (len(self.vector_repr) - 1)
        lista_de_vectores = [vector_inicial[-i:] + vector_inicial[:-i] for i in range(len(self.vector_repr))]
        return np.array(lista_de_vectores)

    def generalize(self, vectors_weight, query=False):
        """
        Generalizes document vectors.

        Args:
            vectors_weight (list): A list of vectors with their corresponding weights.
            query (bool): Whether the vectors correspond to a query.

        Returns:
            list: A list of generalized vectors.
        """
        c = [[0] * len(self.vector_repr) for _ in range(len(self.vocabulary))]
        vectors = self.generate_independets_vectors()

        for i, k in zip(self.vector_repr, range(len(self.vector_repr))):
            for j in i:
                c[j[0]][k] += j[1]

        k_i = []
        k = 0
        for i in c:
            c_big = 0
            for j, v in zip(i, vectors):
                k = k + j * v
                c_big += j ** 2
            k_i.append((k / math.sqrt(c_big)).tolist())
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
                new_weight = 0
                for vector in vectors_weight[doc]:
                    for doc in range(len(vectors_weight)):
                        new_weight += k_i[vector[0]][doc] * vector[1]
                    new_tuple.append((vector[0], new_weight))
                new_vectors.append(new_tuple)
        return new_vectors

    def query_processor(self, query, use_bow=True, Save=True):
        """
        Processes a query for information retrieval.

        Args:
            query (str): The query to be processed.
            use_bow (bool): Whether to use bag-of-words representation.
            Save (bool): Whether to save the query.

        Returns:
            None
        """
        self.current_query = query
        if Save:
            self.save(query)
        self.query_processed = Query(query)
        self.query_processed.process_query()

        filtered_words = [word for _, word in self.dictionary.iteritems()]
        self.query_processed.tokenized_query = [word for word in self.query_processed.tokenized_query if word in filtered_words]

        self.query_processed.query_bow = self.dictionary.doc2bow(self.query_processed.tokenized_query)

        if use_bow:
            self.query_processed.vector_repr = self.query_processed.query_bow
        else:
            tfidf = gensim.models.TfidfModel(self.corpus)
            self.query_processed.vector_repr = tfidf[self.query_processed.query_bow]

        self.query_processed.vector_repr = self.generalize(self.query_processed.vector_repr, query=True)

    def similarity(self):
        """
        Computes similarity between the query and documents.

        Returns:
            map: A map of document indices to their similarity scores.
        """
        index = gensim.similarities.MatrixSimilarity(self.vector_repr)
        similarities = index[self.query_processed.vector_repr]
        top_matches = sorted(enumerate(similarities), key=lambda x: -(x[1]))
        best_match_indices = [match[0] for match in top_matches if match[1] > 1e-8]
        return map(lambda x: self.docs[x], best_match_indices)

    def feedback(self, document):
        """
        Provides feedback for a given document.

        Args:
            document (str): The document to provide feedback for.

        Returns:
            None
        """
        feedback_added = dict()
        try:
            with open('data/feedback.json', 'x') as json_file:
                json.dump({document: self.current_query}, json_file)
            return
        except FileExistsError:
            with open("data/feedback.json", 'r') as data:
                feedback_added = json.load(data)
        if document in feedback_added:
            feedback_added[document] += '\n' + self.current_query
        else:
            feedback_added[document] = self.current_query
        with open('data/feedback.json', 'w') as data:
            json.dump(feedback_added, data)

    def save(self, query):
        """
        Saves a query.

        Args:
            query (str): The query to be saved.

        Returns:
            None
        """
        saved_quey = ''
        try:
            with open('data/recomendation.json', 'x') as json_file:
                json.dump(query, json_file)
            return
        except FileExistsError:
            with open("data/recomendation.json", 'r') as data:
                saved_quey = json.load(data)
        saved_quey += ' ' + query
        with open('data/recomendation.json', 'w') as data:
            json.dump(saved_quey, data)

    def recommend(self):
        """
        Recommends documents based on saved queries.

        Returns:
            list: A list of recommended documents.
        """
        recomended_query = ''
        try:
            with open('data/recomendation.json', 'x') as json_file:
                json.dump("", json_file)
            return self.docs
        except:
            recomended_query = ''
        with open("data/recomendation.json", 'r') as data:
            recomended_query = json.load(data)
        self.query_processor(recomended_query, Save=False)
        return self.similarity()
