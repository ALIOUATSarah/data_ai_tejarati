from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

docs = [
    """
    
    Product name: Comfy Linen PJ Set
    Product type: Pajama set (PJ)
    Pieces included: short, pant, and shirt (3 pieces total)
    Material: high-quality, comfortable linen
    Price: 4 500 DZD
    """
]

vectorstore = FAISS.from_texts(docs, embeddings)
vectorstore.save_local("faiss_index")
print("✅ FAISS index saved.")
