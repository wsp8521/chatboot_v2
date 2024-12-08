import streamlit as st
import speech_recognition as sr
from interface.base import InterfaceBase


class ChatbootInterface(InterfaceBase):
    
     #área do chat    
    def chat_window(self):
        st.header('🚢 Chat Porto Itaqui', divider=True)
        vector_store = self.chatboot.load_vector_store
        recognizer = sr.Recognizer() #caputura do audio do microfone
             
        if vector_store is None: #verifica se ha banco de dados
            st.warning("Faça o upload de um PDF para começar.")
        
         #criando uma sessão de memória
        if 'memory' not in st.session_state: #verifica se há uma sessáo chamda memoria
             st.session_state['memory'] =  self.chatboot.memory_chat() ##armzenando memoria na sessão
             
        memory =  st.session_state['memory'] 
        mensagens = memory.load_memory_variables({})['history'] #lendo as mensagens da 
        container = st.container()#criando container de conversa
        
        for mensagem in mensagens:#percorrendo todas as mensatens
            chat = container.chat_message(mensagem.type)
            chat.markdown(mensagem.content) #exibindo as mensaaens
            
        with self.tab_conversa:
                activate_voice =st.checkbox("Perguntar por voz")
        
        if activate_voice:
            with sr.Microphone() as source: #Capturando audio do micrfone
   
                recognizer.adjust_for_ambient_noise(source)  # Ajusta para ruído ambiente
                st.sidebar.success("Pronto para capturar áudio. Pode começar a falar!")

                while True:
                    #st.sidebar.success("Aguardando detecção de fala...")
                    try:
                        # Detecta áudio sem travar indefinidamente
                        audio = recognizer.listen(source, timeout=None, phrase_time_limit=30)
                        st.sidebar.info("Processando transcrição...")
                        
                        # Transcreve o áudio detectado
                        question =  recognizer.recognize_google(audio, language="pt-BR")
                        self._memory_history(question=question, container=container, memory=memory)
    
                    except sr.UnknownValueError:
                        st.sidebar.warning("Não consegui entender o áudio. Tente novamente.")
                    except sr.RequestError as e:
                        st.sidebar.error(f"Erro ao se conectar ao serviço de reconhecimento: {e}")
                        break
                    except Exception as e:
                        st.sidebar.error(f"Ocorreu um erro inesperado: {e}")
                        break
        else:     
            question =  st.chat_input("Como posso ajudar você?")
            self._memory_history(question=question, container=container, memory=memory)
             
   