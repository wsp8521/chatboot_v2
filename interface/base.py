import os
import time
import queue
import streamlit as st
from langchain_groq import ChatGroq
from langchain_openai import  ChatOpenAI
import speech_recognition as sr
from interface.utils.audios import response_audio_openai
from chat.chatboot import ChatBoot

class InterfaceBase:
    def __init__(self, model_apenai:bool=True, model_groq:bool=True):
        self.openai_activate = model_apenai
        self.groq_activate = model_groq
        self.models =  {
                        'Groq':{'modelos':['llama-3.2-90b-vision-preview','llama-3.1-70b-versatile','gemma2-9b-it'],
                                'chat':ChatGroq, 'api':os.getenv('TOKEN_GROQ')},
                        'Openai':{'modelos':['gpt-4o-mini','gpt-3.5-turbo-0125', 'gpt-4o'],
                                  'chat': ChatOpenAI, 'api':os.getenv('TOKEN_OPENAI')}
                        }
        self.tab_conversa, self.tab_config = st.sidebar.tabs(["Conversa","Configuração"])  
        self.chatboot = ChatBoot(model=self._select_model())
     
       
     
         
     #conteúdos da sidebar
    def sidebar(self):
        # Controle de sessão para interromper o áudio ao atualizar a página
        if 'audio_playing' in st.session_state:
            st.session_state.audio_playing = False
   
        with self.tab_config:
            get_file = st.file_uploader("upload arquivo pdf", accept_multiple_files=True, type=['.pdf'])
            with st.spinner("processando documento"):
                self.chatboot.process_documents(get_file)
        with self.tab_conversa:
            st.session_state.audio_playing = st.checkbox("Ativar voz do chatboot")
            
 
     
    #historico de memoria        
    def _memory_history(self, question, container, memory):
        container = st.container()#criando container de conversa
        if question:
            chat = container.chat_message('human') 
            chat.markdown(question)
            chat = container.chat_message('ai')
            with st.spinner('Buscando informação. Aguarde!'):
                response_ia =  self.chatboot.chat_conversation(question)

            if st.session_state.audio_playing: 
                response_audio_openai(response_ia) #resposta em audio
                chat.markdown(response_ia) #resposta em texto
            else:
                 chat.markdown(response_ia)
        
            memory.chat_memory.add_user_message(question)
            memory.chat_memory.add_ai_message(response_ia)
            
    #seleção de modelo       
    def _select_model(self):
        model_apenai = self.openai_activate
        model_groq = self.groq_activate
        
        # Identificação dos provedores
        if model_apenai and not model_groq:
            provedor = [list(self.models.keys())[1]]  # Apenas os modelos da OpenAI
        elif not model_apenai and model_groq:
            provedor = [list(self.models.keys())[0]]  # Apenas os modelos da Groq
        else:
            provedor = list(self.models.keys())  # Ambos os modelos
        
        with  self.tab_config:
            st.header('🤖 Modelo de IA')
            # Interface do usuário
            descLabel_provedor = (
                'Selecione o provedor do modelo' if not model_apenai and not model_groq else ""
            )
            provedor_model = st.selectbox(descLabel_provedor, provedor)  # Agora `provedor` é sempre uma lista
            models = st.selectbox(
                'Selecione o modelo', 
                self.models[provedor_model]['modelos']
            )
        api = self.models[provedor_model]['api']
            
        # Inicialização do chat
        chat = self.models[provedor_model]['chat'](model=models, api_key=api)
        return chat
    
    