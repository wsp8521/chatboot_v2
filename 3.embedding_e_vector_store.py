import os
from dotenv import load_dotenv
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv('TOKEN_OPENAI')



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


#REALIZANDO O RETRIVEL
pergunta =  "o que é a LDB?"

response = import_vector_stores.similarity_search(pergunta)

print(response)



