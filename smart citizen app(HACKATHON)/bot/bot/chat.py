import os
import streamlit as st
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import WebBaseLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts.chat import (ChatPromptTemplate,
                                    HumanMessagePromptTemplate,
                                    SystemMessagePromptTemplate)
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma

# Load environment variables from .env file (Optional)
load_dotenv()

OPENAI_API_KEY = os.getenv("")

system_template = """Use the following pieces of context to answer the users question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
"""

messages = [
    SystemMessagePromptTemplate.from_template(system_template),
    HumanMessagePromptTemplate.from_template("{question}"),
]
prompt = ChatPromptTemplate.from_messages(messages)
chain_type_kwargs = {"prompt": prompt}

# Dictionary mapping categories to URLs
categories_urls = {
    "Home": "https://coimbatore.nic.in/about-district/",
    "Department": "https://coimbatore.nic.in/about-district/whos-who/",
    "Tourist Place": "https://coimbatore.nic.in/tourism/",
    "Helpline Number": "https://coimbatore.nic.in/helpline/"
}

def main():
    # Set the title and subtitle of the app
    st.title('Chat-Bot')

    # Select box for categories
    selected_category = st.selectbox("Select a category", list(categories_urls.keys()))

    # Get the URL based on the selected category
    url = categories_urls[selected_category]

    prompt = st.text_input("Ask a question (query/prompt)")
    if st.button("Submit Query", type="primary"):
        ABS_PATH: str = os.path.dirname(os.path.abspath(__file__))
        DB_DIR: str = os.path.join(ABS_PATH, "db")

        # Load data from the specified URL
        loader = WebBaseLoader(url)
        data = loader.load()

        # Split the loaded data
        text_splitter = CharacterTextSplitter(separator='\n', 
                                        chunk_size=4000, 
                                        chunk_overlap=40)

        docs = text_splitter.split_documents(data)

        # Create OpenAI embeddings
        openai_embeddings = OpenAIEmbeddings()

        # Create a Chroma vector database from the documents
        vectordb = Chroma.from_documents(documents=docs, 
                                        embedding=openai_embeddings,
                                        persist_directory=DB_DIR)

        vectordb.persist()

        # Create a retriever from the Chroma vector database
        retriever = vectordb.as_retriever(search_kwargs={"k": 3})

        # Use a ChatOpenAI model
        llm = ChatOpenAI(model_name='gpt-3.5-turbo')

        qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

        response = qa(prompt)
        st.write(response)

if __name__ == '__main__':
    main()