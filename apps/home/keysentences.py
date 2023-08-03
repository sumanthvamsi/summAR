import gensim.downloader
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def key_sentences(paragraph, num_sentences=10):
    # Load pre-trained Word2Vec model
    word_vectors = gensim.downloader.load('word2vec-google-news-300')

    # Tokenize the paragraph into sentences
    sentences = [sentence.strip() for sentence in paragraph.split('.') if sentence.strip() != '']

    # Calculate sentence embeddings by averaging word embeddings
    sentence_embeddings = []
    for sentence in sentences:
        word_tokens = gensim.utils.simple_preprocess(sentence)
        sentence_vector = np.mean([word_vectors[word] for word in word_tokens if word in word_vectors], axis=0)
        sentence_embeddings.append(sentence_vector)

    # Calculate sentence similarity using cosine similarity
    sentence_similarity = cosine_similarity(sentence_embeddings)

    # Find the most representative sentence (centroid) as the key sentence
    centroid = np.mean(sentence_similarity, axis=0)
    ranked_sentences = [(centroid[i], sentences[i]) for i in range(len(sentences))]

    # Sort sentences by score in descending order
    ranked_sentences.sort(key=lambda x: x[0], reverse=True)

    # Get the top 'num_sentences' sentences as key sentences
    key_sentences = [sentence for score, sentence in ranked_sentences[:num_sentences]]

    return key_sentences

