# generate_responses_api.py
import requests
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

def load_documents(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read().strip()
    return content.split("\n\n")  # Split by double newlines to separate documents

# Load documents and embeddings
documents_file = 'documents.txt'
embeddings_file = 'embeddings.npy'

documents = load_documents(documents_file)
embeddings = np.load(embeddings_file)

# Initialize the FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# Load the sentence transformer model for query embedding
model = SentenceTransformer('all-MiniLM-L6-v2')

def search_documents(query, top_k=5):
    query_embedding = model.encode(query)
    query_embedding = np.array(query_embedding).reshape(1, -1)  # Ensure 2D shape for FAISS
    distances, indices = index.search(query_embedding, top_k)
    return [(documents[i], distances[0][j]) for j, i in enumerate(indices[0])]

def generate_response_via_api(context, prompt, max_length=300):
    api_url = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
    
    # Hardcoded API token (ensure to keep it secure)
    api_token = "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"

    headers = {
        "Authorization": f"Bearer {api_token}"
    }
    payload = {
        "inputs": f"Context: {context}\nPrompt: {prompt}\nResponse:",
        "parameters": {"max_length": max_length, "num_return_sequences": 1}
    }
    
    response = requests.post(api_url, headers=headers, json=payload)

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Error: {response.status_code}, {response.text}")
        return "An error occurred."

    # Parse response data
    response_data = response.json()
    if isinstance(response_data, list) and len(response_data) > 0 and 'generated_text' in response_data[0]:
        return response_data[0]['generated_text']
    else:
        print("Unexpected response format:", response_data)
        return "An error occurred."

# Query to search
query = "what is Udesk?"

# Retrieve top 5 relevant documents
results = search_documents(query, top_k=5)
combined_context = "\n".join([doc for doc, _ in results])

print("Search Results:")
for doc, distance in results:
    print(f"Distance: {distance}\nDocument:\n{doc}\n")
print("-" * 80)

# Generate a response based on combined context of the top 5 documents
response = generate_response_via_api(combined_context, query)
print("Generated Response:")
print(response)
