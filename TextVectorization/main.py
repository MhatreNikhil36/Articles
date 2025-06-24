import math
import re
from collections import Counter

class TextVectorizer:
    def __init__(self, corpus):
        self.corpus = corpus
        self.vocab = self.build_vocab(corpus)
        self.vectorized_corpus = self.vectorize_corpus(corpus)
    
    def build_vocab(self, corpus):
        # Extract unique words from the corpus
        words = set()
        for doc in corpus:
            words.update(self.extract_words(doc))
        return sorted(words)
    
    def extract_words(self, text):
        # Tokenize and clean text into words
        return re.findall(r'\b\w+\b', text.lower())
    
    def vectorize_document(self, doc):
        # Create a vector for a single document based on the vocabulary
        word_counts = Counter(self.extract_words(doc))
        return [word_counts[word] for word in self.vocab]
    
    def vectorize_corpus(self, corpus):
        # Vectorize the entire corpus
        return [self.vectorize_document(doc) for doc in corpus]
    
    def cosine_similarity(self, vector1, vector2):
        # Calculate cosine similarity between two vectors
        dot_product = sum(x * y for x, y in zip(vector1, vector2))
        magnitude1 = math.sqrt(sum(x ** 2 for x in vector1))
        magnitude2 = math.sqrt(sum(y ** 2 for y in vector2))
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        else:
            return dot_product / (magnitude1 * magnitude2)
    
    def get_vectorized_corpus(self):
        return self.vectorized_corpus

# Example usage:
corpus = [
    "it was the best of times",
    "it was the worst of times",
    "it was the age of wisdom",
    "it was the age of foolishness"
]

vectorizer = TextVectorizer(corpus)
vectorized_corpus = vectorizer.get_vectorized_corpus()

# Calculate cosine similarity between two documents
similarity = vectorizer.cosine_similarity(vectorized_corpus[2], vectorized_corpus[3])
print(f"Cosine Similarity: {similarity}")
