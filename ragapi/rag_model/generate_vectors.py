import math
from langchain.docstore.document import Document
from rag_model.parse_xml import text_list
# from parse_xml import text_list

from langchain_huggingface import HuggingFaceEmbeddings

import torch
import faiss
import numpy as np
from langchain.schema import Document

# Create document objects
docs = [Document(page_content=text, metadata={"source": "local"}) for text in text_list] #TODO: Change "local" to actual source of respective text
print(f"Number of documents: {len(docs)}")

def create_faiss_vectorstore(docs, embeddings):
    """
    Create a FAISS vector store from the given documents and embeddings.

    Args:
        docs (list of str): The documents to index.
        embeddings (HuggingFaceEmbeddings): The HuggingFace embeddings model.
        use_gpu (bool): Whether to use GPU if available.

    Returns:
        faiss.Index: The FAISS index.
        list of str: The original documents for reference.
    """
    # Check for GPU availability
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")

    # Extract page content from Document objects
    doc_texts = [doc.page_content for doc in docs]

    # Generate embeddings for all documents using embed_documents
    doc_embeddings = np.array(embeddings.embed_documents(doc_texts))

    # Initialize FAISS index
    embedding_dim = doc_embeddings.shape[1]  # Dimension of the embeddings
    index = faiss.IndexFlatL2(embedding_dim)  # L2 distance (Euclidean)

    # Add document embeddings to the FAISS index
    index.add(doc_embeddings)

    print(f"FAISS index created with {len(docs)} documents.")
    return index, doc_texts





# Define the total limit for chunks
TOTAL_CHUNKS_LIMIT = 9999


# Calculate the maximum number of chunks per document
max_chunks_per_doc = TOTAL_CHUNKS_LIMIT // len(docs)

# Function to chunk a document into smaller parts
def chunk_document(doc, max_chunks):
    chunk_size = max(1, math.ceil(len(doc) / max_chunks))
    return [doc[i:i+chunk_size] for i in range(0, len(doc), chunk_size)]

# Process the documents into chunks
chunked = []
for doc in docs:
    chunked.extend(chunk_document(doc.page_content, max_chunks_per_doc))

# Check the total number of chunks
total_chunks = len(chunked)
print(f"Total number of chunks: {total_chunks}")

# Ensure the total number of chunks does not exceed the limit
assert total_chunks <= TOTAL_CHUNKS_LIMIT, "Total number of chunks exceeds the limit"


embedding_model = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

# # Create the FAISS vector store
vectorstore, doc_texts = create_faiss_vectorstore(docs, embedding_model)