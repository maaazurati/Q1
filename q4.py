import pandas as pd
import numpy as np

# Coleta de dados dos tratamentos
treatments = {}
alphabet = iter("ABCDEFGHIJKLMNOPQRSTUVWXYZ")  # Gerador de nomes dos tratamentos

print(
    "Insira os valores para cada tratamento separados por espaços (pressione Enter sem digitar valores para encerrar):")

while True:
    treatment_name = next(alphabet)  # Nomeia os tratamentos automaticamente (A, B, C, ...)
    user_input = input(f"Tratamento {treatment_name}: ")
    if not user_input.strip():  # Encerra se o input for vazio
        break
    try:
        # Armazena os valores convertidos para float
        treatments[treatment_name] = list(map(float, user_input.split()))
    except ValueError:
        print("Erro! Por favor, insira apenas números separados por espaços.")

# Verifica se há pelo menos dois tratamentos com dados válidos
if len(treatments) < 2:
    print("Erro: são necessários pelo menos dois tratamentos para continuar.")
    exit()

# Construção dos dados no formato DataFrame
data = []
for treatment, values in treatments.items():
    for value in values:
        data.append({'Tratamento': treatment, 'Valor': value})

df = pd.DataFrame(data)

# Cálculo do número de tratamentos (t) e do número de repetições por tratamento (r)
unique_treatments = df['Tratamento'].nunique()  # Número de tratamentos (t)
r = len(df) // unique_treatments  # Número de valores por tratamento (r)
GL = (unique_treatments - 1) * (r - 1)  # Grau de Liberdade (GL)

# Imprimindo t (número de médias) e GL (grau de liberdade)
print(f"\nt (número de médias): {unique_treatments}")
print(f"GL (Grau de Liberdade): {GL}")

# Coleta do QME
try:
    QME = float(input("\nDigite o valor de QME: "))
except ValueError:
    print("Erro: o valor de QME deve ser válido.")
    exit()

# Coleta do valor de q
try:
    q = float(input("\nDigite o valor de q (Consultar tabela Tukey): "))
except ValueError:
    print("Erro: o valor de q deve ser válido.")
    exit()

# Cálculo do DMS
DMS = q * np.sqrt(QME / r)
print(f"DMS calculado: {DMS:.4f}")

# Cálculo da média por tratamento
mean_values = df.groupby('Tratamento')['Valor'].mean()

# Ordenação das médias em ordem decrescente
ordered_means = mean_values.sort_values(ascending=False)
ordered_treatments = ordered_means.index.tolist()

# Criação do vetor mediaDMS
mediaDMS = ordered_means - DMS

# Construção da tabela cruzada
comparison_results = pd.DataFrame("-", index=ordered_treatments, columns=ordered_treatments)

# Preenchimento da tabela com os resultados
for i, treatment1 in enumerate(ordered_treatments):
    for j, treatment2 in enumerate(ordered_treatments):
        if i == j:  # Para posições diagonais (A*A, B*B, etc.)
            comparison_results.at[treatment1, treatment2] = "-"
        elif j > i:  # Apenas elementos da matriz triangular superior
            diff = ordered_means[treatment1] - ordered_means[treatment2]
            comparison_results.at[treatment1, treatment2] = "TRUE" if diff > DMS else "FALSE"
        else:  # Elementos da matriz triangular inferior
            comparison_results.at[treatment1, treatment2] = "-"

# Exibindo os resultados
print(
    "\nTabela de comparação cruzada (TRUE = diferença significativa / FALSE = diferença não significativa / '-' = não aplicável):\n")
print(comparison_results)
