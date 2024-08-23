
# KALM4Rec

**KALM4Rec** aims to tackle  the cold-start recommendation problem (where users lack historical data) by requiring only a few input keywords from users in a practical scenario of cold-start user restaurant recommendations. [[paper]](https://arxiv.org/pdf/2405.19612) 

## 🛍️ Keyword-driven Retrieval-Augmented Large Language Models for Cold-start User Recommendations

 Our framework is built upon two essential components centered around keywords: **candidates retrieval** focusing on retrieving relevant restaurants and **LLM-ranker** which leverages LLM to re-rank the retrieved candidates.
 
 ## 🚀 Quick Start
 **Installation**
 
    We recommend installing Gradio using pip, which is included by default in Python. Run this in your terminal or command prompt:
   
   ```bash
   pip install gradio
   ```
Now, run your code. If you've written the Python code in a file named, for example [app.py] then you would run [python app.py] from the terminal.

**Core Structure**

**Candidate Retrieval**: We use sentence embeddings to compute similarity between the query and products. The `candidates_retrieval` function returns the top-k most similar products.

**LLM Ranker**: The `llm_ranker` function simulates an LLM-based ranking system. In a real-world scenario, we will replace this with an actual call to an **LLM API** for more sophisticated ranking.

**Enhanced Search**: The `search_and_rank` function combines candidate retrieval and LLM ranking to provide more relevant results.


Some Note!!!
- Search: Allows users to search for products.
- Product Details: Displays details for a specific product based on its ID.
- Recommendations: Provides recommendations based on a product ID.
- Cold Start Recommendations: Offers recommendations for new users based on keywords.
