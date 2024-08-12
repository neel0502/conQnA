# app.py
import streamlit as st
import requests
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

# Load documents and embeddings
documents_file = 'documents.txt'
embeddings_file = 'embeddings.npy'

def load_documents(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read().strip()
    return content.split("\n\n")  # Split by double newlines to separate documents

def search_documents(query, top_k=5):
    query_embedding = model.encode(query)
    query_embedding = np.array(query_embedding).reshape(1, -1)
    distances, indices = index.search(query_embedding, top_k)
    return [(documents[i], distances[0][j]) for j, i in enumerate(indices[0])]

def generate_response_via_api(context, prompt, max_length=300):
    api_url = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
    api_token = "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"

    headers = {
        "Authorization": f"Bearer {api_token}"
    }
    # Create a refined context to send to the model
    refined_context = f"Document excerpt:\n{context}\n\nQuestion: {prompt}\nAnswer:"

    payload = {
        "inputs": refined_context,
        "parameters": {"max_length": max_length, "num_return_sequences": 1}
    }

    response = requests.post(api_url, headers=headers, json=payload)
    
    if response.status_code != 200:
        return "An error occurred."

    response_data = response.json()
    if isinstance(response_data, list) and len(response_data) > 0 and 'generated_text' in response_data[0]:
        return response_data[0]['generated_text'].split("Answer:")[-1].strip()
    else:
        return "An error occurred."

# Initialize the FAISS index and models
documents = load_documents(documents_file)
embeddings = np.load(embeddings_file)
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# Load the sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Streamlit app layout
st.title("Confluence Q&A with Zephyr")

query = st.text_input("Enter your question:")

if st.button("Get Response"):
    # Retrieve top 5 relevant documents
    results = search_documents(query, top_k=5)
    combined_context = "\n".join([doc for doc, _ in results])

    # Generate a response based on the combined context of the top 5 documents
    response = generate_response_via_api(combined_context, query)
    
    st.write("Generated Response:")
    st.write(response)
