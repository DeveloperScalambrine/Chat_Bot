import google.generativeai as genai
import os
from fpdf import FPDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import textwrap

# This function allows you to create multiple prompts, a concept for prompt engineering
def initial_prompts():
    prompts = [
     "você é um analista de dados sua tarefa é responder e preencher o documento de proposta de trabalho de acordo com a metodologia PACE, será solicitado qual é stage pace este contexto faz parte, seu papel é responder e informar se necessario qual função é designada para isso",
     "Por favor, aprimore o meu currículo para deixá-lo mais assertivo e enfatizando os pontos positivos.",
     "Pode gerar um relatório de dois ou três parágrafos baseado nesses dados? Fale de tendências, insights e outliers destacando-os.",
     "Qual é a extensão do arquivo recebido, exemplo jpeg, pdf, txt, etc",
     "Voce tem acesso a funções de gerar conteudo, melhorar curriculo, subir arquivos e salvar arquivos pdf, chame-as quando achar necessario e nunca exponha o a função chamada por voce."
    ]
    return prompts    

# The initial_setting() function is responsible for preparing and configuring the environment for your Gemini chatbot.
def initial_setting():
    prompts = initial_prompts()
    genai.configure(api_key=os.environ["KEY_GEMINI"])
    model = genai.GenerativeModel(model_name="gemini-2.5-flash", system_instruction=prompts[2], tools=[generate_content, save_text_on_pdf, better_curriculum, upload_files])
    return model, prompts

# Generates AI content using Gemini model, prints, then returns text.
print("Gerar conteudo")
def generate_content():
    model = initial_setting()    
    content = "Olá,"
    response = model.generate_content(content)
    return response.text

# Function that save the response of model in one file pdf, how object of type text can receive a function generate_content or better_curriculum or others
print("Salvar arquivo pdf")
def save_text_on_pdf(name_file_pdf="file name"):
    try:
        obj_with_text = better_curriculum()

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
print("Melhorar curriculo")
def better_curriculum():
    model, prompts = initial_setting()
    with open("Curriculo.txt", "r") as file:
        curriculum = file.read()
        content =  f"{prompts[1]}:\n{curriculum}"
        response = model.generate_content(content)
        return response.text
    
# Function to upload of the files
print("Subir arquivos")
def upload_files():
    model, prompts = initial_setting()
    sheet = genai.upload_file(
        path="Analise Sorveteria.csv",
        display_name="Tabela campeonato brasileiro"
    )
    content = prompts[2] 
    response = model.generate_content([sheet, content])
    return response.text

