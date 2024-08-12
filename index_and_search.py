# index_and_search.py
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

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
    query_embedding = model.encode([query])
    distances, indices = index.search(np.array([query_embedding]), top_k)
    return [(documents[i], distances[0][j]) for j, i in enumerate(indices[0])]

# Test the search with a query
query = "How to use Zoom?"
results = search_documents(query)
print("Search Results:")
for doc, distance in results:
    print(f"Distance: {distance}\nDocument:\n{doc}\n")
