import getpass
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain import hub
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts.chat import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.prompts import PromptTemplate

# Export these as global variables from command line or uncomment this code to be prompted for the values on startup
# os.environ["LANGCHAIN_API_KEY"] = getpass.getpass("Enter Langchain API Key:")
# os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter OpenAI API Key:")
os.environ["LANGCHAIN_TRACING_V2"] = "true"


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def get_instructions(product: str):   
    model = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)

    vectorstore = Chroma(persist_directory='embeddings', embedding_function=OpenAIEmbeddings())
    retriever = vectorstore.as_retriever()

# Instructions for the model about how to respond to the user's query
    prompt = ChatPromptTemplate(
        input_variables=['context', 'question'],
        messages=[HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                input_variables=['context', 'question'],
                template="You are an assistant for returning information about how to pack, organize, and label products according to the guidelines document that you have access to. The user will pass you a product name (for example, \'Shirts\') and you will respond with a list of steps that need to be followed to adhere to the rules relating to that product. You will only respond with the list of steps. Do not give any other context or dialogue other than the list of steps. Include as many steps as you can find relating to the product, in order of what page they are found on. Do not include steps that do not mention the product. Use the following pieces of retrieved context to answer the question. If there is no information related to the product that the user passes to, then say that you have no information on that product. \nQuestion: {question} \nContext: {context} \nAnswer:"
            )
        )]
    )
    
    rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
    )
    return rag_chain.invoke(product)