import os
from dotenv import load_dotenv

from langchain_pinecone import PineconeVectorStore
from langchain_mistralai.chat_models import ChatMistralAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.embeddings import HuggingFaceEmbeddings

# loading the important things like api keys and index on pinecone
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

def get_retrieval_chain():
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': False}
    )

    vectorstore = PineconeVectorStore(
        index_name=INDEX_NAME,
        embedding=embedding_model,
        pinecone_api_key=PINECONE_API_KEY
    )
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 100})

    model = ChatMistralAI(mistral_api_key=MISTRAL_API_KEY)
    
    prompt = ChatPromptTemplate.from_template(
    """
You are a FOOD/RESTAURANT assistant EXCLUSIVELY for Ghaziabad. Follow these rules:

1. **STRICT DOMAIN RESTRICTIONS**:
   - ONLY answer questions about FOOD, DISHES, RESTAURANT MENUS, or RESTAURANTS IN Ghaziabad
   - REFUSE ALL OTHER QUESTIONS (geography/history/general knowledge/other cities)

2. **CONTEXT RULES**:
   - Use ONLY information from <context> below
   - NEVER use external knowledge or training data
   - If answer isn't in context: "I don't know based on provided information"

3. **RESPONSE FORMAT**:
   - For non-Ghaziabad/non-food questions: ONLY reply "I only answer food/restaurant questions about Ghaziabad"
   - NO explanations, apologies, or additional text - just the refusal phrase

<context>
{context}
</context>

Current date: {current_date}

Question: {input}
Answer:
"""
)

       
    document_chain = create_stuff_documents_chain(model, prompt)
    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    return retrieval_chain