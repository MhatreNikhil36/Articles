import unittest
from main import TextVectorizer

class TestTextVectorizer(unittest.TestCase):

    def setUp(self):
        self.corpus = [
            "it was the best of times",
            "it was the worst of times",
            "it was the age of wisdom",
            "it was the age of foolishness"
        ]
        self.vectorizer = TextVectorizer(self.corpus)

    def test_vocab_length(self):
        expected_vocab = [
            'age', 'best', 'foolishness', 'it', 'of',
            'the', 'times', 'was', 'wisdom', 'worst'
        ]
        self.assertEqual(self.vectorizer.vocab, sorted(expected_vocab))

    def test_vectorization_shape(self):
        vectors = self.vectorizer.get_vectorized_corpus()
        self.assertEqual(len(vectors), 4)         # 4 documents
        self.assertEqual(len(vectors[0]), 10)     # 10 unique words

    def test_vector_values(self):
        vectors = self.vectorizer.get_vectorized_corpus()
        # "it was the best of times" → [0, 1, 0, 1, 1, 1, 1, 1, 0, 0]
        self.assertEqual(vectors[0], [0, 1, 0, 1, 1, 1, 1, 1, 0, 0])

    def test_cosine_similarity_self(self):
        vectors = self.vectorizer.get_vectorized_corpus()
        sim = self.vectorizer.cosine_similarity(vectors[0], vectors[0])
        self.assertAlmostEqual(sim, 1.0)

    def test_cosine_similarity_different(self):
        vectors = self.vectorizer.get_vectorized_corpus()
        sim = self.vectorizer.cosine_similarity(vectors[2], vectors[3])
        self.assertAlmostEqual(sim, 0.8333333, places=4)

    def test_zero_vector_similarity(self):
        vec1 = [0, 0, 0]
        vec2 = [1, 0, 0]
        sim = self.vectorizer.cosine_similarity(vec1, vec2)
        self.assertEqual(sim, 0.0)

if __name__ == '__main__':
    unittest.main()
