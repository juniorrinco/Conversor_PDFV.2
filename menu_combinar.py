import pypdf  # Importação redundante, deve ser PyPDF2
import streamlit as st

from utilidades import pegar_dados_pdf


def exibir_menu_combinar(coluna):
    """Exibe o menu para combinar dois ou mais arquivos PDFs em um único arquivo."""
    with coluna:
        st.markdown(
            """
        # Combinar PDFs

        Selecione dois ou mais arquivos PDF para combinar:
        """
        )

        arquivos_pdf = st.file_uploader(
            label="Selecione os arquivos PDF para combinar",
            type="pdf",
            accept_multiple_files=True,
        )
        if arquivos_pdf:
            botoes_desativados = False
        else:
            botoes_desativados = True

        clicou_processar = st.button(
            "Clique para processar o arquivo PDF",
            disabled=botoes_desativados,
            use_container_width=True,
        )
        if clicou_processar:
            dados_pdf = combinar_arquivos_pdf(arquivos_pdf=arquivos_pdf)
            nome_arquivo = f"combinado.pdf"
            st.download_button(
                "Clique para baixar o arquivo PDF resultante",
                type="primary",
                data=dados_pdf,
                file_name=nome_arquivo,
                mime="application/pdf",
                use_container_width=True,
            )


def combinar_arquivos_pdf(arquivos_pdf):
    """Combina vários arquivos PDF em um único arquivo."""
    escritor = pypdf.PdfWriter()  # Corrigido o nome do módulo para PyPDF2
    for arquivo_pdf in arquivos_pdf:
        leitor = pypdf.PdfReader(arquivo_pdf)  # Corrigido o nome do módulo para PyPDF2
        for pagina in leitor.pages:
            escritor.add_page(pagina)
    # Função pegar_dados_pdf precisa ser definida ou importada corretamente
    dados_pdf = pegar_dados_pdf(escritor=escritor)
    return dados_pdf
