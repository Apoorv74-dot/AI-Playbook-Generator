
import os
import base64
import requests
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from langchain_nomic.embeddings import NomicEmbeddings
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough


# Set up the Nomic Embedder for document embeddings
nomic_embedder = NomicEmbeddings(model="nomic-embed-text-v1.5", inference_mode="local")

import os
from langchain.schema import Document

# Path to the directory containing the YAML playbooks
playbook_directory = "playbooks/"

# List to store the Document objects
ansible_documents = []

# Loop through each file in the directory
for filename in os.listdir(playbook_directory):
    if filename.endswith(".yml") or filename.endswith(".yaml"):
        # Construct the full path to the file
        file_path = os.path.join(playbook_directory, filename)
        
        # Read the content of the YAML file
        with open(file_path, "r") as file:
            page_content = file.read()
        
        # Remove the '.yml' or '.yaml' extension for metadata
        metadata = {"purpose": os.path.splitext(filename)[0]}
        
        # Create a Document object and add it to the list
        ansible_documents.append(Document(page_content=page_content, metadata=metadata))

# Now, ansible_documents contains Document objects for each YAML file in the directory


# For training
vectorstore = Chroma.from_documents(
    ansible_documents,
    embedding=nomic_embedder,
    persist_directory="vector_store_file"
)

# For loading
from langchain_chroma import Chroma

vectorstore = Chroma(
    persist_directory="vector_store_file",
    embedding_function=nomic_embedder  # Ensure this is the same function used for embeddings originally
)

