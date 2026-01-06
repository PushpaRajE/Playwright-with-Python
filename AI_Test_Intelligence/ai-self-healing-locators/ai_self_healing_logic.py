import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def text_to_vector(text):
    vector = [0] * 26
    for char in text.lower():
        if char.isalpha():
            vector[ord(char) - 97] += 1
    return vector

def find_best_match(target_text, candidate_texts):
    target_vec = np.array([text_to_vector(target_text)])
    scores = []

    for text in candidate_texts:
        vec = np.array([text_to_vector(text)])
        similarity = cosine_similarity(target_vec, vec)[0][0]
        scores.append(similarity)

    best_index = scores.index(max(scores))
    return candidate_texts[best_index]
