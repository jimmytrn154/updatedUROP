import gradio as gr
import random

# Simulated database of products
products = [
    {"id": 1, "name": "Spaghetti Carbonara", "category": "Italian"},
    {"id": 2, "name": "Sushi Platter", "category": "Japanese"},
    {"id": 3, "name": "Beef Burger", "category": "American"},
    {"id": 4, "name": "Pad Thai", "category": "Thai"},
    {"id": 5, "name": "Chicken Tikka Masala", "category": "Indian"}
]

def search_products(query):
    # Simple search function
    results = [p for p in products if query.lower() in p['name'].lower()]
    return "\n".join([f"{p['name']} - {p['category']}" for p in results])

def get_product_details(product_id):
    # Get details for a specific product
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        return f"Name: {product['name']}\nCategory: {product['category']}"
    return "Product not found"

def recommend_items(product_id):
    # Simple recommendation based on category
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        category = product['category']
        recommendations = [p for p in products if p['category'] == category and p['id'] != product_id]
        return "\n".join([p['name'] for p in recommendations])
    return "No recommendations available"

def cold_start_recommend(keywords):
    # Simple recommendation for new users based on keywords
    keyword_list = [k.strip().lower() for k in keywords.split(',')]
    recommendations = [p for p in products if any(k in p['name'].lower() or k in p['category'].lower() for k in keyword_list)]
    return "\n".join([p['name'] for p in recommendations])

# Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# Restaurant Recommendation System Demo")
    
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
        keywords_input = gr.Textbox(label="Enter keywords (comma-separated)")
        cold_start_output = gr.Textbox(label="Recommended Items")
        cold_start_button = gr.Button("Get Recommendations")

    search_button.click(search_products, inputs=search_input, outputs=search_output)
    details_button.click(get_product_details, inputs=product_id_input, outputs=product_details_output)
    recommend_button.click(recommend_items, inputs=recommend_id_input, outputs=recommend_output)
    cold_start_button.click(cold_start_recommend, inputs=keywords_input, outputs=cold_start_output)

demo.launch(share=True)