# Importando módulos necessários
import tempfile
from pathlib import Path


# Definindo a função para pegar os dados do PDF
def pegar_dados_pdf(escritor):
    # Criando um diretório temporário
    with tempfile.TemporaryDirectory() as temp_dir:
        # Criando um caminho para um arquivo temporário dentro do diretório temporário
        temp_pdf_file = Path(temp_dir) / "temp.pdf"
        # Escrevendo os dados do PDF no arquivo temporário
        escritor.write(temp_pdf_file)
        # Abrindo o arquivo temporário para leitura binária
        with open(temp_pdf_file, "rb") as output_pdf:
            # Lendo os dados do PDF e retornando
            pdf_data = output_pdf.read()
    return pdf_data
