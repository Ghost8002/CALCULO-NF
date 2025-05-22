# Calculadora de Notas Fiscais

Aplicação web para calcular totais de notas fiscais emitidas e recebidas.

## Funcionalidades

- Upload de arquivos Excel (.xlsx ou .xls)
- Cálculo automático de totais
- Suporte a NF Emitidas, NF Recebidas e NFC Emitidas
- Formatação de valores no padrão brasileiro
- Interface amigável e responsiva

## Requisitos

- Python 3.8 ou superior
- Dependências listadas em `requirements.txt`

## Instalação

1. Clone este repositório:
```bash
git clone [URL_DO_REPOSITÓRIO]
cd [NOME_DO_DIRETÓRIO]
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Uso Local

Para executar localmente:
```bash
streamlit run app.py
```

## Deploy no Streamlit Cloud

1. Crie uma conta no [Streamlit Cloud](https://streamlit.io/cloud)
2. Conecte com seu repositório GitHub
3. Selecione este repositório
4. Configure o deploy:
   - Main file path: `app.py`
   - Python version: 3.8 ou superior

## Estrutura do Projeto

```
.
├── app.py              # Interface principal
├── codigo.py           # Lógica de cálculo
├── requirements.txt    # Dependências
├── README.md          # Documentação
└── .gitignore         # Arquivos ignorados
```

## Formato dos Arquivos Excel

Os arquivos Excel devem conter:
- Planilha chamada 'RelatorioNotas'
- Colunas: 'Valor N.F.', 'Situacao', 'Operacao'

## Contribuição

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request 