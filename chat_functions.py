import google.generativeai as genai
import os
from fpdf import FPDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import textwrap
import mimetypes
import gradio as gr
import time
from google.api_core.exceptions import InvalidArgument

# This function allows you to create multiple prompts, a concept for prompt engineering
def initial_prompts():
    prompts = [
     "você é um analista de dados sua tarefa é responder e preencher o documento de proposta de trabalho de acordo com a metodologia PACE, será solicitado qual é stage pace este contexto faz parte, seu papel é responder e informar se necessario qual função é designada para isso",
     "Por favor, aprimore o meu currículo para deixá-lo mais assertivo e enfatizando os pontos positivos. Eis o meu currículo",
     "Pode gerar um relatório de dois ou três parágrafos baseado nesses dados? Fale de tendências dos clubes.",
     "Qual é a extensão do arquivo recebido, exemplo jpeg, pdf, txt, etc"
    ]
    return prompts    

# The initial_setting() function is responsible for preparing and configuring the environment for your Gemini chatbot.
def initial_setting():
    prompts = initial_prompts()
    genai.configure(api_key=os.environ["KEY_GEMINI"])
    model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=prompts[3])
    return model, prompts

# Generates AI content using Gemini model, prints, then returns text.
def generate_content():
    model = initial_setting()    
    content = "Olá,"
    response = model.generate_content(content)
    print(response.text)
    return response.text

# Function that save the response of model in one file pdf, how object of type text can receive a function generate_content or better_curriculum or others
def save_text_on_pdf(name_file_pdf="file name"):
    try:
        obj_with_text = upload_files()

        if hasattr(obj_with_text, 'text'):
            content_text = obj_with_text.text
        else:
            content_text = str(obj_with_text)

        # Create a file PDF with text
        c = canvas.Canvas(name_file_pdf, pagesize=A4)
        width, height = A4
        margin = 40
        y = height - margin

        lines = textwrap.wrap(content_text, width=100)

        for line in lines:
            if y < margin:
                c.showPage()
                y = height - margin
            c.drawString(margin, y, line)
            y -= 15

        c.save()
        print(f"Arquivo PDF salvo como: {name_file_pdf}")

    except Exception as e:
        print(f"Erro ao obter ou salvar o texto: {e}")
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.set_left_margin(10)
    pdf.set_right_margin(10)
    pdf.set_auto_page_break(True, margin=15)
    pdf.multi_cell(0, 10, content_text)
    pdf.output(name_file_pdf)
    print(f"O texto foi salvo com sucesso em '{name_file_pdf}' usando FPDF.")

# Function that receives a resume and suggests improvements
def better_curriculum():
    model, prompts = initial_setting()
    with open("Curriculo.txt", "r") as file:
        curriculum = file.read()
        content =  f"{prompts[1]}:\n{curriculum}"
        response = model.generate_content(content)
        return response.text
    
# Function to upload of the files
def upload_files():
    model, prompts = initial_setting()
    sheet = genai.upload_file(
        path="Brasileiro_2024.csv",
        display_name="Tabela campeonato brasileiro"
    )
    content = prompts[2] 
    response = model.generate_content([sheet, content])
    return response.text

# Initialize the chat of mode global
model, prompts = initial_setting()
chat =  model.start_chat(history=[])
# Function that its passed for create interface using gradio
def gradio_wrapper(message: dict, history: list) -> str:
    try:

        user_message_text = message.get("text", "")
        user_message_files = message.get("files", [])

        # List to build the 'parts' of the message to Gemini
        gemini_content_parts = []

        if user_message_text:
            gemini_content_parts.append(user_message_text)

        # process attached files
        for file_path in user_message_files:
            if file_path: 
                try:
                    # Try to guess the MIME type of the file
                    mime_type, _ = mimetypes.guess_type(file_path)
                    if not mime_type:
                        mime_type = 'application/octet-stream'
                    with open(file_path, 'rb') as f:
                        file_data = f.read()
                    gemini_content_parts.append(
                        {
                            'mime_type': mime_type,
                            'data': file_data
                        }
                    )
                except Exception as file_err:
                    print(f"DEBUG: Erro ao processar arquivo {file_path}: {file_err}")
                    gemini_content_parts.append(f"Erro ao carregar arquivo: {os.path.basename(file_path)}. Detalhes: {file_err}")
        if not gemini_content_parts:
           return "Por favor, digite uma mensagem ou anexe um arquivo para iniciar a conversa."

        # Send the 'parts' (text + files) to the Gemini model
        # 'chat' is the global chat object that holds the context
        response = chat.send_message(gemini_content_parts)

        # Return the response of text
        if hasattr(response, 'text') and isinstance(response.text, str):
            return response.text
        else:
            print(f"DEBUG: Resposta inesperada da API Gemini: {response}")
            return "Desculpe, recebi uma resposta inesperada do modelo."

    except Exception as e:
        print(f"DEBUG: Erro geral na função gradio_wrapper: {e}")
        return f"Desculpe, ocorreu um erro ao processar sua mensagem: {e}" 
chat_interface = gr.ChatInterface(fn=gradio_wrapper,
title="Chatbot com Suporte a Arquivos 🤖", multimodal=True)
chat_interface.launch()

