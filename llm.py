import streamlit as st
# On crée une instance LLM de la classe ChatOpenAI, l'instance est initialisée grâce à la clée de l'API d'OpenAI et du modèle stcokés dans le fichier secrets.toml
# Create the LLM
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

llm = ChatOpenAI(
    openai_api_key=st.secrets["OPENAI_API_KEY"],
    model=st.secrets["OPENAI_MODEL"],
    max_tokens = 100
)

# Create the Embedding model

embeddings = OpenAIEmbeddings(
    openai_api_key=st.secrets["OPENAI_API_KEY"]
)