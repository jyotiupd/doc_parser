## Modules ##
from langchain.schema import Document
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from config.get_config import llm,memory,azure_openai_embeddings
from utils.topic_generator import Topic_gen


class CreateVectors:
    def __init__(self,text_content,table_content):
        self.text_content = text_content
        self.table_content=table_content
        self.topic_gen = Topic_gen()
        self.vectorstore = Chroma(collection_name="utility_data", embedding_function=azure_openai_embeddings)
        self.splitter = RecursiveCharacterTextSplitter(separators=["page_number1","page_number2","page_number3","page_number4","page_number5",
                                                      "page_number6","page_number7","page_number8","page_number9","page_number10",
                                                      "page_number11","page_number12","page_number13","page_number14","page_number15",
                                                      "page_number16","page_number17","page_number18","page_number19","page_number20",
                                                      "page_number21","page_number22","page_number23","page_number24","page_number25",
                                                      "page_number26","page_number27","page_number28","page_number29","page_number30",
                                                      "page_number31","page_number32","page_number33","page_number34","page_number35",
                                                      "page_number36","page_number37","page_number38","page_number39","page_number40",
                                                      "page_number41","page_number42","page_number43","page_number44","page_number45",
                                                      "page_number46","page_number47","page_number48","page_number49","page_number50",
                                                      "page_number51","page_number52","page_number53","page_number54","page_number55",
                                                      "page_number56","page_number57","page_number58","page_number59","page_number60"
                                                      ])


    def text_splitter(self):
        type_text = self.splitter.split_text(self.text_content)
        type_table = self.splitter.split_text(self.table_content)
        text_doc = [
            Document(page_content=s, metadata={"page_number": s[0:s.find(":")],"topics":" ,".join(self.topic_gen.create_topic(s)[5:20])})
            for i, s in enumerate(type_text)
        ]

        table_doc = [
            Document(page_content=s, metadata={"page_number": s[0:s.find(":")],"topics":" ,".join(self.topic_gen.create_topic(s)[:10])})
            for i, s in enumerate(type_table)
        ]

        combined_doc = text_doc+table_doc
        return combined_doc
    
    def add_vectors(self):
        documents = self.text_splitter()
        self.vectorstore.add_documents(documents)
        return self.vectorstore


# vectorstore=Chroma.from_documents(combined_doc,azure_openai_embeddings,
#                            collection_name="utility_data",
#                            persist_directory="chroma_db",)
# vectorstore = Milvus.from_documents(
#     combined_doc,
#     azure_openai_embeddings,
#     connection_args={"uri": URI},
#     drop_old=True,
#     partition_key_field="page_number"
# )
