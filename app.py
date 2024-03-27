import streamlit as st
from streamlit_option_menu import option_menu

# Importação dos menus personalizados
import menu_combinar
import menu_extrair
import menu_imagens
import menu_marca_dagua
import menu_relatorio

# Configuração da página
st.set_page_config(
    page_title="",
    page_icon=":page_facing_up:",  # Ícone da página
    layout="wide",  # Layout amplo
)

# Divisão da página em três colunas, com uma coluna vazia em cada lado e o menu no centro
_, col2, _ = st.columns(3)

# Título principal do aplicativo
with col2:
    st.title("📄 TEP - Tools Easy PDF ")
    st.markdown(
        """
    ### Escolha a opção desejada abaixo:
    """
    )

# Dicionário de entradas do menu com as opções e seus ícones correspondentes
entradas_menu = {
    "Extrair página": "file-earmark-pdf-fill",
    "Combinar PDFs": "plus-square-fill",
    "Adicionar marca d'água": "droplet-fill",
    "Imagens para PDF": "file-earmark-richtext-fill",
    "PDF para Excel": "file-earmark-spreadsheet-fill",
}

# Renderização do menu de opções com ícones
escolha = option_menu(
    menu_title=None,
    orientation="horizontal",
    options=list(entradas_menu.keys()),
    icons=list(entradas_menu.values()),
    default_index=0,
)

# Redivisão da página em três colunas para o conteúdo do menu
_, col2, _ = st.columns(3)

# Lógica para renderizar o conteúdo do menu com base na opção escolhida
match escolha:
    case "Extrair página":
        menu_extrair.exibir_menu_extrair(coluna=col2)
    case "Combinar PDFs":
        menu_combinar.exibir_menu_combinar(coluna=col2)
    case "Adicionar marca d'água":
        menu_marca_dagua.exibir_menu_marca_dagua(coluna=col2)
    case "Imagens para PDF":
        menu_imagens.exibir_menu_imagens(coluna=col2)
    case "PDF para Excel":
        menu_relatorio.exibir_menu_conversor(coluna=col2)
