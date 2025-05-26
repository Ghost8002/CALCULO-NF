import pandas as pd

def preparar_df(df):
    # Verifica se o DataFrame está vazio
    if df.empty:
        return pd.DataFrame(columns=['Valor N.F.', 'Situacao', 'Operacao'])
    
    # Verifica se tem pelo menos uma linha
    if len(df) == 0:
        return pd.DataFrame(columns=['Valor N.F.', 'Situacao', 'Operacao'])
    
    # Verifica se tem pelo menos uma coluna
    if len(df.columns) == 0:
        return pd.DataFrame(columns=['Valor N.F.', 'Situacao', 'Operacao'])
    
    # Tenta definir as colunas
    try:
        df.columns = df.iloc[0]
        df = df.drop(0).reset_index(drop=True)
    except:
        # Se falhar, verifica se as colunas já existem
        colunas_necessarias = ['Valor N.F.', 'Situacao', 'Operacao']
        if not all(col in df.columns for col in colunas_necessarias):
            return pd.DataFrame(columns=colunas_necessarias)
    
    # Converte as colunas para o formato correto
    try:
        df['Valor N.F.'] = pd.to_numeric(df['Valor N.F.'], errors='coerce')
        df['Situacao'] = df['Situacao'].astype(str).str.strip().str.lower()
        df['Operacao'] = df['Operacao'].astype(str).str.strip().str.upper()
    except:
        # Se falhar na conversão, retorna DataFrame vazio
        return pd.DataFrame(columns=['Valor N.F.', 'Situacao', 'Operacao'])
    
    return df

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
            raise Exception(f"Erro ao ler o arquivo {arquivo}: {str(e)}")

def calcular_totais(nf_emitidas_path, nf_recebidas_path, nfc_emitidas_path=None):
    # Carregar arquivos Excel
    df_nf_emitidas = ler_excel(nf_emitidas_path)
    df_nf_recebidas = ler_excel(nf_recebidas_path)
    
    df_nf_emitidas = preparar_df(df_nf_emitidas)
    df_nf_recebidas = preparar_df(df_nf_recebidas)
    
    if nfc_emitidas_path:
        df_nfc_emitidas = ler_excel(nfc_emitidas_path)
        df_nfc_emitidas = preparar_df(df_nfc_emitidas)
    else:
        df_nfc_emitidas = pd.DataFrame(columns=df_nf_emitidas.columns)  # vazio se não informado

    # Filtrar notas válidas (não canceladas)
    emitidas_validas = df_nf_emitidas[df_nf_emitidas['Situacao'] != 'Cancelamento']
    recebidas_validas = df_nf_recebidas[df_nf_recebidas['Situacao'] != 'Cancelamento']
    nfc_emitidas_validas = df_nfc_emitidas[df_nfc_emitidas['Situacao'] != 'Cancelamento']

    # NF Emitidas:
    emitidas_saida = emitidas_validas[emitidas_validas['Operacao'] == 'SAIDA']['Valor N.F.'].sum()
    emitidas_entrada_devolucao = emitidas_validas[emitidas_validas['Operacao'] == 'ENTRADA']['Valor N.F.'].sum()

    # NFC Emitidas:
    nfc_emitidas_saida = nfc_emitidas_validas[nfc_emitidas_validas['Operacao'] == 'SAIDA']['Valor N.F.'].sum()
    nfc_emitidas_entrada_devolucao = nfc_emitidas_validas[nfc_emitidas_validas['Operacao'] == 'ENTRADA']['Valor N.F.'].sum()

    # NF Recebidas:
    recebidas_entrada = recebidas_validas[recebidas_validas['Operacao'] == 'SAIDA']['Valor N.F.'].sum()
    recebidas_entrada_devolucao = recebidas_validas[recebidas_validas['Operacao'] == 'ENTRADA']['Valor N.F.'].sum()

    # Totais finais
    total_nf_emitidas = emitidas_saida + recebidas_entrada_devolucao + nfc_emitidas_saida + nfc_emitidas_entrada_devolucao
    total_nf_recebidas = recebidas_entrada + emitidas_entrada_devolucao

    return total_nf_emitidas, total_nf_recebidas

# Exemplo de uso
if __name__ == "__main__":
    nf_emitidas_file = 'NF EMITIDAS.xlsx'
    nf_recebidas_file = 'NF RECEBIDAS.xlsx'
    nfc_emitidas_file = 'NFC EMITIDAS.xlsx'  # ou None se não tiver
    
    total_emitidas, total_recebidas = calcular_totais(nf_emitidas_file, nf_recebidas_file, nfc_emitidas_file)
    print(f"Total NF Emitidas (com devoluções e NFC Emitidas): {total_emitidas}")
    print(f"Total NF Recebidas (com devoluções): {total_recebidas}")
