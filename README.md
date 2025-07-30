# 🚀 Projeto de Automação e Geração de Conteúdo com IA

Este projeto visa explorar e implementar soluções de automação e geração de conteúdo utilizando modelos de Inteligência Artificial, com foco inicial no modelo `gemini-1.5-flash` da Google.

---

## 📝 Sumário

1.  [Geração de Conteúdo e Exportação para PDF](#1-geração-de-conteúdo-e-exportação-para-pdf)
    * [Formulação do Prompt Correto](#formulação-do-prompt-correto)
    * [Uso do Modelo `gemini-1.5-flash`](#uso-do-modelo-gemini-15-flash)
    * [Salvar a Resposta em PDF](#salvar-a-resposta-em-pdf)
2.  [Criação das Funções `better_curriculum`, `upload_files` e `save_text_on_pdf`](#2-criação-das-funções-better_curriculum-upload_files-e-save_text_on_pdf)
    * [Função `better_curriculum`](#função-better_curriculum)
    * [Função `upload_files`](#função-upload_files)
    * [Função `save_text_on_pdf`](#função-save_text_on_pdf)
3.  [Configuração e Instalação](#3-configuração-e-instalação)
4.  [Uso Básico](#4-uso-básico)

---

## 1. Geração de Conteúdo e Exportação para PDF

Este tópico detalha o processo de como formular prompts eficazes para o modelo `gemini-1.5-flash` e, em seguida, como salvar a resposta gerada em um arquivo PDF.

### Formulação do Prompt Correto

A qualidade da resposta da IA depende diretamente da clareza e precisão do prompt. Para obter os melhores resultados:

* **Seja Claro e Específico:** Defina exatamente o que você espera. Evite ambiguidades.
* **Forneça Contexto:** Inclua informações relevantes que ajudem a IA a entender a tarefa.
* **Defina o Formato Desejado:** Especifique se você quer uma lista, um parágrafo, um código, etc.
* **Indique o Tom e Estilo:** Casual, formal, técnico, criativo, etc.
* **Limitações (Opcional):** Se houver, indique o tamanho máximo ou o número de itens.

**Exemplo de Prompt:**
"Crie um resumo de 200 palavras sobre a importância da energia solar fotovoltaica para a sustentabilidade global. O tom deve ser informativo e acessível ao público geral."

### Uso do Modelo `gemini-1.5-flash`

Para interagir com o modelo `gemini-1.5-flash`, utilizamos a API da Google AI. É necessário configurar sua chave de API para autenticação. A função `initial_setting()` é a responsável por preparar e configurar esse ambiente.

**Snippet Conceitual:**

```python
import google.generativeai as genai
import os

# A função initial_setting() configura a API e retorna o modelo e os prompts iniciais.
def initial_setting():
    prompts = [
     "você é um analista de dados sua tarefa é responder e preencher o documento de proposta de trabalho de acordo com a metodologia PACE, será solicitado qual é stage pace este contexto faz parte, seu papel é responder e informar se necessario qual função é designada para isso",
     "Por favor, aprimore o meu currículo para deixá-lo mais assertivo e enfatizando os pontos positivos. Eis o meu currículo",
     "Pode gerar um relatório de dois ou três parágrafos baseado nesses dados? Fale de tendências dos clubes."
    ]
    genai.configure(api_key=os.environ["KEY_GEMINI"])
    model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=prompts[1])
    return model, prompts

# Exemplo de como gerar conteúdo utilizando a função generate_content()
# Esta função gera conteúdo textual utilizando o modelo Gemini configurado em `initial_setting()`.
def generate_content():
    model, _ = initial_setting() # Obtém o modelo. Ignora os prompts retornados, pois o conteúdo é fixo.
    content = "Olá,"
    response = model.generate_content(content)
    print(response.text)
    return response.text
```
Salvar a Resposta em PDF
Após obter o texto da IA, é crucial salvá-lo em um formato acessível e padronizado como o PDF. Utilizaremos bibliotecas Python como FPDF e reportlab.lib.pagesizes.A4 para essa finalidade. A função save_text_on_pdf() lida com esse processo.

```python
from fpdf import FPDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import textwrap

# ... (Código para obter o texto_gerado, como de generate_content() ou upload_files()) ...

# Função que salva a resposta do modelo em um arquivo PDF
# Ela pode receber a saída de funções como generate_content ou better_curriculum.
def save_text_on_pdf(name_file_pdf="resposta_gemini.pdf"):
    try:
        # Exemplo: Chamando upload_files() para obter o texto a ser salvo.
        # Você pode substituir isso por qualquer função que retorne o texto.
        obj_with_text = upload_files() # ou generate_content() ou better_curriculum()

        if hasattr(obj_with_text, 'text'):
            content_text = obj_with_text.text
        else:
            content_text = str(obj_with_text) # Garante que o objeto é convertido para string

        # Cria um arquivo PDF usando ReportLab (para wrap de texto)
        c = canvas.Canvas(name_file_pdf, pagesize=A4)
        width, height = A4
        margin = 40
        y = height - margin

        # Quebra o texto em linhas para caber na página
        lines = textwrap.wrap(content_text, width=100)

        for line in lines:
            if y < margin: # Se a linha for além da margem inferior, cria nova página
                c.showPage()
                y = height - margin # Reseta 'y' para o topo da nova página
            c.drawString(margin, y, line) # Desenha a string
            y -= 15 # Move para a próxima linha

        c.save() # Salva o PDF gerado pelo ReportLab
        print(f"Arquivo PDF salvo como: {name_file_pdf} (via ReportLab)")

        # Geração de PDF adicional usando FPDF (mantido do original, pode ser uma alternativa)
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.set_left_margin(10)
        pdf.set_right_margin(10)
        pdf.set_auto_page_break(True, margin=15)
        pdf.multi_cell(0, 10, content_text) # Adiciona o texto ao PDF
        pdf.output(name_file_pdf.replace(".pdf", "_fpdf.pdf")) # Salva com nome diferente para não sobrescrever
        print(f"O texto foi salvo com sucesso em '{name_file_pdf.replace('.pdf', '_fpdf.pdf')}' usando FPDF.")

    except Exception as e:
        print(f"Erro ao obter ou salvar o texto: {e}")
```

🧠 2. Criação das Funções better_curriculum, upload_files e save_text_on_pdf
Este tópico aborda a implementação de funções fundamentais para aprimorar currículos, processar dados de arquivos (incluindo planilhas) e gerar relatórios, além da capacidade de salvar o texto gerado em formato PDF.

✍️ Função better_curriculum
A função better_curriculum é projetada para aprimorar um currículo existente. Ela lê o conteúdo de um arquivo Curriculo.txt e utiliza o modelo Gemini (com um prompt específico carregado de initial_prompts()) para reformular e otimizar o currículo, enfatizando os pontos positivos e tornando-o mais assertivo.

Esta função é útil para obter sugestões de melhoria diretamente da IA para o seu documento profissional.

```python
# Function that receives a resume and suggests improvements
def better_curriculum():
    # Obtém o modelo e os prompts. O system_instruction do modelo será prompts[1] (aprimorar currículo).
    model, prompts = initial_setting()
    with open("Curriculo.txt", "r") as file:
        curriculum = file.read()
        # O prompt completo para o Gemini inclui a instrução de aprimoramento e o conteúdo do currículo.
        content =  f"{prompts[1]}:\n{curriculum}"
        response = model.generate_content(content)
        return response.text
```
```python
# Function to upload of the files
def upload_files():
    # Obtém o modelo e os prompts. O system_instruction do modelo será prompts[1] (aprimorar currículo).
    # Se a intenção é gerar um relatório, o system_instruction inicial pode precisar ser ajustado
    # para 'prompts[2]' em initial_setting(), ou o prompt deve ser mais auto-contido.
    model, prompts = initial_setting()
    sheet = genai.upload_file(
        path="Brasileiro_2024.csv",
        display_name="Tabela campeonato brasileiro"
    )
    # O prompt final para o Gemini inclui o arquivo e a solicitação do relatório.
    content = prompts[2]
    response = model.generate_content([sheet, content]) # Envia o arquivo e o prompt como partes.
    return response.text
```
⚙️ 3. Configuração e Instalação
Para configurar o ambiente de desenvolvimento e rodar o projeto, siga os passos abaixo:
```
Clonar o Repositório:
git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
cd seu-repositorio
```
Criar Ambiente Virtual (Recomendado):
```
python -m venv .venv
# No Windows
.\.venv\Scripts\activate
# No macOS/Linux
source .venv/bin/activate
```
Instalar Dependências:
```
pip install -r requirements.txt
# Conteúdo de requirements.txt:
# google-generativeai
# fpdf
# reportlab # Adicionar se estiver usando o módulo canvas
```
Configurar sua Chave API do Google AI:
Crie um arquivo .env na raiz do projeto e adicione sua chave:
```
KEY_GEMINI=SUA_CHAVE_API_GERADA_AQUI
(Lembre-se de nunca comitar seu arquivo .env em repositórios públicos!)
```
Uso Básico
```
Para executar o script principal que demonstra a geração de conteúdo e exportação para PDF (após a configuração):

Bash

python main.py
```
🤝 Contribuições
Contribuições são bem-vindas! Se você tiver sugestões, melhorias ou quiser adicionar novos tópicos, sinta-se à vontade para abrir uma issue ou enviar um pull request.

📄 Licença
Este projeto está licenciado sob a Licença MIT. Veja o arquivo LICENSE para mais detalhes.

Desenvolvido por: Carlos Henrique Scalambrine de Souza
