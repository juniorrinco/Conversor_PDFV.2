from pathlib import Path  # Importação redundante, pode ser removida
import PyPDF2  # Corrigido o nome do módulo para PyPDF2
import streamlit as st

from utilidades import pegar_dados_pdf


def exibir_menu_extrair(coluna):
    """Exibe o menu para extrair uma página de um arquivo PDF."""
    with coluna:
        st.markdown(
            """
        # Extrair página de PDF

        Escolha um arquivo PDF para extrair uma página:
        """
        )

        arquivo_pdf = st.file_uploader(
            label="Selecione o arquivo PDF",
            type="pdf",
            accept_multiple_files=False,
        )
        if arquivo_pdf:
            botoes_desativados = False
        else:
            botoes_desativados = True

        numero_pagina = st.number_input(
            "Página para extrair", disabled=botoes_desativados, min_value=1
        )
        clicou_processar = st.button(
            "Clique para processar o arquivo PDF",
            disabled=botoes_desativados,
            use_container_width=True,
        )
        if clicou_processar:
            dados_pdf = extrair_pagina_pdf(
                arquivo_pdf=arquivo_pdf, numero_pagina=numero_pagina
            )
            if dados_pdf is None:
                st.warning(f"PDF não possui página de número {numero_pagina}!")
            else:
                # Renomeando o arquivo PDF resultante com o número da página
                nome_arquivo = (
                    f"{Path(arquivo_pdf.name).stem}_pg{numero_pagina:03d}.pdf"
                )
                # Adicionando um botão para baixar o arquivo PDF
                st.download_button(
                    "Clique para baixar o arquivo PDF",
                    type="primary",
                    data=dados_pdf,
                    file_name=nome_arquivo,
                    mime="application/pdf",
                    use_container_width=True,
                )


def extrair_pagina_pdf(arquivo_pdf, numero_pagina):
    """Extrai a página especificada de um arquivo PDF."""
    leitor = PyPDF2.PdfReader(arquivo_pdf)
    try:
        pagina = leitor.pages[numero_pagina - 1]
    except IndexError:
        return None

    escritor = PyPDF2.PdfWriter()
    escritor.add_page(pagina)
    # Função pegar_dados_pdf precisa ser definida ou importada corretamente
    dados_pdf = pegar_dados_pdf(escritor=escritor)
    return dados_pdf
