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
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
import streamlit as st


# Load environment variables from .env file
load_dotenv()

# Set up environment variables
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
app_key = os.getenv("CISCO_OPENAI_APP_KEY")
cisco_idp = os.getenv("TOKEN_URL")
api_version = os.getenv("API_VERSION")
azure_endpoint = os.getenv("AZURE_ENDPOINT")
model_name = os.getenv("DEPLOYMENT_NAME")

# Set up the Nomic Embedder for document embeddings
nomic_embedder = NomicEmbeddings(model="nomic-embed-text-v1.5", inference_mode="local")

# For loading
from langchain_chroma import Chroma

vectorstore = Chroma(
    persist_directory="vector_store_file",
    embedding_function=nomic_embedder  # Ensure this is the same function used for embeddings originally
)


# Set up a retriever for similarity search
ansible_retriever = vectorstore.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={"k": 3, "score_threshold": 0.4},
)


# Function to get the auth token from Cisco IDP
def get_auth_token():
    payload = "grant_type=client_credentials"
    value = base64.b64encode(f'{client_id}:{client_secret}'.encode('utf-8')).decode('utf-8')
    headers = {
        "Accept": "*/*",
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {value}"
    }
    token_response = requests.request("POST", cisco_idp, headers=headers, data=payload)
    return token_response.json()["access_token"]

# Set up the LLM (Azure OpenAI)
token = get_auth_token()
llm = AzureChatOpenAI(
    deployment_name=model_name,
    azure_endpoint=azure_endpoint,
    api_key=token,
    api_version=api_version,
    model_kwargs=dict(user=f'{{"appkey": "{app_key}"}}')
)




st.title("Next GenAI Playbook Generator")

if "messages" not in st.session_state:
    st.session_state.messages = [
        SystemMessage(content="You are a helpful assistant. Answer all questions to the best of your ability."),
    ]

from langchain.prompts import ChatPromptTemplate


for message in st.session_state.messages:
    if isinstance(message, HumanMessage):
        st.chat_message("human").write(message.content)
    elif isinstance(message, AIMessage):
        st.chat_message("assistant").write(message.content)



def update_conversation_history_string(conversation_history_string ,user_message, bot_response):
    # Prepend the bot response and user message to the conversation string
    conversation_history_string = f"User: {user_message}\nBot: {bot_response}\n {conversation_history_string}"
    return conversation_history_string

text = st.chat_input(
    "I am an Helpful Assitant. Ask me anything...",
)


if text:
    st.session_state.messages.append(HumanMessage(content=text))
    st.chat_message("human").write(text)
    with st.chat_message("assistant"):

        playbook_message = """
        Based on the given context, create an Ansible playbook for the following request:

        {question}

        Context:
        {context}
        """
        playbook_prompt = ChatPromptTemplate.from_messages([("human", playbook_message)])

        ansible_rag_chain = {"context": ansible_retriever,  "question": RunnablePassthrough()} | playbook_prompt | llm


        # Retrieve the last AI response
        last_ai_response = ""
        for message in reversed(st.session_state.messages):
            if isinstance(message, AIMessage):
                last_ai_response = message.content
                break

        # Display the last AI response
        text_for_prompt= text + "\n Previous Conversation History"+ last_ai_response
        print('____________________0000000000_')
        print(last_ai_response)
        print('__________________________')
        # Test the RAG chain with a sample question
        response = ansible_rag_chain.invoke(text_for_prompt)

        # Check if the response is generic or doesn't contain relevant info
        if "specific context" in response.content.lower() or "basic structure" in response.content.lower():
            print("HELLOOO")
            
            response.content = "Sorry, I couldn't find any relevant information regarding your request. Please provide more specific details."
        
        st.write(response.content)
        print(st.session_state.messages)
        st.session_state.messages.append(AIMessage(content=response.content))
    

