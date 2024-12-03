import streamlit as st
from chat.chatboot import ChatBoot
from langchain.memory import ConversationBufferMemory



class ChatbootInterface:
    def __init__(self):
        self.chatboot = ChatBoot(model="llama-3.2-90b-vision-preview")
        self.models =  {'Groq':{'modelos':['llama-3.2-90b-vision-preview','llama-3.1-70b-versatile','gemma2-9b-it'] },
                        'Openai':{'modelos':['gpt-4o-mini','gpt-3.5-turbo-0125']}}

    
        
    #config da página
    def config_page(self, page_title, page_icon=None ):
        st.set_page_config(page_title=page_title, page_icon=page_icon)
        

     #conteúdos da sidebar
    def sidebar(self):
        with st.sidebar:
           get_file = st.file_uploader("upload arquivo pdf", accept_multiple_files=True, type=['.pdf'])
           
        with st.spinner("processando documento"):
           self.chatboot.process_documents(get_file)

    #área do chat    
    def chat_window(self):
        st.header('🤖 Chat Port', divider=True)
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
         
            
