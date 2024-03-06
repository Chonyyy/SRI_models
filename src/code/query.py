"""
This module provides a class for processing queries.

Attributes:
    None

Classes:
    Query: A class for processing queries.

Functions:
    None
"""

import nltk

class Query:
    """
    A class for processing queries.

    Attributes:
        query (str): The query string.
        tokenized_query (list): The tokenized version of the query.
        vector_repr (list): The vector representation of the query.
        query_bow (list): The bag-of-words representation of the query.
    """

    def __init__(self, query):
        """
        Initializes a Query object.

        Args:
            query (str): The query string.
        """
        self.query = query
        self.tokenized_query = []
        self.vector_repr = []
        self.query_bow = []

    def tokenization_nltk(self):
        """
        Tokenizes the query using NLTK tokenizer.
        """
        self.tokenized_query = nltk.tokenize.word_tokenize(self.query)

    def remove_noise_nltk(self):
        """
        Removes noise from the tokenized query using NLTK.
        """
        self.tokenized_query = [word.lower() for word in self.tokenized_query if word.isalpha()]

    def remove_stopwords(self):
        """
        Removes stopwords from the tokenized query.
        """
        stop_words = set(nltk.corpus.stopwords.words('english'))
        self.tokenized_query = [word for word in self.tokenized_query if word not in stop_words]

    def morphological_reduction_nltk(self, use_lemmatization=True):
        """
        Performs morphological reduction (lemmatization or stemming) using NLTK.

        Args:
            use_lemmatization (bool, optional): Whether to use lemmatization. Defaults to True.
        """
        if use_lemmatization:
            lemmatizer = nltk.stem.WordNetLemmatizer()
            self.tokenized_query = [lemmatizer.lemmatize(word) for word in self.tokenized_query]
                
        else:
            stemmer = nltk.stem.PorterStemmer()
            self.tokenized_query = [stemmer.stem(word) for word in self.tokenized_query]

    def process_query(self):
        """
        Processes the query by tokenization, noise removal, stopword removal, and morphological reduction.
        """
        self.tokenization_nltk()
        self.remove_noise_nltk()
        self.remove_stopwords()
        self.morphological_reduction_nltk()
