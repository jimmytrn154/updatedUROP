import gradio as gr
import random
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Dict

# Simulated database of products with pre-computed embeddings
products = [
    {"id": 1, "name": "Spaghetti Carbonara", "category": "Italian", "description": "Creamy pasta dish with eggs, cheese, and pancetta"},
    {"id": 2, "name": "Sushi Platter", "category": "Japanese", "description": "Assorted fresh fish and rice rolls"},
    {"id": 3, "name": "Beef Burger", "category": "American", "description": "Juicy beef patty with lettuce, tomato, and cheese"},
    {"id": 4, "name": "Pad Thai", "category": "Thai", "description": "Stir-fried rice noodles with tofu, shrimp, and peanuts"},
    {"id": 5, "name": "Chicken Tikka Masala", "category": "Indian", "description": "Tender chicken in a creamy tomato-based sauce"}
]

# Load a pre-trained sentence transformer model
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Pre-compute embeddings for all products
for product in products:
    product['embedding'] = model.encode(product['name'] + " " + product['description'])

def candidates_retrieval(query: str, k: int = 3) -> List[Dict]:
    query_embedding = model.encode(query)
    similarities = [np.dot(query_embedding, p['embedding']) for p in products]
    top_k_indices = np.argsort(similarities)[-k:][::-1]
    return [products[i] for i in top_k_indices]

def llm_ranker(query: str, candidates: List[Dict]) -> List[Dict]:
    # Simulate LLM ranking with a simple scoring function
    # In a real scenario, you would call an actual LLM API here
    def score_candidate(candidate):
        relevance = sum(1 for word in query.lower().split() if word in candidate['name'].lower() or word in candidate['description'].lower())
        return relevance * np.random.random()  # Add some randomness to simulate LLM behavior
    
    scored_candidates = [(candidate, score_candidate(candidate)) for candidate in candidates]
    return [candidate for candidate, _ in sorted(scored_candidates, key=lambda x: x[1], reverse=True)]

def search_and_rank(query):
    candidates = candidates_retrieval(query)
    ranked_results = llm_ranker(query, candidates)
    return "\n".join([f"{p['name']} - {p['category']}\n{p['description']}\n" for p in ranked_results])

def get_product_details(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        return f"Name: {product['name']}\nCategory: {product['category']}\nDescription: {product['description']}"
    return "Product not found"

def recommend_items(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        query = product['name'] + " " + product['description']
        candidates = candidates_retrieval(query, k=4)  # Get 4 candidates
        recommendations = [p for p in candidates if p['id'] != product_id][:3]  # Exclude the input product and limit to 3
        return "\n".join([f"{p['name']} - {p['category']}\n{p['description']}\n" for p in recommendations])
    return "No recommendations available"

def cold_start_recommend(keywords):
    recommendations = candidates_retrieval(keywords, k=5)
    return "\n".join([f"{p['name']} - {p['category']}\n{p['description']}\n" for p in recommendations])

# Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# Enhanced Restaurant Recommendation System Demo")
    
    with gr.Tab("Search"):
        search_input = gr.Textbox(label="Search for dishes")
        search_output = gr.Textbox(label="Search Results")
        search_button = gr.Button("Search")
    
    with gr.Tab("Product Details"):
        product_id_input = gr.Number(label="Enter Product ID")
        product_details_output = gr.Textbox(label="Product Details")
        details_button = gr.Button("Get Details")
    
    with gr.Tab("Recommendations"):
        recommend_id_input = gr.Number(label="Enter Product ID for Recommendations")
        recommend_output = gr.Textbox(label="Recommended Items")
        recommend_button = gr.Button("Get Recommendations")
    
    with gr.Tab("Cold Start Recommendations"):
        keywords_input = gr.Textbox(label="Enter keywords")
        cold_start_output = gr.Textbox(label="Recommended Items")
        cold_start_button = gr.Button("Get Recommendations")

    search_button.click(search_and_rank, inputs=search_input, outputs=search_output)
    details_button.click(get_product_details, inputs=product_id_input, outputs=product_details_output)
    recommend_button.click(recommend_items, inputs=recommend_id_input, outputs=recommend_output)
    cold_start_button.click(cold_start_recommend, inputs=keywords_input, outputs=cold_start_output)

demo.launch()
