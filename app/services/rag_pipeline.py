from sentence_transformers import SentenceTransformer
from transformers import pipeline
import faiss
import json

class RAGPipeline:
    def __init__(self):
        # Load retriever model and generator
        self.retriever_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.generator_model = pipeline("text2text-generation", model="t5-small")

        # Load data and create FAISS index
        self.documents, self.index = self.load_data()

    def load_data(self):
        with open("data/medical_data.json", "r") as f:
            documents = json.load(f)
        texts = [doc["content"] for doc in documents]
        embeddings = self.retriever_model.encode(texts)
        index = faiss.IndexFlatL2(embeddings.shape[1])
        index.add(embeddings)
        return documents, index

    def query(self, question):
        query_embedding = self.retriever_model.encode([question])
        _, indices = self.index.search(query_embedding, k=3)
        context = " ".join([self.documents[i]["content"] for i in indices[0]])
        input_text = f"question: {question} context: {context}"
        result = self.generator_model(input_text, max_length=50)
        return result[0]["generated_text"]