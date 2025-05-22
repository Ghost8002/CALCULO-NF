import streamlit as st
import pandas as pd
from codigo import calcular_totais
import os
import locale

# Configurar locale para português do Brasil
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def formatar_valor(valor):
    """Formata o valor para o padrão brasileiro"""
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

st.set_page_config(page_title="Calculadora de Notas Fiscais", page_icon="📊")

def ler_excel(arquivo):
    """Função para ler arquivos Excel (.xls ou .xlsx)"""
    try:
        # Tenta ler como .xlsx primeiro
        return pd.read_excel(arquivo, sheet_name='RelatorioNotas', engine='openpyxl')
    except:
        try:
            # Se falhar, tenta ler como .xls
            return pd.read_excel(arquivo, sheet_name='RelatorioNotas', engine='xlrd')
        except Exception as e:
            raise Exception(f"Erro ao ler o arquivo {arquivo.name}: {str(e)}")

st.title("Calculadora de Notas Fiscais")
st.write("Faça upload dos arquivos Excel para calcular os totais de notas fiscais.")

# Upload dos arquivos
st.subheader("Upload dos Arquivos")
uploaded_files = st.file_uploader(
    "Selecione os arquivos Excel (NF Emitidas, NF Recebidas e/ou NFC Emitidas)",
    type=['xlsx', 'xls'],
    accept_multiple_files=True
)

if st.button("Calcular Totais"):
    if uploaded_files:  # Se houver pelo menos um arquivo
        try:
            # Dicionário para armazenar os arquivos
            arquivos = {
                'nf_emitidas': None,
                'nf_recebidas': None,
                'nfc_emitidas': None
            }
            
            # Identificar os arquivos pelo nome
            for file in uploaded_files:
                nome_arquivo = file.name.lower()
                if 'emitida' in nome_arquivo and 'nfc' not in nome_arquivo:
                    arquivos['nf_emitidas'] = file
                elif 'recebida' in nome_arquivo:
                    arquivos['nf_recebidas'] = file
                elif 'nfc' in nome_arquivo:
                    arquivos['nfc_emitidas'] = file

            # Verificar quais arquivos foram carregados
            arquivos_carregados = {k: v for k, v in arquivos.items() if v is not None}
            if not arquivos_carregados:
                st.error("Nenhum arquivo válido foi identificado. Verifique se os nomes dos arquivos contêm 'emitida', 'recebida' ou 'nfc'.")
            else:
                # Salvar arquivos temporariamente
                temp_files = {}
                for tipo in arquivos.keys():
                    if tipo in arquivos_carregados:
                        temp_path = f"temp_{tipo}.xlsx"
                        with open(temp_path, "wb") as f:
                            f.write(arquivos_carregados[tipo].getvalue())
                        temp_files[tipo] = temp_path
                    else:
                        # Criar um DataFrame vazio com as colunas necessárias
                        df_vazio = pd.DataFrame(columns=['Valor N.F.', 'Situacao', 'Operacao'])
                        temp_path = f"temp_{tipo}.xlsx"
                        # Criar um ExcelWriter para garantir a criação da planilha correta
                        with pd.ExcelWriter(temp_path, engine='openpyxl') as writer:
                            df_vazio.to_excel(writer, sheet_name='RelatorioNotas', index=False)
                        temp_files[tipo] = temp_path

                # Calcular totais
                total_emitidas, total_recebidas = calcular_totais(
                    temp_files['nf_emitidas'],
                    temp_files['nf_recebidas'],
                    temp_files['nfc_emitidas']
                )

                # Exibir resultados
                st.success("Cálculos realizados com sucesso!")
                
                # Mostrar quais arquivos foram processados
                st.write("Arquivos processados:")
                for tipo, arquivo in arquivos_carregados.items():
                    st.write(f"- {tipo.replace('_', ' ').title()}: {arquivo.name}")
                
                # Mostrar arquivos não fornecidos
                arquivos_nao_fornecidos = {k: v for k, v in arquivos.items() if v is None}
                if arquivos_nao_fornecidos:
                    st.write("\nArquivos não fornecidos:")
                    for tipo in arquivos_nao_fornecidos.keys():
                        st.write(f"- {tipo.replace('_', ' ').title()}")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Total NF Emitidas", formatar_valor(total_emitidas))
                with col2:
                    st.metric("Total NF Recebidas", formatar_valor(total_recebidas))

                # Limpar arquivos temporários
                for temp_file in temp_files.values():
                    if os.path.exists(temp_file):
                        os.remove(temp_file)

        except Exception as e:
            st.error(f"Erro ao processar os arquivos: {str(e)}")
            st.write("Verifique se:")
            st.write("1. Os arquivos estão no formato correto (.xlsx ou .xls)")
            st.write("2. A planilha 'RelatorioNotas' existe em cada arquivo")
            st.write("3. Os arquivos contêm as colunas necessárias: 'Valor N.F.', 'Situacao', 'Operacao'")
    else:
        st.warning("Por favor, faça upload de pelo menos um arquivo Excel.")

# Adicionar informações de ajuda
with st.expander("Como usar"):
    st.write("""
    1. Selecione um ou mais arquivos Excel (.xlsx ou .xls) de:
       - NF Emitidas
       - NF Recebidas
       - NFC Emitidas
    2. Clique em 'Calcular Totais'
    
    Observações:
    - Os arquivos podem estar no formato Excel (.xlsx ou .xls)
    - Todos os arquivos são opcionais
    - Os nomes dos arquivos devem conter as palavras 'emitida', 'recebida' ou 'nfc' para identificação automática
    - O sistema calculará os totais com base nos arquivos disponíveis
    """) 