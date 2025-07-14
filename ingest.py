import json
import os
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore


load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

with open("Nugget_restaurant_menu.json", "r", encoding="utf-8") as f:
    docs_json = json.load(f)

docs = [
    Document(page_content=doc["page_content"], metadata=doc["metadata"])
    for doc in docs_json
]

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2",
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': False}
)

index_name = "zomato-chatbot"

vectorstore = PineconeVectorStore(
    index_name=index_name,
    embedding=embedding_model,
    pinecone_api_key = PINECONE_API_KEY
)

batch_size = 10  
for i in range(0, len(docs), batch_size):
    batch = docs[i:i+batch_size]
    vectorstore.add_documents(batch)
    print(f"Uploaded batch {i//batch_size + 1}")