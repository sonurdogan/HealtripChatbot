from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=500)
    chunks = text_splitter.split_text(text)
    return chunks

def create_vector_store(vector_db_name):
    # pdf_docs = PyPDFLoader(f"/Users/onurdogan/Desktop/{vector_db_name}.pdf")
    # pages = pdf_docs.load_and_split()
    # raw_text = "\n\n".join(str(p.page_content) for p in pages)

    from update_db import update_vector_db
    update_vector_db()

    with open(f"./sources/{vector_db_name}.txt", "r") as file:
        raw_text = file.read()

    try:
        os.rmdir(f"./{vector_db_name}")
    except:
        pass

    text_chunks = get_text_chunks(raw_text)
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local(vector_db_name)

def get_conversational_chain():
    prompt_template = """
    You are the Health Tourism Planner assistant.
    Your task is to answer common questions on Hospitals, Doctors and Hotels nearby Hospitals.
    Please provide short and clear answers based on only the provided context. If you don't know the answer, say 'I am not conversational chatbot, Can you please ask question again with more detail or contact us via e-mail at healtrip.codewizards@gmail.com'.

    Context:
    {context}

    Question:
    {question}

    Your answer:
    """

    model = ChatGoogleGenerativeAI(model="gemini-pro",
                                   temperature=0.4)

    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    return chain

def start_vector_store(vector_db_name):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_db = FAISS.load_local(vector_db_name, embeddings, allow_dangerous_deserialization=True)
    return vector_db

def run_healtrip_chatbot(user_question, vector_store):

    docs = vector_store.similarity_search(user_question)
    chain = get_conversational_chain()

    response = chain(
        {"input_documents": docs, "question": user_question}
        , return_only_outputs=True)

    return response["output_text"]


