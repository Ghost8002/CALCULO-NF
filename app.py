import streamlit as st
import pandas as pd
from codigo import calcular_totais
import os

def formatar_valor(valor):
    """Formata o valor para o padrão brasileiro"""
    try:
        # Converte para string com 2 casas decimais
        valor_str = f"{valor:,.2f}"
        # Substitui a vírgula por X (temporário)
        valor_str = valor_str.replace(",", "X")
        # Substitui o ponto por vírgula
        valor_str = valor_str.replace(".", ",")
        # Substitui X por ponto
        valor_str = valor_str.replace("X", ".")
        return f"R$ {valor_str}"
    except:
        return f"R$ {valor:,.2f}"

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

# Criar colunas para os uploads
col1, col2, col3 = st.columns(3)

with col1:
    st.write("**NF Emitidas**")
    nf_emitidas = st.file_uploader("Selecione o arquivo", type=['xlsx', 'xls'], key="emitidas")

with col2:
    st.write("**NF Recebidas**")
    nf_recebidas = st.file_uploader("Selecione o arquivo", type=['xlsx', 'xls'], key="recebidas")

with col3:
    st.write("**NFC Emitidas**")
    nfc_emitidas = st.file_uploader("Selecione o arquivo", type=['xlsx', 'xls'], key="nfc")

if st.button("Calcular Totais"):
    if nf_emitidas or nf_recebidas:  # Pelo menos um dos arquivos principais deve estar presente
        try:
            # Dicionário para armazenar os arquivos
            arquivos = {
                'nf_emitidas': nf_emitidas,
                'nf_recebidas': nf_recebidas,
                'nfc_emitidas': nfc_emitidas
            }
            
            # Verificar quais arquivos foram carregados
            arquivos_carregados = {k: v for k, v in arquivos.items() if v is not None}
            
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
        st.warning("Por favor, faça upload de pelo menos um arquivo de NF Emitidas ou NF Recebidas.")

# Adicionar informações de ajuda
with st.expander("Como usar"):
    st.write("""
    1. Selecione os arquivos Excel (.xlsx ou .xls) para cada tipo de nota fiscal:
       - NF Emitidas (obrigatório se não houver NF Recebidas)
       - NF Recebidas (obrigatório se não houver NF Emitidas)
       - NFC Emitidas (opcional)
    2. Clique em 'Calcular Totais'
    
    Observações:
    - Os arquivos podem estar no formato Excel (.xlsx ou .xls)
    - É necessário pelo menos um arquivo de NF Emitidas ou NF Recebidas
    - O arquivo de NFC Emitidas é opcional
    - A planilha deve ter o nome 'RelatorioNotas'
    - As colunas necessárias são: 'Valor N.F.', 'Situacao', 'Operacao'
    """) 
