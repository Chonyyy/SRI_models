import nltk

class Query:
    def __init__(self, query):
        self.query = query
        self.tokenized_query = []
        self.vector_repr = []
        self.query_bow = []

    def tokenization_nltk(self):
        #Tokenize the query using NLTK
        self.tokenized_query = nltk.tokenize.word_tokenize(self.query)

    def remove_noise_nltk(self):
        #Remove noise from the tokenized query using NLTK
        self.tokenized_query = [word.lower() for word in self.tokenized_query if word.isalpha()]

    def remove_stopwords(self):
        #Remove stopwords from the tokenized query
        stop_words = set(nltk.corpus.stopwords.words('english'))
        self.tokenized_query = [word for word in self.tokenized_query if word not in stop_words]

    def morphological_reduction_nltk(self, use_lemmatization=True):
        # Perform morphological reduction (lemmatization or stemming) using NLTK
        if use_lemmatization:
            lemmatizer = nltk.stem.WordNetLemmatizer()
            self.tokenized_query = [lemmatizer.lemmatize(word) for word in self.tokenized_query]
                
        else:
            stemmer = nltk.stem.PorterStemmer()
            self.tokenized_query = [stemmer.stem(word) for word in self.tokenized_query]

    def process_query(self):
        self.tokenization_nltk()
        self.remove_noise_nltk()
        self.remove_stopwords()
        self.morphological_reduction_nltk()
        