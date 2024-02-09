import streamlit as st
from langchain.llms import Ollama
import os
import chromadb
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from chromadb.config import Settings

from langchain.vectorstores import Chroma
from langchain.llms import Ollama
from langchain.callbacks.base import BaseCallbackHandler

# Custom streamlit handler to display LLM outputs in stream mode
class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text=initial_text
    def on_llm_new_token(self, token: str, **kwargs) -> None:

        self.text+=token+"" 
        self.container.markdown(self.text)

# streamlit UI configuration
def setup_page():
    st.set_page_config(layout="wide")
    st.markdown("<h2 style='text-align: center; color: white;'>Your Personal MBA </h2>" , unsafe_allow_html=True)
    url = 'https://personalmba.com/'
    col1, col2, col3= st.columns(3)
    with col2:
        st.markdown("""
            <div style="text-align: center;">
            <h5 style='color: white;'>Inspired by </h5>
            <a href="%s">The Personal MBA by Josh Kaufman</a>  
            </div>
            """ % url, unsafe_allow_html=True)
    st.divider()

# get necessary environment variables for later use
def get_environment_variables():
    model = os.environ.get("MODEL", "mistral")
    embeddings_model_name = os.environ.get("EMBEDDINGS_MODEL_NAME", "all-MiniLM-L6-v2")
    persist_directory = os.environ.get("PERSIST_DIRECTORY", "db")
    target_source_chunks = int(os.environ.get('TARGET_SOURCE_CHUNKS', 4))
    return model, embeddings_model_name, persist_directory, target_source_chunks

# create knowledge base retriever
def create_knowledge_base(embeddings_model_name, persist_directory, target_source_chunks):
    embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)
    db = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
    retriever = db.as_retriever(search_kwargs={"k": target_source_chunks})
    return retriever

# handle query when user hit 'enter' on a question
def handle_query(query, model, retriever):
    with st.chat_message('assistant'):

        with st.spinner("Generating answer..."):
            message_placeholder = st.empty()
            stream_handler = StreamHandler(message_placeholder)  
            llm = Ollama(model=model, callbacks=[stream_handler])
            qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=False)
            res = qa(query)
            answer = res['result']
            message_placeholder.markdown(answer)
            return answer

# dictionary to store the previous messages, create a 'memory' for the LLM
def initialize_session():
    if 'messages' not in st.session_state:
        st.session_state.messages = []

# display the messages
def display_messages():
    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.markdown(message['content'])

# example questions when user first load up the app. Will disappear after user send the first query
def show_examples():
    examples = st.empty()
    with examples.container():
        with st.chat_message('assistant'):
            st.markdown('Example questions:')
            st.markdown(' - How do I know that I am making the right decisions?')
            st.markdown(' - What are the key ideas in Chapter 6 "The Human Mind"?')
            st.markdown(' - What are common traits shared by the most sucessful individuals in the world?')
            st.markdown(' - I want to be a millionaire, build me a 5 year roadmap based on the top 0.01 percent of the human population.')
            st.markdown('So, how may I help you today?')
    return examples

    
def main():
    setup_page()
    initialize_session()
    display_messages()
    examples = show_examples()
    model, embeddings_model_name, persist_directory, target_source_chunks = get_environment_variables()
    retriever = create_knowledge_base(embeddings_model_name, persist_directory, target_source_chunks)
    
    query = st.chat_input(placeholder='Ask a question...')  # starting with empty query

    if query:   # if user input a query and hit 'Enter'
        examples.empty()

        st.session_state.messages.append({  # add the query into session state/ dictionary
            'role': 'user', 
            'content': query
        })

        with st.chat_message('user'):
            st.markdown(query)

        answer = handle_query(query, model, retriever)

        st.session_state.messages.append({  # add the answer into session state/ dictionary
             'role': 'assistant',
             'content': answer  
        })

if __name__ == "__main__":
    main()
