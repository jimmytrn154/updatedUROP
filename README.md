
# KALM4Rec

**KALM4Rec** aims to tackle  the cold-start recommendation problem (where users lack historical data) by requiring only a few input keywords from users in a practical scenario of cold-start user restaurant recommendations. [[paper]](https://arxiv.org/pdf/2405.19612) 

![Picture](https://github.com/user-attachments/assets/2a0abebb-e43a-4816-8c26-be64a7071623)


## 🛍️ Keyword-driven Retrieval-Augmented Large Language Models for Cold-start User Recommendations

 Our framework is built upon two essential components centered around keywords: **candidates retrieval** focusing on retrieving relevant restaurants and **LLM-ranker** which leverages LLM to re-rank the retrieved candidates.
 
 ## 🚀 Quick Start
 **Installation**
 
  We recommend installing Gradio using pip, which is included by default in Python. Run this in your terminal or command prompt:
 
   ``` 
   pip install gradio numpy sentence-transformers tf-keras
   ```
Now, run your code. If you've written the Python code in a file named, for example [app.py] then you would run [python app.py] from the terminal.

**Core Structure**

**Keyword Processing**: The `extract_keywords` function simulates keyword extraction from user reviews.

**Retrieval Model**: The `retrieve_candidates` function uses embeddings to find similar restaurants based on keywords.

**KALM4REC**:
 - The `generate_prompt` function creates a prompt that includes user keywords and restaurant information.

 - The `llm_rerank` function simulates the re-ranking process using the generated prompt.


Some Note!!!
- Search: Allows users to search for products.
- Product Details: Displays details for a specific product based on its ID.
- Recommendations: Provides recommendations based on a product ID.
- Cold Start Recommendations: Offers recommendations for new users based on keywords.
