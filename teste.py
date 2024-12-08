from openai import OpenAI
import os
import pygame  # Biblioteca para reproduzir áudio

# Configuração da chave da API
os.environ['OPENAI_API_KEY'] = os.getenv('TOKEN_OPENAI')

# Inicializa o cliente da OpenAI
cliente = OpenAI()
response = cliente.audio.speech.create(
    model='tts-1',
    voice='onyx', #tipo de voz: onyx, alloy, echo, fable, nova, shimmer
    input="onde fica essa casas"
)

# Salva o arquivo de áudio gerado
response.write_to_file('response.mp3')

# Inicializa o mixer do pygame para reprodução de áudio
pygame.mixer.init()

# Carrega e reproduz o arquivo de áudio
pygame.mixer.music.load('response.mp3')
pygame.mixer.music.play()

# Aguarda o fim da reprodução do áudio
while pygame.mixer.music.get_busy():  # Enquanto o áudio estiver tocando
    pygame.time.Clock().tick(10)
