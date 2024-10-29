from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from config.get_config import llm,memory
from utils.prompt_config import answer_prompt
from utils.vector_store import CreateVectors


class LLM_response:
    def __init__(self,text_content,table_content,query):
        create_vector = CreateVectors(text_content,table_content)
        self.vectorstore = create_vector.add_vectors()
        self.query = query
        self.llm = llm
        self.memory = memory
        self.llm_chain = ""

    def gen_context(self,top_k=15):
        base_retriever=self.vectorstore.as_retriever(search_type="mmr",search_kwargs=dict(k=top_k))
        context=base_retriever.get_relevant_documents(self.query)
        return context
    
    def gen_response(self):
        self.answer_prompt = PromptTemplate(template=answer_prompt,
                                               input_variables=["context", "query", "chat_history"])
        self.llm_chain = (
                {
                    "context": RunnablePassthrough(),
                    "chat_history": RunnablePassthrough(),
                    "query": RunnablePassthrough(),
                }
                | self.answer_prompt
                | llm
                | StrOutputParser()
        )
        self.context = self.gen_context()

        res= self.llm_chain.invoke({"context": self.context, "question": self.query ,
                         "chat_history": self.memory.chat_memory.messages}) 
        return res
