import os
from dotenv import load_dotenv
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai.chat_models import ChatOpenAI
from langchain.chains.retrieval_qa.base import RetrievalQA #classe que implementa uma cadeia (ou chain) de Perguntas e Respostas com Recuperação de Dados (Re
from langchain.prompts import PromptTemplate
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory  # Importando a memória
from langchain_groq import ChatGroq


#Classes que permitem configurar as respostas da llm em forma de streaming
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.base import BaseCallbackManager

load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv('TOKEN_OPENAI')
memory = ConversationBufferWindowMemory()
callback_manager = BaseCallbackManager([StreamingStdOutCallbackHandler()])  # Callback para streaming no terminal
#model = ChatOpenAI(streaming=True, callback_manager=callback_manager)

model = ChatGroq(model='llama-3.2-90b-vision-preview', api_key=os.getenv('TOKEN_GROQ'), streaming=True, callback_manager=callback_manager)
embeddings = OpenAIEmbeddings() #inicializando uma embedding
document_pdf = PyPDFLoader('apostila.pdf') #lendo documento
recursive_esplitter = RecursiveCharacterTextSplitter(chunk_size = 500,chunk_overlap = 100,)
chunk_documents = recursive_esplitter.split_documents(documents=document_pdf.load()) #quebrando o documento em chunkks

#CRIANDO VECTOR STORE

db = 'db_vector_store' #definindo o nome da base de dados

#criando o vector strore
vector_stores = Chroma.from_documents(
    documents=chunk_documents, #documento ja quebrado em chunks
    embedding= embeddings, #modelo responsavel pelo embedding
    persist_directory=db #base de dados onde será armazenados os vetores
)


#IMPORTANDO VECTO STORES
import_vector_stores = Chroma(
    embedding_function= embeddings, #modelo responsavel pelo embedding
    persist_directory=db #base de dados onde será armazenados os vetores
)

#CRIANDO PROMPT
prompt = PromptTemplate.from_template(
    '''Responda exclusivamente com base no contexto fornecido. 
            Não faça buscas externas, nem busque informações fora do contexto, incluindo a internet ou fontes externas.
            limite-se a responder apenas no que está no contexto. 
            Se uma pergunta se referir a algo que não está presente no contexto, informe que não há informações disponíveis para responder a essa questão.
            Não faça suposições e não forneça informações não mencionadas no contexto.
            Responda de maneira clara e objetiva.
            Contexto: {context}
            Pergunta:{question}
            
            
            '''
)


# #CRIANDO ESTRUTURA DE CHAT
chat = RetrievalQA.from_chain_type(
    llm = model,
    retriever = import_vector_stores.as_retriever(), #transforma o vector_stores em um retriever
    chain_type_kwargs={'prompt':prompt},

)

pergunta = "faça um resumo sobre o documento"

response = chat.invoke({'query':pergunta})
print(response.get('result'))
