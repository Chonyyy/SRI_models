   
from typing import Callable
from code.document import Document
import numpy as np
import math
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class Vector_Model_G():

    def __init__(self, text_processor: Callable[[str, str], list[str]]):
        self.documents:list[Document] = [] 
        self.text_processor = text_processor
        """
        This is the set of all words in the collection of documents
        """
        self.tc: dict[tuple[str, int], float] = {}
        """
        This is the count of the terms in the doc
        """
        self.tf: dict[tuple[str, int], float] = {}
        """
        This is the relative frequency of a token in a document. 
        Dictionary where the key is a tuple (term_str, doc_index) and the value is the tf of the term in the document"""
        self.df: dict[str, int] = {}
        """
        This is the amount of documents in which the term is present
        """
        self.smooth_constant: float = 0.5
        """
        This is the smooth constant for the query formula
        """
        self.document_vector_dirty = False
        """
        This is a property to know when is necessary to recalculate the document vectors
        """
        self.document_vectors: list[list[tuple[str, float]]] = []
        """
        This is the dictionary where the key is the document_id and the value is a list of tuples (term_index, tf * idf)
        """
        # This acts as a cache for storing the last ranking of a consult, this is in the case of handling result pages
        self.last_ranking: list[tuple[float, int]] = []
        # Inicializar un vectorizador TF-IDF para convertir texto en vectores de alta dimensión
        self.vectorizer = TfidfVectorizer()
        
    def set_smooth_constant(self, smooth: float):
        """This method is for setting the smooth constant for the query formula

        Args:
            smooth (float): Smooth Constant
        """
        self.smooth_constant = max(0.1, min(1, smooth))

    def add_document(self, document: Document):
        # tell the model that needs to recalculate the vectors of documents
        self.document_vector_dirty = True
        self.documents.append(document)
        title = ' '.join(document.doc_normalized_name)  # Convertir la lista de palabras en una cadena de texto
        body = ' '.join(document.doc_normalized_body)  # Convertir la lista de palabras en una cadena de texto
        text = title + ' ' + body  # Ahora 'text' es una cadena de texto
        term_frequency = self.__get_tf(text)
        # Add the document to the list of documents
        # Update the amount of documents in which the term is
        for token in term_frequency:
            if token in self.df:
                self.df[token] +=  1
            else:
                self.df[token] =  1
            self.tf[(token, len(self.documents) -  1)] = term_frequency[token]
            
    def __get_tf(self, text: list[str]) -> dict[str, float]:
        """Generate the normalized term frequency of a text as a dictionary

        Args:
            text (list[str]): A list of normalized string tokens

        Returns:
            dict[str, int]: Dictionary where the key is a term and the value is the frequency of the term in the text
        """
        tf: dict[str, float] = { }# Dictionary where the key is a term and the value is the frequency of the term in the document
        tc: dict[str, float] = { }
        
        max_frequency = 0  # The maximum frequency of a term in the document
        for token in text:
            if token in tf:
                tf[token] += 1
                tc[token] += 1
            else:
                tf[token] = 1
                tc[token] += 1
            if tf[token] > max_frequency:
                max_frequency = tf[token]
        # Normalize the term frequency
        for token in tf:
            tf[token] = tf[token] / max_frequency
        return tf

    def generate_document_vectors(self):
         # Convertir todos los documentos en vectores de alta dimensión
        self.document_vectors = self.vectorizer.fit_transform(
            [doc.doc_normalized_name + ' ' + doc.doc_normalized_body for doc in self.documents]
        ).toarray()

    def calculate_minterms(self,vector):
        minterms = []
        for vector in self.tc:
            vector = []
            for x in vector:
                if x != 0:
                    vector.append(1)
                else:
                    vector.append(0)
            if vector not in minterms:
                minterms.append(vector)
            vector.clear()
        return minterms
                
        
    def calculate_coefficients(document_vector, query_vector):
        coefficients = []
        for i in range(len(document_vector)):
            c = sum([document_vector[i][j] * query_vector[j] for j in range(len(document_vector[i]))])
            coefficients.append(c)
        return coefficients
    
    def calculate_k_vectors(coefficients, independent_vectors):
        k_vectors = []
        for i in range(len(coefficients)):
            k = sum([coefficients[i][j] * independent_vectors[j] for j in range(len(coefficients[i]))])
            k_vectors.append(k)
        return k_vectors

    def generate_query_vector(self, query: str, lang: str = 'english'):
        # Convertir la consulta en un vector de alta dimensión
        query_vector = self.vectorizer.transform([query]).toarray()
        return query_vector

    # [ ]: se escribe similarity
    def similitud(self, vector1: list[tuple[str, float]], vector2: list[tuple[str, float]]) -> float:
        # Calcular la similitud entre dos vectores de alta dimensión
        return cosine_similarity(vector1.reshape(1, -1), vector2.reshape(1, -1))[0][0]

    def get_ranking(self, query: str, first_n_results: int, offset:int = 0, lang: str = 'english'):
         # Calcular la similitud entre la consulta y cada documento
        self.generate_document_vectors()
        query_vector = self.generate_query_vector(query, lang)
        doc_rank = []
        for index, doc_vector in enumerate(self.document_vectors):
            sim = self.similitud(doc_vector, query_vector)
            doc_rank.append((sim, index))
        self.last_ranking = sorted(doc_rank, key=lambda rank_index: rank_index[0], reverse=True)
        return [(self.documents[doc], rank) for rank, doc in self.last_ranking[offset:offset + first_n_results]]
    
    def feedback(self, relevant_docs:list[int]):
        pass
    
    def _get_document_by_id(self, documents:list[Document], id:int, start:int, end:int) -> Document:
            if start > end:
                return None
            mid = (start + end) // 2
            if documents[mid].doc_id == id:
                return documents[mid]
            elif documents[mid].doc_id < id:
                return self._get_document_by_id(documents, id, mid + 1, end)
            else:
                return self._get_document_by_id(documents, id, start, mid - 1)

    #TODO: remake this method with binary search
    def get_document_by_id(self, id:int) -> Document:
        return self._get_document_by_id(self.documents, id, 0, len(self.documents) - 1)
                