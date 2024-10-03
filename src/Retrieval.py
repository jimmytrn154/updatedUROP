from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import pandas as pd
from tabulate import tabulate


keywords = ["food", "service", "price", "atmosphere", "location"]
restaurants = [
    "Restaurant A", "Restaurant B", "Restaurant C", 
    "Restaurant D", "Restaurant E", "Restaurant F", 
    "Restaurant G", "Restaurant H", "Restaurant I", 
    "Restaurant J", "Restaurant K", "Restaurant L"
]

# Keyword mentions represented as binary mentions (1: mentioned, 0: not mentioned)
keyword_mentions = [
    [1, 0, 1, 0, 1],  # "food", "price", "atmosphere"
    [0, 1, 0, 1, 0],  # "service", "atmosphere"
    [0, 0, 1, 1, 1],  # "food", "service", "location"
    [0, 0, 1, 0, 0],  # "atmosphere"
    [1, 0, 1, 0, 1],  # "food", "price", "location"
    [0, 0, 1, 1, 0],  # "price", "service"
    [1, 0, 0, 1, 1],  # "food", "atmosphere", "location"
    [1, 1, 0, 1, 0],  # "food", "service", "location"
    [0, 1, 1, 1, 1],  # "service", "price", "location"
    [1, 0, 0, 0, 1],  # "food", "location"
    [1, 0, 1, 0, 1],  # "food", "price", "location"
    [0, 0, 0, 1, 0]   # "atmosphere"
]

restaurant_docs = []
for mention in keyword_mentions:
    doc = []
    for idx, val in enumerate(mention):
        if val == 1:
            doc.append(keywords[idx])
    restaurant_docs.append(" ".join(doc))


user_preference = np.array([0, 0, 1, 1, 1])  


tfidf_vectorizer = TfidfVectorizer(vocabulary=keywords)
tfidf_matrix = tfidf_vectorizer.fit_transform(restaurant_docs).toarray()

user_preference_vector = user_preference.reshape(1, -1)
restaurant_scores = user_preference_vector.dot(tfidf_matrix.T)

K = 5
top_k_indices = restaurant_scores.argsort()[0][::-1][:K]
top_k_restaurants = [restaurants[i] for i in top_k_indices]

result_df = pd.DataFrame({
    'Restaurant': top_k_restaurants,
    'Score': restaurant_scores[0][top_k_indices]
})

print(tabulate(result_df, headers='keys', tablefmt='grid'))
