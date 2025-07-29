import google.generativeai as genai
import os

# This function allows you to create multiple prompts, a concept for prompt engineering
def initial_prompts():
    prompts = [
     "você é um analista de dados sua tarefa é responder e preencher o documento de proposta de trabalho de acordo com a metodologia PACE, será solicitado qual é stage pace este contexto faz parte, seu papel é responder e informar se necessario qual função é designada para isso",
     "voce é um torcedor do sao paulo futebol clube"
    ]
    return prompts    

# The initial_setting() function is responsible for preparing and configuring the environment for your Gemini chatbot.
def initial_setting():
    prompts = initial_prompts()
    genai.configure(api_key=os.environ["KEY_GEMINI"])
    print(f"seu prompt inicial é este: {prompts[0]}")
    model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=prompts[0])
    return model

