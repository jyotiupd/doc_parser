## Importing the essential libraries
import base64
import fitz
import re
import json
import os
from dotenv import load_dotenv
from langchain.memory import ConversationBufferWindowMemory,ChatMessageHistory
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.schema import Document
from langchain_openai import AzureChatOpenAI,AzureOpenAIEmbeddings
from langchain.vectorstores import AzureSearch
from langchain.text_splitter import RecursiveCharacterTextSplitter
from openai import AzureOpenAI
from io import BytesIO
from mimetypes import guess_type
_ = load_dotenv("./config/azure.env")

#print(os.getenv("AZURE_OPENAI_API_VERSION"))
LLM_Model = AzureChatOpenAI(temperature         = 0.3,
                            azure_deployment    = os.getenv("AZURE_DEPLOYMENT"),
                            api_version  = os.getenv("AZURE_OPENAI_API_VERSION"),
                            api_key             = os.getenv("AZURE_OPENAI_API_KEY"),
                            azure_endpoint      = os.getenv("AZURE_OPENAI_ENDPOINT")
                            )

ConvBuffMemory = ConversationBufferWindowMemory(k=10,memory_key="chat_history",\
                                input_key="query",chat_memory=ChatMessageHistory(messages=[]))

AzureOpenAI_Embeddings = AzureOpenAIEmbeddings(chunk_size=1,
                                   openai_api_version=os.getenv("EMBEDDINGS_API_VERSION"),
                                   azure_endpoint=os.getenv("EMBEDDINGS_ENDPOINT"),
                                   openai_api_key=os.getenv("EMBEDDINGS_API_KEY"),
                                   model=os.getenv("EMBEDDINGS_MODEL"),
                                   deployment=os.getenv("EMBEDDINGS_DEPLOYMENT")
                                   )


llm = LLM_Model
memory = ConvBuffMemory
azure_openai_embeddings = AzureOpenAI_Embeddings

search_index=AzureSearch(azure_search_endpoint = os.getenv('AZURE_COGNITIVE_SEARCH_SERVICE_NAME'),
                                    azure_search_key = os.getenv('AZURE_COGNITIVE_SEARCH_API_KEY'),
                                    index_name = "indi-test",
                                    embedding_function=azure_openai_embeddings.embed_query)