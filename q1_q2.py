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
r = df.shape[0] # Número de linhas(r)
t = df.shape[1] # Número de tratamentos

# Cálculos

# Correção para o total (C)
total_sum = df.values.sum() # Somatório de todos valores observados
total_obs = df.size # Número de observações(n)
C = (total_sum ** 2) / total_obs
print(f'\nA correção devida à constante do modelo (C) = {round(C, 4)}\n'.replace('.', ','))

# Soma de Quadrados Total (SQT)
sum_of_squares = (df ** 2).values.sum() # Cada valor elevado ao quadrado
SQT = sum_of_squares - C
# print(f'A soma de quadrados total (SQT) = {round(SQT, 4)}')

# Soma de Quadrados do tratamento (SQTrat)
sqt_colunas = (df.sum() ** 2) / r
SQTrat = sqt_colunas.sum() - C
# print(f"Soma de Quadrados do Tratamento (SQTrat): {round(SQTrat, 4)}")

# Soma de Quadrados de Erros (SQErro)
SQErro = SQT - SQTrat
# print(f"Soma de Quadrados de Erros (SQErro): {round(SQErro, 4)}")

# Causas de variação
# Graus de liberdade (GL)
GL_SQTrat = t -1
GL_SQErro = t*(r-1)
GL_total = t*r -1
# print(f"Graus de liberdade (GL) para SQTrat: {GL_SQTrat}")
# print(f"Graus de liberdade (GL) para SQErro: {GL_SQErro}")
# print(f"Graus de liberdade (GL) para Total: {GL_total}")

# Quadrados Médios (QM)
QM_SQTrat = SQTrat / GL_SQTrat
QM_SQErro = SQErro / GL_SQErro
# print(f'Quadrado médio (QM) para SQTrat: {round(QM_SQTrat, 4)}')
# print(f'Quadrado médio (QM) para SQErro: {round(QM_SQErro, 4)}')

# Estatística F
f_calc = QM_SQTrat/QM_SQErro
# print(f'O valor da estatística F calculado é: {round(F, 2)}')

# Tabela ANOVA
anova_table = pd.DataFrame({
    "Causas de Variação": ["Tratamentos", "Erro", "Total"],
    "GL": [GL_SQTrat, GL_SQErro, GL_total],
    "SQ": [round(SQTrat, 4), round(SQErro, 4), round(SQT, 4)],
    "QM": [round(QM_SQTrat, 4), round(QM_SQErro, 4), None],
    "F": [round(f_calc, 2), None, None]
})
print(f'{anova_table}'.replace('.', ','))

# Teste F
alfa = float(input('\nInsira o nível de significância:'))
# stat, p_value = f_oneway(data["Input1"], data["Input2"], data["Input3"])
# print(f'Estatística F: {stat}')
# print(f'P-value: {p_value}')
# if p_value < alfa:
#     print(f'Rejeitamos a hipótese nula (H₀) ao nível de significância de {alfa}')
# else:
#     print(f'Não rejeitamos a hipótese nula (H₀) ao nível de significância de {alfa}')

# Valor do F crítico(tabela)
f_critico = f.ppf(1 - alfa, GL_SQTrat, GL_SQErro) # 1 - alfa = q. Percentil, teste unilateral superior
print(f'\nF crítico({GL_SQTrat},{GL_SQErro}): {round(f_critico, 2)}'.replace('.', ','))
if round(f_calc, 2) > round(f_critico,2):
    print(f"\nRejeitamos a hipótese nula (H₀) porque F calculado ({round(f_calc, 2)}) > F crítico ({round(f_critico,2)})")
else:
    print(f"\nNão rejeitamos a hipótese nula (H₀) porque F calculado ({round(f_calc, 2)}) < F crítico ({round(f_critico,2)})")