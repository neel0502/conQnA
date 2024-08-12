# generate_embeddings.py
from sentence_transformers import SentenceTransformer
import numpy as np

def load_documents(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read().strip()
    return content.split("\n\n")  # Split by double newlines to separate documents

# Load documents
input_file = 'documents.txt'
documents = load_documents(input_file)

# Load a pre-trained sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Generate embeddings for each document
embeddings = model.encode(documents)

# Save embeddings to a numpy file
output_file = 'embeddings.npy'
np.save(output_file, embeddings)
print(f"Embeddings saved to {output_file}")
