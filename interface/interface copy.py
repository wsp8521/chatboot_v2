import streamlit as st
from chat.chatboot import ChatBoot
from langchain.memory import ConversationBufferWindowMemory


class ChatbootInterface:
    def __init__(self):
        self.chatboot = ChatBoot("llama-3.2-90b-vision-preview")
    
        
    
    def config_page(self, page_title, page_icon=None ):
        st.set_page_config(page_title=page_title, page_icon=page_icon)
        

    def sidebar(self):
        with st.sidebar:
           get_file = st.file_uploader("upload arquivo pdf", accept_multiple_files=True, type=['.pdf'])
           
        with st.spinner("processando documento"):
           self.chatboot.process_documents(get_file)

        
    def chat_window(self):
        st.header('🤖 Chat Port', divider=True)
        #st.session_state['memory'] = self.chatboot.memory_chat() #armzenando memoria na sessão
        vector_store = self.chatboot.load_vector_store()
                
        if vector_store is None:
            st.warning("Faça o upload de um PDF para começar.")
            st.stop()
        
        # chain = st.session_state['chain']
        # memory = chain.memory
        
       # memory = self.chatboot.memory_chat()
       
        memory = ConversationBufferWindowMemory(k=10, return_messages=True)
        memory.chat_memory.add_user_message("Olá IA")
        memory.chat_memory.add_ai_message("olá weley")
        
        
        
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
            chat.markdown("gerando resposta")
            memory.chat_memory.add_user_message(question)
            memory.chat_memory.add_ai_message("olá, aqui é uma llm que esta respondeod")
            