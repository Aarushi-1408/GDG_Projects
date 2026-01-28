from openai import embeddings
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class NewsVectorStore:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = faiss.IndexFlatL2(384)
        self.documents = []

    '''def add_documents(self, texts):
        embeddings = self.model.encode(texts)
        self.index.add(np.array(embeddings).astype("float32"))
        self.documents.extend(texts)
    '''
    def add_documents(self, texts):
        # Ensure texts is always a list
        if isinstance(texts, str):
            texts = [texts]

        embeddings = self.model.encode(texts)
        embeddings = np.array(embeddings).astype("float32")
        self.index.add(embeddings)
        self.documents.extend(texts)

    def search(self, query, k=3):
        query_emb = self.model.encode([query])
        distances, indices = self.index.search(
            np.array(query_emb).astype("float32"), k
        )
        return [self.documents[i] for i in indices[0]]
