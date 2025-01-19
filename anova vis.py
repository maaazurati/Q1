import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats


# Data input
def criar_dataframe():
    return pd.DataFrame({'altura':[16, 20, 22, 17 ,18,
                            12, 11, 12, 13, 10,
                            20, 18, 14, 16, 19],
                    'especie':["A","A","A","A","A",
                               "B","B","B","B","B",
                               "C","C","C","C","C"]
                         })




##########################################################################
##########################VISUALIZAÇÃO DE DADOS###########################
##########################################################################

# Gráfico de dispersão
def plotar_grafico_dispersao(df):
    # Calculating the global mean
    global_mean = df['altura'].mean()

    # Calculating the mean of each species group
    group_means = df.groupby('especie')['altura'].mean()

    # Creating the scatter plot
    plt.figure(figsize=(8, 6))
    for especie, group_data in df.groupby('especie'):
        plt.scatter([especie] * len(group_data), group_data['altura'], label=f'Espécie {especie}')

    # Adding the global mean as a horizontal line
    plt.axhline(global_mean, color='red', linestyle='--', label='Média Global')

    # Adding points for the means of each species group
    x_coords = list(group_means.index)
    y_coords = list(group_means.tolist())
    plt.plot(x_coords, y_coords, color='blue', linestyle='-', marker='o', label='Linha de Médias')

    for especie, mean in group_means.items():
        plt.scatter(especie, mean, color='black', zorder=5, label=f'Média {especie}')

    # Configuring the plot
    plt.xlabel('Espécie')
    plt.ylabel('Altura')
    plt.title('Gráfico de Dispersão: Altura por Espécie')
    plt.ylim(df['altura'].min() - 2, df['altura'].max() + 2)  # Adjusted y-axis to better center the graph
    plt.legend()
    plt.show()

# Boxplot
def plotar_boxplot(df):
    # Calcular as médias por grupo
    group_means = df.groupby('especie')['altura'].mean()

    # Cores para os boxplots
    colors = ['lightblue', 'lightgreen', 'lightcoral']

    # Criando o boxplot
    plt.figure(figsize=(8, 6))
    boxplot = plt.boxplot(
        [df[df['especie'] == especie]['altura'] for especie in group_means.index],
        patch_artist=True,  # Necessário para permitir colorir os boxplots
        labels=group_means.index
    )

    # Colorindo cada boxplot
    for patch, color in zip(boxplot['boxes'], colors):
        patch.set_facecolor(color)

    # Adicionando estilo às linhas de mediana (preto e negrito)
    for median in boxplot['medians']:
        median.set_color('black')  # Cor preta
        median.set_linewidth(2)  # Mais grosso (negrito)

    # Adicionando os pontos das médias
    x_coords = list(range(1, len(group_means) + 1))
    y_coords = group_means.tolist()
    plt.scatter(x_coords, y_coords, color='black', zorder=5, label='Médias')

    # Adicionando linha tracejada conectando as médias
    plt.plot(x_coords, y_coords, color='black', linestyle='--', zorder=4)

    # Configurando o gráfico
    plt.xlabel('Espécie')
    plt.ylabel('Altura')
    plt.title('Boxplot Comparativo: Altura por Espécie')
    plt.ylim(df['altura'].min() - 2, df['altura'].max() + 2)  # Ajustando os limites do eixo Y
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)  # Adicionando grade para facilitar a leitura
    plt.show()

# Histograma para verificar distribuições aparentes
def plotar_histograma(df):
    # Configurando o tema do gráfico
    sns.set_theme(style="whitegrid")  # Tema minimalista similar ao `theme_minimal`

    # Criando o histograma com KDE
    plt.figure(figsize=(10, 6))
    sns.histplot(
        data=df,
        x="altura",
        hue="especie",  # Diferencia cada espécie
        bins=20,  # Número de divisões no histograma
        kde=True,  # Inclui a curva de densidade suavizada
        palette=["red", "blue", "green"],  # Cores definidas para os grupos
        alpha=0.3,  # Transparência do preenchimento
        element="step",  # Estilo do histograma (barras com bordas)
        stat="density"  # Normaliza o histograma para exibir densidades
    )

    # Customizando o gráfico
    plt.title("Distribuição da Altura por Espécie", fontsize=14)
    plt.xlabel("Altura", fontsize=12)
    plt.ylabel("Densidade", fontsize=12)
    plt.legend(title="Espécie", loc='upper right', fontsize=10)  # Ajustando posição e tamanho da legenda
    plt.grid(axis='y', linestyle='--', alpha=0.7)  # Adicionando grade horizontal

    # Mostrando o gráfico
    plt.show()

# QQ-plots
def criar_qq_plot_por_especie(df):
    """
    Cria QQ-plots por espécie.

    Parâmetros:
    df (DataFrame): DataFrame com as colunas 'altura' e 'especie'.

    Retorna:
    None: Exibe o gráfico.
    """
    sns.set(style="whitegrid")  # Configurando o estilo visual do gráfico

    # Criar a estrutura para multiplots com FacetGrid
    unique_species = df["especie"].unique()
    num_species = len(unique_species)
    fig, axes = plt.subplots(1, num_species, figsize=(6 * num_species, 6), sharey=True)

    for i, especie in enumerate(unique_species):
        ax = axes[i] if num_species > 1 else axes

        # Filtrar os dados para a espécie atual
        group_data = df[df["especie"] == especie]["altura"]

        # Ordenar os dados observados
        y = np.sort(group_data)

        # Calcular quantis teóricos
        quantiles = np.linspace(0, 1, len(y) + 2)[1:-1]  # Excluir 0 e 1
        x = stats.norm.ppf(quantiles, loc=np.mean(y), scale=np.std(y))

        # QQ-plot para essa espécie
        ax.scatter(x, y, alpha=0.7, color=sns.color_palette("tab10")[i], label=f'Espécie {especie}')
        ax.plot(x, x, linestyle="--", color="gray", label="Linha Diagonal (Y=X)")

        # Configurações do gráfico
        ax.set_title(f"QQ-plot para Espécie {especie}")
        ax.set_xlabel("Quantis Teóricos")
        ax.set_ylabel("Quantis Observados")
        ax.legend()

    # Ajuste geral dos subplots
    plt.tight_layout()
    plt.suptitle("QQ-plots das Alturas por Espécie", fontsize=16, y=1.02)
    plt.show()
# terminar qqplots

if __name__ == "__main__":
#Criação única do dataframe
    df = criar_dataframe()

# Escolha doque plotar
#     plotar_grafico_dispersao(df)
#     plotar_boxplot(df)
#     plotar_histograma(df)
#     criar_qq_plot_por_especie(df)

#