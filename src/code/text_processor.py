import ir_datasets
import nltk
import gensim
from query import Query

class TextProcessor:
    def __init__(self):
        self.dictionary = {}
        self.corpus = []
        dataset = ir_datasets.load("cranfield")
        self.docs = [doc.text for doc in dataset.docs_iter()]
        self.tokenized_docs = self.filter_tokens_by_occurrence(self.morphological_reduction_nltk(self.remove_stopwords(self.remove_noise_nltk(self.tokenization_nltk()))))
        self.vector_repr = self.vector_representation(self.tokenized_docs, self.dictionary)

    def tokenization_nltk(self):
        #Tokenize the query using NLTK
        tokenized = [nltk.tokenize.word_tokenize(doc) for doc in self.docs[:10]]
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

    def filter_tokens_by_occurrence(self, tokenized_docs, no_below=2, no_above=0.5):
        if not self.dictionary:
            self.dictionary = gensim.corpora.Dictionary(tokenized_docs)
            self.dictionary.filter_extremes(no_below=no_below, no_above=no_above)
     
        filtered_words = [word for _, word in self.dictionary.iteritems()]
        return [
            [word for word in doc if word in filtered_words]
            for doc in tokenized_docs
        ]
    
    def vector_representation(self, tokenized_docs, dictionary, use_bow=False):
        if not self.corpus:
            self.corpus = [dictionary.doc2bow(doc) for doc in tokenized_docs]

        if use_bow:
            vector_repr = self.corpus
        else:
            tfidf = gensim.models.TfidfModel(self.corpus)
            vector_repr = [tfidf[doc] for doc in self.corpus]

        return vector_repr
    
    def query_processor(self, query, use_bow=False):
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

    def similarity(self):
        #Find matched documents based on the query
        index = gensim.similarities.MatrixSimilarity(self.vector_repr)
                
        similarities = index[self.query_processed.vector_repr]
        top_matches = sorted(enumerate(similarities), key=lambda x: -(x[1]))

        best_match_indices = [match[0] for match in top_matches]
        return best_match_indices