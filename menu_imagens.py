import tempfile
from pathlib import Path

import pypdf
import streamlit as st
from PIL import Image

from utilidades import pegar_dados_pdf


def exibir_menu_imagens(coluna):
    """Exibe o menu para gerar um arquivo PDF contendo múltiplas imagens, uma por página."""
    with coluna:
        # Título e instruções para o usuário
        st.markdown(
            """
        # Imagens para PDF

        Selecione as imagens para gerar um arquivo PDF com elas:
        """
        )

        # Carregamento das imagens pelo usuário
        imagens = st.file_uploader(
            label="Selecione as imagens que irão para o arquivo PDF...",
            type=["png", "jpg", "jpeg"],
            accept_multiple_files=True,
        )

        # Verificação se imagens foram carregadas
        if imagens:
            botoes_desativados = False
        else:
            botoes_desativados = True

        # Botão para processar as imagens
        clicou_processar = st.button(
            "Clique para processar o arquivo PDF...",
            disabled=botoes_desativados,
            use_container_width=True,
        )

        # Processamento das imagens quando o botão é clicado
        if clicou_processar:
            dados_pdf = gerar_arquivo_pdf_com_imagens(imagens=imagens)
            nome_arquivo = "imagens.pdf"

            # Botão de download do arquivo PDF resultante
            st.download_button(
                "Clique para baixar o arquivo PDF resultante...",
                type="primary",
                data=dados_pdf,
                file_name=nome_arquivo,
                mime="application/pdf",
                use_container_width=True,
            )


def gerar_arquivo_pdf_com_imagens(imagens):
    # Conversão das imagens para o formato Pillow
    imagens_pillow = []
    for imagem in imagens:
        dados_imagem = Image.open(imagem)
        if dados_imagem.mode == "RGBA":
            dados_imagem = remover_canal_transparencia(imagem=imagem)
        imagens_pillow.append(dados_imagem)

    # Salvando as imagens em um arquivo PDF temporário
    with tempfile.TemporaryDirectory() as tempdir:
        nome_arquivo = Path(tempdir) / "temp.pdf"
        imagens_pillow[0].save(
            nome_arquivo, save_all=True, append_images=imagens_pillow[1:]
        )
        pdf_imagens = pypdf.PdfReader(nome_arquivo)

    # Redimensionando e mesclando as páginas para garantir que todas tenham o mesmo tamanho e orientação
    escritor = pypdf.PdfWriter()
    for pagina in pdf_imagens.pages:
        # Adicionando uma página em branco com as dimensões adequadas
        pagina_em_branco = escritor.add_blank_page(
            width=pypdf.PaperSize.A4.width,
            height=pypdf.PaperSize.A4.height,
        )

        # Calculando a escala para ajustar a imagem à página em branco
        if pagina.mediabox.top > pagina.mediabox.right:
            scale = pagina_em_branco.mediabox.top / pagina.mediabox.top * 0.9
        else:
            scale = pagina_em_branco.mediabox.right / pagina.mediabox.right * 0.9

        # Calculando as translações necessárias para centralizar a imagem
        tx = (pagina_em_branco.mediabox.right - pagina.mediabox.right * scale) / 2
        ty = (pagina_em_branco.mediabox.top - pagina.mediabox.top * scale) / 2

        # Aplicando a transformação para redimensionar e centralizar a imagem na página em branco
        transformation = pypdf.Transformation().scale(scale).translate(tx=tx, ty=ty)
        pagina_em_branco.merge_transformed_page(pagina, transformation, over=True)

    # Coletando os dados do PDF resultante
    dados_pdf = pegar_dados_pdf(escritor=escritor)
    return dados_pdf


def remover_canal_transparencia(imagem):
    # Removendo o canal de transparência das imagens no formato RGBA
    imagem_rgba = Image.open(imagem)
    imagem_rgb = Image.new("RGB", imagem_rgba.size, (255, 255, 255))
    imagem_rgb.paste(imagem_rgba, mask=imagem_rgba.split()[3])
    return imagem_rgb
