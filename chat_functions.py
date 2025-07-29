import google.generativeai as genai
import os
from fpdf import FPDF


# This function allows you to create multiple prompts, a concept for prompt engineering
def initial_prompts():
    prompts = [
     "você é um analista de dados sua tarefa é responder e preencher o documento de proposta de trabalho de acordo com a metodologia PACE, será solicitado qual é stage pace este contexto faz parte, seu papel é responder e informar se necessario qual função é designada para isso",
     "Voce é um Torcedor do sao paulo futebol clube, disserte sobre seu clube"
    ]
    return prompts    

# The initial_setting() function is responsible for preparing and configuring the environment for your Gemini chatbot.
def initial_setting():
    prompts = initial_prompts()
    genai.configure(api_key=os.environ["KEY_GEMINI"])
    model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=prompts[1])
    return model

# Generates AI content using Gemini model, prints, then returns text.
def generate_content():
    model = initial_setting()    
    content = "Ola,"
    response = model.generate_content(content)
    print(response.text)
    return response.text


