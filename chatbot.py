# product_bot.py
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA

# Load .env
load_dotenv()

# Load embeddings + FAISS index
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
vectorstore = FAISS.load_local(
    "faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)

# LLM (chat model)
llm = ChatGoogleGenerativeAI(model="models/gemini-1.5-flash")  # or use gemini-pro if enabled

# Prompt to limit hallucination<
prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=(
        "You are a helpful assistant that answers ONLY from the context below.\n"
        "If the answer is not in the context, say:\n"
        "'Sorry, I don't have that information. Please check with the admin.'\n\n"
        "Context:\n{context}\n\nQuestion: {question}\nAnswer:"
    ),
)

# RetrievalQA Chain
qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
    return_source_documents=True,
    chain_type_kwargs={"prompt": prompt},
)

# Chat function
# Chat function
def ask_product_bot(question: str) -> str:
    # Handle greetings manually
    greetings = ["hello", "hi", "hey", "salam", "bonjour","coucou"]
    if question.lower().strip() in greetings:
        return "Hi, how can I help you?"

    # Use LangChain QA for other queries
    result = qa.invoke(question)
    answer = result["result"]
    docs = result["source_documents"]

    if not docs or "i don't know" in answer.lower():
        return "Sorry, I don't have that information. Please check with the admin."
    
    return answer


# CLI
if __name__ == "__main__":
    print("🛍️  Ask me about the PJ set! (type 'exit' to quit)\n")
    while True:
        q = input("You: ")
        if q.lower() in {"exit", "quit"}:
            break
        print("Bot:", ask_product_bot(q))
