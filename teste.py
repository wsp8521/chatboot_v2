MODEL = {
    'Groq':{
        'modelos':['llama-3.2-90b-vision-preview','llama-3.1-70b-versatile','gemma2-9b-it']
        },
    'Openai':{
        'modelos':['gpt-4o-mini','gpt-3.5-turbo-0125']
        }
    }


provedor = list(MODEL.keys())[0]
modelos = MODEL[provedor]['modelos']
print(provedor)
print(modelos)