import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_community.document_loaders.pdf import PyPDFLoader

#classe que divide o texto em chunks
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter

load_dotenv()


document_pdf = PyPDFLoader('apostila.pdf') #lendo documento
model = ChatGroq(model='llama-3.2-90b-vision-preview', api_key=os.getenv('TOKEN_GROQ'))
texto = '''Responda exclusivamente com base no contexto fornecido. 
            Não faça buscas externas, nem busque informações fora do contexto, incluindo a internet ou fontes externas.
            limite-se a responder apenas no que está no contexto. 
            Se uma pergunta se referir a algo que não está presente no contexto, informe que não há informações disponíveis para responder a essa questão.
            Não faça suposições e não forneça informações não mencionadas no contexto.
            Responda de maneira clara e objetiva, apenas com os dados disponíveis no contexto.'''

#configurando o CharacterTextSplitter
char_splitter = CharacterTextSplitter(
    chunk_size = 5, #define quantidade de chunks
    chunk_overlap = 2, #os últimos caracteres da chunks anteriores serão os primeiros caracteres da próxima chunk
    separator='' #onde irá ser feito a quebra. Vazio significa que a split será feito em qualquer lugar
)

recursive_explitter = RecursiveCharacterTextSplitter(chunk_size = 50,chunk_overlap = 10,)
splliter_recursvie = recursive_explitter.split_text(texto) #executando o splitter no texto
spliiter_dcomentos = recursive_explitter.split_documents(documents=document_pdf.load()) #executando splitter no documento


print(spliiter_dcomentos)
print(len(spliiter_dcomentos))

