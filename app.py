import ollama
from dotenv import load_dotenv
from google import genai
import chromadb
import streamlit as st


# loading the env variable
load_dotenv()

# config
embed_model = "nomic-embed-text-v2-moe"
lll_model = "gemini-2.5-flash"
top_k = 4

# init clients
@st.cache_resource
def load_collection():
    chroma_client = chromadb.PersistentClient(path = './chroma_db')
    return chroma_client.get_or_create_collection(name = 'my_chunks')


@st.cache_resource
def load_gemini():
    return genai.Client()


collection = load_collection()
gemini_client = load_gemini()


# UI

st.title("DocGPT")
st.caption("Ask anything about your uploaded document.")
st.info(
    "This application is trained on curated Data Science notes by "
    "[Sanan Shaikh](https://github.com/shaikhsanan04), "
    "used as the primary knowledge base for retrieval."
)

question = st.text_area("Ask a question")

if question:
    with st.spinner("Thinking..."):
    
        response = ollama.embed(
            model = embed_model,
            input = [question]
        )
        
        question_vector = response["embeddings"][0]
        
        result = collection.query(
            query_embeddings = [question_vector],
            n_results = top_k,
            include = ["documents"]
        )
        
        retrieved_chunks = result["documents"][0]
        
                # Build prompt
        context = "\n\n".join(retrieved_chunks)
        prompt = f"""You are a helpful assistant. Use only the context below to answer the question.If the answer is not in the context, say "I don't know based on the document."
        Context:
        {context}

        Question: {question}

        Answer:"""
        
        # get answer from gemini
        
        llm_response = gemini_client.models.generate_content(
            model = lll_model,
            contents = prompt
        )
        
        st.markdown("### Answer")
        st.write(llm_response.text)
        
        with st.expander("See retrieved chunks:"):
            for i, chunk in enumerate(retrieved_chunks):
                st.markdown(f"** chunk {i+1} **")
                st.write(chunk)