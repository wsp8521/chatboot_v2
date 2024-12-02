import os
import tempfile
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


#Classes que permitem configurar as respostas da llm em forma de streaming
from langchain.callbacks.base import BaseCallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler



os.environ['OPENAI_API_KEY'] = os.getenv('TOKEN_OPENAI')

class ChatBoot:
    def __init__(self, model):
        self.temp_file_path = None
        self.vector_store_db_name = 'db'
        self.model = model,
        self.memory = ConversationBufferMemory(return_messages=True, memory_key='history', output_key='result')
        
     #método chat   
    def chat_conversation(self, question):
        vector_store = self.load_vector_store()
        callback_manager = BaseCallbackManager([StreamingStdOutCallbackHandler()])  # Callback para streaming no terminal
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
       
       
        model = ChatGroq(model='llama-3.2-90b-vision-preview', api_key=os.getenv('TOKEN_GROQ'), streaming=True, callback_manager=callback_manager)
        chat = RetrievalQA.from_chain_type(
            llm = model,
            memory = self.memory,
            retriever = vector_store.as_retriever(), #transforma o vector_stores em um retriever
            chain_type_kwargs={'prompt':prompt},

        )
        response = chat.invoke({'query':question})
        return response.get('result')
    
    
    #memoria do chat
    def memory_chat(self):
        return self.memory

    #lendo vector_store existente
    def load_vector_store(self):
        if os.path.exists(self.vector_store_db_name):
            
            # Conecta ao Chroma se houver um db vector store
            vector_store = Chroma(
                persist_directory=self.vector_store_db_name,
                embedding_function=OpenAIEmbeddings()
            )
            return vector_store
        return None

    #processamento de documentos
    def process_documents(self, documents):
        all_chunks = [] #inicializando lista de armazenamento dos chunks

        if documents:
            for document in documents: #percorrendo as lista de documentos
                chunks = self.__chunk(document)
                all_chunks.extend(chunks) #salvando lista de chunkd
        
                # Remove o arquivo temporário
                if self.temp_file_path and os.path.exists(self.temp_file_path): #verifica se o arquivo existe na pasta
                    os.remove(self.temp_file_path) #remove os arquvicos
                    self.__create_vector_store(chunks=all_chunks)     
            return None
        
                    
    #PROCESSOS DE RAGS
        
    #lendo arquivo    
    def __load_file(self, file):    
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file: #criando arquivo temporário e salvando no disco
            temp_file.write(file.read()) #Escreve os dados binários lidos do arquivo enviado (file.read()) em um arquivo temporário (temp_file).
            self.temp_file_path =  temp_file.name #armazenando o caminho do arquivo
        load_doc = PyPDFLoader(self.temp_file_path)   #carregando arquivo   
        read_doc = load_doc.load() #lendo os arquivos            
        return read_doc
                
    
    #transformando arquvios em chunks
    def __chunk(self, file):
        doc = self.__load_file(file)
        
         #quebrando documento em chunks
        splitter_doc = RecursiveCharacterTextSplitter(
            chunk_size=2000, 
            chunk_overlap=200,
            separators=["\n\n", "\n","."," ",""]
            
            )
        chunk = splitter_doc.split_documents(doc) #gerando chunks
        return chunk #retorna os chunks
    

    def __create_vector_store(self, chunks):
        vector_store = self.load_vector_store()
        if vector_store:
            vector_store.add_documents(chunks) #adiciona novos chunks de já existir um vector_sotre
        else:
           vector_store = Chroma.from_documents( #criando vector_store
               documents=chunks,
               embedding=OpenAIEmbeddings(),
               persist_directory=self.vector_store_db_name   
           ) 
        
        return None
            