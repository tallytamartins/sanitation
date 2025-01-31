import pandas as pd
import re

# Carregar o arquivo Excel 
excelFile = "test-phone.xlsx"
df = pd.read_excel(excelFile, dtype=str)

# Lista das colunas que serão alteradas
phoneColumns=["homePhone", "businessPhone", "phone"]

# Limpar e formatar os números de telefone
def clearNumberPhone(number):
    if pd.notna(number):  # Verifica se o valor não é nulo
        number = re.sub(r"\D", "", number)  # Remove tudo que não for número
        number = re.sub(r"^55", "", number)  # Remove o prefixo 55 do começo do número
        return number
    return ""

# Verificar se o telefone tem tamanho válido
def charactersQuantity(number):
    if 10 <= len(number) <= 11:
        return "Não"  # Número válido
    return "Sim"  # Número inválido

# Identificar números sequenciais ou repetidos
def repeteadAndSequential(number):
    if re.search(r"(012345|123456|234567|345678|456789|567890)", number):  # Sequências comuns
        return "Sim"
    if re.search(r"^(.)\1{5,}$", number):  # Exemplo: 1111111111 (número repetido)
        return "Sim"
    return "Não"

# Aplicar a função às colunas 
for column in phoneColumns:
    if column in df.columns:  # Garante que a coluna existe no arquivo
        df[column] = df[column].apply(clearNumberPhone)
        df[f"{column}_invalido"] = df[column].apply(charactersQuantity)  # Cria coluna de validação de quantidade de caracteres
        df[f"{column}_suspeito"] = df[column].apply(repeteadAndSequential)  # Cria coluna para validar se o número possui sequência numérica ou repetição

# Salvar o resultado em um novo arquivo Excel
df.to_excel("test-phoneSANEADO.xlsx", index=False)

print("Processo concluído! Arquivo salvo como 'dados_saneados.xlsx'.")