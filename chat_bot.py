import os
import mimetypes
import gradio as gr
import time
from google.api_core.exceptions import InvalidArgument

from chat_functions import(
    initial_setting    
)

# Initialize the chat of mode global
model, prompts = initial_setting()
chat =  model.start_chat(history=[], enable_automatic_function_calling=True)
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

