import os
import streamlit as st
from chat.chatboot import ChatBoot
from langchain_openai import  ChatOpenAI
from langchain_groq import ChatGroq


class ChatbootInterface:
    def __init__(self, model_apenai:bool=True, model_groq:bool=True):
        self.openai_activate = model_apenai
        self.groq_activate = model_groq
        self.chatboot = ChatBoot(model="llama-3.2-90b-vision-preview")
        self.models =  {
                        'Groq':{'modelos':['llama-3.2-90b-vision-preview','llama-3.1-70b-versatile','gemma2-9b-it'],
                                'chat':'ChatGroq', 'api':os.getenv('TOKEN_GROQ')},
                        'Openai':{'modelos':['gpt-4o-mini','gpt-3.5-turbo-0125', 'gpt-4o'],
                                  'chat': 'ChatOpenAI', 'api':os.getenv('TOKEN_OPENAI')}
                        }
        self.__select_model()
 
     #conteúdos da sidebar
    def sidebar(self):
        with st.sidebar:
           get_file = st.file_uploader("upload arquivo pdf", accept_multiple_files=True, type=['.pdf'])

        with st.spinner("processando documento"):
           self.chatboot.process_documents(get_file)
           
                 
    #seleção de modelo       
    def __select_model(self):
        st.sidebar.header('🤖 Modelo de IA')
        model_apenai = self.openai_activate
        model_groq = self.groq_activate
        
         #identificação dos rovedores
        if model_apenai and model_groq==False:
           provedor =  list(self.models.keys())[1] #exibe apenas os modelos da openais
        elif model_apenai==False and model_groq:
            provedor =  list(self.models.keys())[0] #exibe apenas os modelos da Groq
        else:
            provedor = self.models.keys() #exibe os dois modelos
            
            
        descLabel_provedor = 'selecione o provedor do modelo' if model_apenai==False and model_groq==False else ""
        provedor_model = st.sidebar.selectbox(descLabel_provedor, provedor)
        models = st.sidebar.selectbox('selecione o modelo', self.models[provedor_model]['modelos']),
        api = self.models[provedor_model]['api']
        
        chat = self.models[provedor]['chat'](model = models, api_key = api)
        #return chat
        

    #área do chat    
    def chat_window(self):
        st.header('🚢 Chat Porto Itaqui', divider=True)
        vector_store = self.chatboot.load_vector_store()
                
        if vector_store is None: #verifica se ha banco de dados
            st.warning("Faça o upload de um PDF para começar.")
        
         #criando uma sessão de memória
        if 'memory' not in st.session_state: #verifica se há uma sessáo chamda memoria
             st.session_state['memory'] = self.chatboot.memory_chat() ##armzenando memoria na sessão
             
        memory =  st.session_state['memory'] 
        mensagens = memory.load_memory_variables({})['history'] #lendo as mensagens da 
        container = st.container()#criando container de conversa
        
        for mensagem in mensagens:#percorrendo todas as mensatens
            chat = container.chat_message(mensagem.type)
            chat.markdown(mensagem.content) #exibindo as mensaaens
                 
        question = st.chat_input("Como posso ajudar você")
        
        if question:
            chat = container.chat_message('human') 
            chat.markdown(question)
            chat = container.chat_message('ai')
            with st.spinner('Buscando informação. Aguarde!'):
                response_ia = self.chatboot.chat_conversation(question)
            chat.markdown(response_ia)
            memory.chat_memory.add_user_message(question)
            memory.chat_memory.add_ai_message(response_ia)
         
            
