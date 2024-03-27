import streamlit as st
from tabula.io import read_pdf
import pandas as pd
from io import BytesIO


def convert_single_pdf_to_excel(uploaded_file):
    try:
        dfs = read_pdf(
            BytesIO(uploaded_file.read()),
            pages="all",
            multiple_tables=True,
            stream=True,
        )
        df_final = pd.concat(dfs)
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df_final.to_excel(writer, index=False)
        output.seek(0)
        return output
    except Exception as e:
        st.error(f"Ocorreu um erro durante a conversão: {e}")
        return None


def exibir_menu_conversor(coluna):
    with coluna:
        st.markdown("## Conversor de PDF para Excel")
        st.markdown("Escolha o(s) arquivo(s) PDF para converter em Excel:")

        uploaded_files = st.file_uploader(
            "Selecione os arquivos PDF",
            type="pdf",
            accept_multiple_files=True,
            key="pdf_uploader",
            label_visibility="collapsed",
        )

        converter_disabled = not uploaded_files
        clicou_converter = st.button(
            "Converter",
            disabled=converter_disabled,
            use_container_width=True,
            key="converter_button",
        )

        if clicou_converter:
            multi_file_option = st.radio(
                "Escolha o tipo de conversão:",
                ("Único arquivo Excel", "Múltiplos arquivos Excel"),
                key="conversion_radio",
            )

            multi_file = multi_file_option == "Múltiplos arquivos Excel"
            if multi_file:
                for i, uploaded_file in enumerate(uploaded_files):
                    result = convert_single_pdf_to_excel(uploaded_file)
                    if result:
                        st.download_button(
                            label=f"Baixar Excel {i+1}",
                            data=result,
                            file_name=f"converted_{i+1}.xlsx",
                            mime="application/vnd.ms-excel",
                            key=f"download_excel_{i}",
                        )
            else:
                all_dfs = []
                for uploaded_file in uploaded_files:
                    single_result = convert_single_pdf_to_excel(uploaded_file)
                    if single_result:
                        all_dfs.append(pd.read_excel(single_result))

                if all_dfs:
                    concatenated_df = pd.concat(all_dfs)
                    output = BytesIO()
                    with pd.ExcelWriter(output, engine="openpyxl") as writer:
                        concatenated_df.to_excel(writer, index=False)
                    output.seek(0)
                    st.download_button(
                        label="Baixar Excel Consolidado",
                        data=output,
                        file_name="consolidated_converted.xlsx",
                        mime="application/vnd.ms-excel",
                        key="download_consolidated_excel",
                    )
