
import os
import time
import queue
import tempfile
import pygame  # Biblioteca para reproduzir áudio
import streamlit as st
from openai import OpenAI
import speech_recognition as sr
from dotenv import load_dotenv
from streamlit_webrtc import WebRtcMode, webrtc_streamer
load_dotenv()

# Configuração da chave da API
os.environ['OPENAI_API_KEY'] = os.getenv('TOKEN_OPENAI')


#resposta do chatboot por audio
def response_audio_openai(text):
    
    with st.spinner("processando audio"): 
        # Inicializa o cliente da OpenAI
        cliente = OpenAI()
        response = cliente.audio.speech.create(
            model='tts-1',
            voice='onyx',  # Tipo de voz: onyx, alloy, echo, fable, nova, shimmer
            input=text
        )
    
        # Cria um arquivo temporário para o áudio
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
            audio_path = temp_audio.name
        response.write_to_file(audio_path) # Salva o arquivo de áudio gerado no arquivo temporário

    # Inicializa o mixer do pygame para reprodução de áudio
    pygame.mixer.init()
    pygame.mixer.music.load(audio_path)
    stop_audio = st.sidebar.button("Parar áudio")# Define o botão para parar o áudio
    
        # Reproduz o áudio enquanto não foi interrompido
    if  st.session_state.audio_playing:
        st.session_state.audio_playing = False
        pygame.mixer.music.play()
        
         # Enquanto o áudio estiver tocando
    while pygame.mixer.music.get_busy():
        if stop_audio:  # Verifica se o botão foi clicado
            pygame.mixer.music.stop()
            st.session_state.audio_playing = False
            break
        time.sleep(0.1)

    # Finaliza a execução e limpa o estado
    pygame.mixer.quit()
    if os.path.exists(audio_path):
        os.remove(audio_path)
        

#captura de audio pelo microfone
def transcrever_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source: #Capturando audio do micrfone
            recognizer.adjust_for_ambient_noise(source)  # Ajusta para ruído ambiente
            st.sidebar.success("Pronto para capturar áudio. Pode começar a falar!")

            while True:
                #st.sidebar.write("Aguardando detecção de fala...")
                try:
                    # Detecta áudio sem travar indefinidamente
                    audio = recognizer.listen(source, timeout=None, phrase_time_limit=5)
                    st.sidebar.info("Processando transcrição...")
                    
                    # Transcreve o áudio detectado
                    question =  recognizer.recognize_google(audio, language="pt-BR")
                    return question
                except sr.UnknownValueError:
                    st.sidebar.warning("Não consegui entender o áudio. Tente novamente.")
                except sr.RequestError as e:
                    st.sidebar.error(f"Erro ao se conectar ao serviço de reconhecimento: {e}")
                    break
                except Exception as e:
                    st.sidebar.error(f"Ocorreu um erro inesperado: {e}")
                    break
            return question
        

