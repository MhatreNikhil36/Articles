# 📚 TextVectorizer: Representing Text as Vectors & Measuring Similarity

Welcome to **TextVectorizer**, a lightweight Python library that demonstrates how **textual data can be represented as vectors**, and how to **compute similarity between them using cosine similarity**—built entirely in Python with no external ML libraries.

---

## 🚀 What Does This Library Do?

* ✅ Converts a corpus of text documents into numeric **vectors** (Count Vectorization)
* ✅ Stores and exposes the **vocabulary** used for vectorization
* ✅ Computes **cosine similarity** between any two documents
* ✅ Helps understand the **mathematics behind NLP vector spaces**

---

## 🧠 Core Concepts

### 1. **What is a Vector?**

In Data Science, especially NLP (Natural Language Processing), we often represent **documents as vectors** in a high-dimensional space. Each dimension corresponds to a word in our **vocabulary**, and the value represents how often the word appears in the document.

For example:

```
Document: "it was the best of times"
Vocabulary: ['age', 'best', 'foolishness', 'it', 'of', 'the', 'times', 'was', 'wisdom', 'worst']
Vector:     [ 0,      1,     0,           1,    1,    1,     1,      1,     0,       0 ]
```

### 2. **Corpus & Vocabulary**

* **Corpus**: The entire collection of text documents.
* **Vocabulary**: The set of all unique words across the corpus. This determines the **dimensionality of the vector space**.

### 3. **Count Vectorization**

A simple form of vectorization where each document is converted into a vector of **word counts** corresponding to the vocabulary.

### 4. **Cosine Similarity**

Cosine similarity is a measure of similarity between two vectors. It captures the **angle** between them:

$$
\text{cosine\_similarity} = \frac{\vec{A} \cdot \vec{B}}{||A|| \times ||B||}
$$

* **1.0** → Vectors are identical
* **0.0** → Vectors are orthogonal (no similarity)
* **< 1.0** → Partial similarity

This is especially useful in **text analysis**, where you want to know how similar two documents are, even if they're not exactly the same.

---

## 🔧 How It Works

```python
from text_vectorizer import TextVectorizer

corpus = [
    "it was the best of times",
    "it was the worst of times",
    "it was the age of wisdom",
    "it was the age of foolishness"
]

vectorizer = TextVectorizer(corpus)
vectors = vectorizer.get_vectorized_corpus()

similarity = vectorizer.cosine_similarity(vectors[2], vectors[3])
print(f"Cosine Similarity: {similarity}")
```

---

## 📂 Structure

* `TextVectorizer` class:

  * `__init__(corpus)` – builds the vocabulary and vectorizes the corpus
  * `build_vocab()` – extracts unique words
  * `vectorize_document()` – turns a document into a vector
  * `cosine_similarity(vec1, vec2)` – computes cosine similarity
  * `get_vectorized_corpus()` – returns all document vectors

---

## ✅ Use Cases

* Educational purpose: Understand how text data can be represented mathematically
* Rapid prototyping for simple NLP tasks
* Comparing text similarity in search engines, chatbots, and recommendation engines

---

## 🧪 Example Output

```plaintext
Cosine Similarity: 0.8333
```

This means the sentences *“it was the age of wisdom”* and *“it was the age of foolishness”* are quite similar in structure and shared words, despite differing in meaning.

---

## 📌 Conclusion

This simple library reflects the **core of modern NLP techniques**: representing data in vector form to find **relationships and patterns**. While this uses basic Count Vectorization, it sets the stage for deeper concepts like TF-IDF, Word2Vec, and Transformers.

> *“We all are vectors. Many of us are still in search of direction.”*

