import faiss
import numpy as np
from coeai import LLMinfer
from knowledge_base import knowledge_documents

llm = LLMinfer(api_key="YOUR_API_KEY")

index = None
documents = []


def build_index():

    global index, documents

    vectors = []

    for doc in knowledge_documents:

        text = doc["command"] + " " + doc["description"]

        response = llm.generate(
            model="bge-m3:567m",
            prompt=text,
            max_tokens=10
        )

        embedding = np.random.rand(768)

        vectors.append(embedding)
        documents.append(doc)

    vectors = np.array(vectors).astype("float32")

    dimension = vectors.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(vectors)


def search(query):

    response = llm.generate(
        model="bge-m3:567m",
        prompt=query,
        max_tokens=10
    )

    query_vector = np.random.rand(768).astype("float32")

    D, I = index.search(np.array([query_vector]), k=1)

    return documents[I[0][0]]

