import pandas as pd
# from scipy.stats import f_oneway
from scipy.stats import f

# Input dos dados

data = {"Input1": [], "Input2": [], "Input3": []}
for i, key in enumerate(data.keys()):
    user_input = input(f"Insira os valores do tratamento {i + 1}, separados por espaços: ")
    data[key] = user_input.split()

df = pd.DataFrame(data)
df = df.astype(float) # Conversão dos valores
t = df.shape[0] # Número de tratamentos (linhas)
r = df.shape[1] # Número de blocos (colunas)

# Cálculos

# Correção para o total (C)
total_sum = df.values.sum() # Somatório de todos valores observados
# total_obs = df.size # Número de observações(n)
C = (total_sum ** 2) / (r*t)
print(f'\nA correção devida à constante do modelo (C) = {round(C, 4)}\n'.replace('.', ','))

# Soma de Quadrados Total (SQT)
sum_of_squares = (df ** 2).values.sum() # Cada valor elevado ao quadrado
SQT = sum_of_squares - C
# print(f'A soma de quadrados total (SQT) = {round(SQT, 4)}')

# Soma de Quadrados do tratamento (SQTrat)
sqt_linhas = (df.sum(axis=1) ** 2) / r
SQTrat = sqt_linhas.sum() - C
# print(f"Soma de Quadrados do Tratamento (SQTrat): {round(SQTrat, 4)}")

# Soma de Quadrado de Blocos (SQB)
sqt_colunas = (df.sum(axis=0) ** 2) / t
SQB = sqt_colunas.sum() - C

# Soma de Quadrados de Erros (SQErro)
SQErro = SQT - SQTrat - SQB

# Causas de variação
# Graus de liberdade (GL)
GL_SQB = r - 1
GL_SQTrat = t -1
GL_SQErro = (r-1)*(t-1)
GL_total = t*r -1

# Quadrados Médios (QM)
QM_SQB = SQB / GL_SQB
QM_SQTrat = SQTrat / GL_SQTrat
QM_SQErro = SQErro / GL_SQErro

# Estatística F
f_calcBloc = QM_SQB/QM_SQErro
f_calcTrat = QM_SQTrat/QM_SQErro

# Tabela ANOVA
anova_table = pd.DataFrame({
    "Causas de Variação": ["Tratamentos", "Blocos", "Erro", "Total"],
    "GL": [GL_SQTrat, GL_SQB, GL_SQErro, GL_total],
    "SQ": [round(SQTrat, 4), round(SQB, 4), round(SQErro, 4), round(SQT, 4)],
    "QM": [round(QM_SQTrat, 4), round(QM_SQB,4), round(QM_SQErro, 4), None],
    "F": [round(f_calcTrat, 2), round(f_calcBloc, 2),  None, None]
})
print(f'{anova_table}'.replace('.', ','))

# Teste F
# Para Blocos (verificando se o uso de blocos foi importante)
alfa = float(input('\nInsira o nível de significância:'))
# Valor do F crítico(tabela)
f_critBloc = f.ppf(1 - alfa, GL_SQB, GL_SQErro) # 1 - alfa = q. Percentil, teste unilateral superior
# print(f'F crítico({GL_SQB},{GL_SQErro}): {round(f_critBloc, 2)}')
if round(f_calcBloc, 2) > round(f_critBloc,2):
    print(f"\nRejeitamos a hipótese nula (H₀), uso de blocos se revelou importante")
else:
    print(f"\nNão rejeitamos a hipótese nula (H₀), uso de blocos NÃO se revelou importante")

# Para tratamentos
# Valor do F crítico(tabela)
f_critTrat = f.ppf(1 - alfa, GL_SQTrat, GL_SQErro)
# print(f'F crítico({GL_SQTrat},{GL_SQErro}): {round(f_critTrat, 2)}')
if round(f_calcTrat, 2) > round(f_critTrat,2):
    print(f"\nRejeitamos a hipótese nula (H₀) porque F calculado ({round(f_calcTrat, 2)}) > F crítico ({round(f_critTrat,2)})")
    print(f'Há evidência amostral suficiente para afirmar que há diferença entre os tratamentos.')
else:
    print(f"\nNão rejeitamos a hipótese nula (H₀) porque F calculado ({round(f_calcTrat, 2)}) < F crítico ({round(f_critTrat,2)})")
    print(f'Não há evidência amostral suficiente para afirmar que há diferença entre os tratamentos.')