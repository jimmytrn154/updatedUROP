import gradio as gr
import random
from sentence_transformers import SentenceTransformer
import numpy as np

# Load a pre-trained sentence transformer model
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Simulated database of restaurants
restaurants = [
    {"id": 1, "name": "Pasta Paradise", "cuisine": "Italian", "keywords": ["pasta", "cozy", "romantic"]},
    {"id": 2, "name": "Sushi Sensation", "cuisine": "Japanese", "keywords": ["sushi", "fresh", "modern"]},
    {"id": 3, "name": "Burger Bliss", "cuisine": "American", "keywords": ["burger", "casual", "family-friendly"]},
    {"id": 4, "name": "Spice Avenue", "cuisine": "Indian", "keywords": ["spicy", "authentic", "vegetarian-friendly"]},
    {"id": 5, "name": "Mediterranean Delight", "cuisine": "Mediterranean", "keywords": ["healthy", "seafood", "outdoor seating"]}
]

# Pre-compute embeddings for all restaurants
for restaurant in restaurants:
    restaurant['embedding'] = model.encode(" ".join(restaurant['keywords']))

def extract_keywords(review):
    # Simple keyword extraction (in a real scenario, use NLP techniques)
    words = review.lower().split()
    return [word for word in words if len(word) > 3]

def retrieve_candidates(keywords, k=3):
    query_embedding = model.encode(" ".join(keywords))
    similarities = [np.dot(query_embedding, r['embedding']) for r in restaurants]
    top_k_indices = np.argsort(similarities)[-k:][::-1]
    return [restaurants[i] for i in top_k_indices]

def generate_prompt(user_keywords, restaurant):
    return f"User keywords: {', '.join(user_keywords)}\nRestaurant: {restaurant['name']}\nCuisine: {restaurant['cuisine']}\nKeywords: {', '.join(restaurant['keywords'])}"

def llm_rerank(candidates, prompt):
    # Simulate LLM re-ranking with a simple scoring function
    def score_candidate(candidate, user_keywords):
        return sum(1 for keyword in user_keywords if keyword in candidate['keywords'])
    
    scored_candidates = [(candidate, score_candidate(candidate, prompt.split(', ')[1:])) for candidate in candidates]
    return [candidate for candidate, _ in sorted(scored_candidates, key=lambda x: x[1], reverse=True)]

def recommend_restaurants(user_review, is_cold_start=False):
    if is_cold_start:
        user_keywords = user_review.split(',')
    else:
        user_keywords = extract_keywords(user_review)
    
    candidates = retrieve_candidates(user_keywords)
    
    prompt = generate_prompt(user_keywords, candidates[0])
    ranked_results = llm_rerank(candidates, prompt)
    
    return "\n\n".join([f"Name: {r['name']}\nCuisine: {r['cuisine']}\nKeywords: {', '.join(r['keywords'])}" for r in ranked_results])

# Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# KALM4REC-inspired Restaurant Recommendation Demo")
    
    with gr.Tab("Regular User"):
        review_input = gr.Textbox(label="Enter your restaurant review")
        regular_output = gr.Textbox(label="Recommended Restaurants")
        regular_button = gr.Button("Get Recommendations")
    
    with gr.Tab("Cold-Start User"):
        keywords_input = gr.Textbox(label="Enter keywords (comma-separated)")
        cold_start_output = gr.Textbox(label="Recommended Restaurants")
        cold_start_button = gr.Button("Get Recommendations")

    regular_button.click(recommend_restaurants, inputs=review_input, outputs=regular_output)
    cold_start_button.click(lambda x: recommend_restaurants(x, True), inputs=keywords_input, outputs=cold_start_output)

demo.launch()
